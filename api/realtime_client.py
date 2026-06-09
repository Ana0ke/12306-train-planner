"""
12306真实查询客户端 - 内嵌版
直接请求12306接口，无需外部服务

功能：
- 余票查询（支持G/D/C/Z/T/K等车型）
- 中转方案查询
- 车站代码解析

注意：
- 需要正确的Cookie才能查询，建议设置环境变量 USE_REALTIME=false 禁用
- 12306有反爬机制，查询间隔至少1.5秒
- 部分请求可能需要从init页面动态获取query URL
"""

import httpx
import json
import logging
import time
from pathlib import Path
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)

# 12306 API URLs
INIT_URL = "https://kyfw.12306.cn/otn/leftTicket/init"
QUERY_URL = "https://kyfw.12306.cn/otn/leftTicket/queryG"
TRANSFER_URL = "https://kyfw.12306.cn/lcquery/queryG"

# 请求头
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Referer": "https://kyfw.12306.cn/otn/leftTicket/init",
    "Host": "kyfw.12306.cn",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://kyfw.12306.cn"
}

# 座位类型映射（字段名 → 中文名）
SEAT_FIELDS = {
    "swz_num": "商务座",
    "tz_num": "特等座",
    "zy_num": "一等座",
    "ze_num": "二等座",
    "rw_num": "软卧",
    "yw_num": "硬卧",
    "yz_num": "硬座",
    "wz_num": "无座",
    "gr_num": "高级软卧",
    "dw_num": "动卧",
}

# 票价字段映射（字段名 → 中文名）
PRICE_FIELDS = {
    "swz_price": "商务座",
    "tz_price": "特等座",
    "zy_price": "一等座",
    "ze_price": "二等座",
    "yw_price": "硬卧",
    "rw_price": "软卧",
    "yz_price": "硬座",
    "wz_price": "无座",
    "gr_price": "高级软卧",
    "dw_price": "动卧",
}


class RealtimeClient:
    """12306真实查询客户端"""

    def __init__(self, station_codes_path: Optional[str] = None):
        """
        初始化客户端
        
        Args:
            station_codes_path: 站名→三字码映射文件路径
        """
        self._station_codes: Dict[str, str] = {}
        self._last_query_time = 0.0
        self._min_interval = 1.5  # 最小查询间隔（秒），防反爬
        self._query_urls: List[str] = []  # 动态query URL列表
        
        # 加载站名代码映射
        if station_codes_path:
            self._load_station_codes(station_codes_path)
        else:
            # 默认从data目录加载
            code_file = Path(__file__).resolve().parent.parent / "data" / "station_codes.json"
            if code_file.exists():
                self._load_station_codes(str(code_file))

    def _load_station_codes(self, file_path: str):
        """加载站名→三字码映射"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self._station_codes = json.load(f)
            logger.info(f"已加载 {len(self._station_codes)} 个车站代码")
        except Exception as e:
            logger.warning(f"加载车站代码失败: {e}")

    def get_station_code(self, name: str) -> Optional[str]:
        """
        站名→三字码转换
        
        Args:
            name: 站名（如"长沙南"、"深圳"）
            
        Returns:
            三字码（如"CWQ"、"IOQ"），未找到返回None
        """
        if not name:
            return None
        
        name = name.strip()
        
        # 直接匹配
        if name in self._station_codes:
            return self._station_codes[name]
        
        # 去掉末尾"站"
        if name.endswith("站") and len(name) > 1:
            short_name = name[:-1]
            if short_name in self._station_codes:
                return self._station_codes[short_name]
        
        # 如果已经是三字码（3位大写字母）
        if len(name) == 3 and name.isalpha() and name.isupper():
            return name
        
        return None

    def get_station_name(self, code: str) -> Optional[str]:
        """
        三字码→站名转换
        
        Args:
            code: 三字码
            
        Returns:
            站名，未找到返回None
        """
        for name, c in self._station_codes.items():
            if c == code:
                return name
        return None

    def _rate_limit(self):
        """请求限流"""
        now = time.time()
        elapsed = now - self._last_query_time
        if elapsed < self._min_interval:
            time.sleep(self._min_interval - elapsed)
        self._last_query_time = time.time()

    def _get_session_cookies(self) -> Optional[Dict[str, str]]:
        """
        访问init页面获取Cookie
        
        Returns:
            Cookie字典，失败返回None
        """
        try:
            with httpx.Client(timeout=8, verify=False) as client:
                resp = client.get(INIT_URL, headers=HEADERS, follow_redirects=True, timeout=8)
                if resp.status_code == 200:
                    # 返回cookie字典
                    return dict(resp.cookies)
                return None
        except Exception as e:
            logger.warning(f"获取12306会话Cookie失败: {e}")
            return None

    def _extract_query_urls(self, init_html: str) -> List[str]:
        """
        从init页面HTML中提取query URL
        
        12306的查询URL可能是：
        - /otn/leftTicket/queryG
        - /otn/leftTicket/queryZ
        - /otn/leftTicket/query
        等，需要从页面脚本中提取
        
        Args:
            init_html: init页面HTML内容
            
        Returns:
            可用的query URL列表
        """
        import re
        
        urls = []
        
        # 尝试匹配 CLeftTicketUrl 配置
        patterns = [
            r'CLeftTicketUrl\s*=\s*["\']([^"\']+)["\']',
            r'var\s+url\s*=\s*["\']([^"\']*query[^"\']*)["\']',
            r'["\']/(otn/leftTicket/query[^"\']*)["\']',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, init_html, re.IGNORECASE)
            for m in matches:
                if m.startswith('/'):
                    m = 'https://kyfw.12306.cn' + m
                if m not in urls:
                    urls.append(m)
        
        # 默认URL
        default_urls = [
            "https://kyfw.12306.cn/otn/leftTicket/queryG",
            "https://kyfw.12306.cn/otn/leftTicket/queryZ",
            "https://kyfw.12306.cn/otn/leftTicket/query",
        ]
        
        for u in default_urls:
            if u not in urls:
                urls.append(u)
        
        return urls

    def query_tickets(
        self,
        from_station: str,
        to_station: str,
        date: str,
    ) -> Optional[List[dict]]:
        """
        查询真实余票信息
        
        Args:
            from_station: 出发站名（如"长沙南"）
            to_station: 到达站名（如"广州南"）
            date: 日期，格式 YYYY-MM-DD
            
        Returns:
            标准化的车次列表，失败返回None
        """
        from_code = self.get_station_code(from_station)
        to_code = self.get_station_code(to_station)
        
        if not from_code:
            logger.warning(f"无法获取出发站代码: {from_station}")
            return None
        if not to_code:
            logger.warning(f"无法获取到达站代码: {to_station}")
            return None
        
        self._rate_limit()
        
        # 获取会话Cookie
        cookies = self._get_session_cookies()
        if not cookies:
            logger.warning("无法获取12306会话Cookie")
            return None
        
        # 查询参数
        params = {
            "leftTicketDTO.train_date": date,
            "leftTicketDTO.from_station": from_code,
            "leftTicketDTO.to_station": to_code,
            "purpose_codes": "ADULT"
        }
        
        # 尝试多个query URL
        query_urls = [
            "https://kyfw.12306.cn/otn/leftTicket/queryG",
            "https://kyfw.12306.cn/otn/leftTicket/queryZ",
            "https://kyfw.12306.cn/otn/leftTicket/query",
        ]
        
        for query_url in query_urls:
            try:
                with httpx.Client(timeout=8, verify=False) as client:
                    # 设置cookie
                    client.cookies.update(cookies)
                    
                    resp = client.get(
                        query_url,
                        headers=HEADERS,
                        params=params,
                        timeout=8
                    )
                    
                    if resp.status_code == 200:
                        try:
                            data = resp.json()
                            
                            # 检查响应状态
                            if data.get("httpstatus") == 200 and "data" in data:
                                tickets = self._parse_tickets(data["data"], date)
                                if tickets:
                                    logger.info(
                                        f"12306查询成功: {from_station}({from_code})→"
                                        f"{to_station}({to_code}) {date}, {len(tickets)}条数据"
                                    )
                                    return tickets
                            
                            # 检查是否需要用c_url
                            if data.get("status") == False:
                                c_url = data.get("c_url", "")
                                if c_url:
                                    real_url = f"https://kyfw.12306.cn/otn/leftTicket/{c_url}"
                                    resp2 = client.get(
                                        real_url,
                                        headers=HEADERS,
                                        params=params,
                                        timeout=8
                                    )
                                    if resp2.status_code == 200:
                                        data2 = resp2.json()
                                        if data2.get("httpstatus") == 200 and "data" in data2:
                                            tickets = self._parse_tickets(data2["data"], date)
                                            if tickets:
                                                logger.info(
                                                    f"12306查询成功(c_url): {from_station}→{to_station}, "
                                                    f"{len(tickets)}条数据"
                                                )
                                                return tickets
                            
                        except json.JSONDecodeError:
                            continue
                    elif resp.status_code == 302:
                        # 被重定向，可能被反爬
                        logger.warning("12306查询被重定向，可能触发反爬")
                        continue
                        
            except (httpx.TimeoutException, httpx.NetworkError) as e:
                logger.warning(f"12306查询网络错误({query_url}): {e}")
                continue
            except Exception as e:
                logger.warning(f"12306查询异常({query_url}): {e}")
                continue
        
        logger.warning(f"12306查询未返回有效数据: {from_station}→{to_station}")
        return None

    def _parse_tickets(self, raw_data: dict, date: str) -> List[dict]:
        """
        解析12306返回的余票数据
        
        Args:
            raw_data: 原始响应数据
            date: 查询日期
            
        Returns:
            标准化后的车次列表
        """
        results = []
        
        try:
            # raw_data可能是dict或list
            if isinstance(raw_data, dict):
                # 尝试获取result字段
                raw_list = raw_data.get("result") or raw_data.get("datas") or []
            elif isinstance(raw_data, list):
                raw_list = raw_data
            else:
                return results
            
            for item in raw_list:
                try:
                    ticket = self._parse_single_ticket(item, date)
                    if ticket:
                        results.append(ticket)
                except Exception as e:
                    logger.debug(f"解析单条车票失败: {e}")
                    continue
                    
        except Exception as e:
            logger.warning(f"解析车票数据失败: {e}")
        
        return results

    def _parse_single_ticket(self, item, date: str) -> Optional[dict]:
        """
        解析单条车票数据
        
        12306返回的数据结构：
        - item可能是字符串（@分隔）或字典
        """
        try:
            # 处理字符串格式
            if isinstance(item, str):
                fields = item.split("@")
                if len(fields) < 20:
                    return None
                    
                # 字符串格式解析
                # secretStr|buttonTextInfo|train_no|code|from_code|to_code|
                # from_name|to_name|start_time|arrive_time|duration|...
                dto = {
                    "secretStr": fields[0],
                    "buttonTextInfo": fields[1] if len(fields) > 1 else "",
                    "train_no": fields[2] if len(fields) > 2 else "",
                    "station_train_code": fields[3] if len(fields) > 3 else "",
                    "start_station_telecode": fields[4] if len(fields) > 4 else "",
                    "end_station_telecode": fields[5] if len(fields) > 5 else "",
                    "from_station_telecode": fields[6] if len(fields) > 6 else "",
                    "to_station_telecode": fields[7] if len(fields) > 7 else "",
                    "start_time": fields[8] if len(fields) > 8 else "",
                    "arrive_time": fields[9] if len(fields) > 9 else "",
                    "lishi": fields[10] if len(fields) > 10 else "",
                    "canWebBuy": fields[11] if len(fields) > 11 else "",
                    "from_station_name": self.get_station_name(fields[6]) if len(fields) > 6 else "",
                    "to_station_name": self.get_station_name(fields[7]) if len(fields) > 7 else "",
                }
                
            elif isinstance(item, dict):
                # 字典格式（queryLeftNewDTO）
                dto = item.get("queryLeftNewDTO", item)
            else:
                return None
            
            # 提取基本信息
            train_no = dto.get("station_train_code", dto.get("train_no", ""))
            if not train_no:
                return None
            
            from_code = dto.get("from_station_telecode", "")
            to_code = dto.get("to_station_telecode", "")
            
            # 提取余票信息
            remaining = {}
            for field, name in SEAT_FIELDS.items():
                val = dto.get(field, "")
                if val and val != "--" and val != "*" and val != "无":
                    remaining[name] = val
            
            # 提取票价信息
            prices = {}
            for field, name in PRICE_FIELDS.items():
                val = dto.get(field, "")
                if val and val != "--":
                    try:
                        # 12306票价最后一位是角（如"553.00"或"5530"）
                        if isinstance(val, str):
                            val = val.replace(".00", "")
                        p = float(val)
                        if p > 100:  # 超过100元，需要除以10（角变元）
                            p = round(p / 10, 1)
                        prices[name] = p
                    except (ValueError, TypeError):
                        pass
            
            # 构建结果
            result = {
                "train_no": train_no,
                "train_code": train_no,
                "from_station": dto.get("from_station_name", self.get_station_name(from_code) or ""),
                "to_station": dto.get("to_station_name", self.get_station_name(to_code) or ""),
                "from_code": from_code,
                "to_code": to_code,
                "depart_time": dto.get("start_time", ""),
                "arrive_time": dto.get("arrive_time", ""),
                "duration": dto.get("lishi", ""),
                "train_type": self._infer_train_type(train_no),
                "remaining": remaining,
                "prices": prices,
                "date": date,
                "is_realtime": True,
            }
            
            # 添加价格字段（兼容旧格式）
            if "二等座" in prices:
                result["price_edz"] = prices["二等座"]
            if "一等座" in prices:
                result["price_ydz"] = prices["一等座"]
            if "商务座" in prices:
                result["price_swb"] = prices["商务座"]
            if "硬座" in prices:
                result["price_yz"] = prices["硬座"]
            if "硬卧" in prices:
                result["price_yw"] = prices["硬卧"]
            if "软卧" in prices:
                result["price_rw"] = prices["软卧"]
            
            return result
            
        except Exception as e:
            logger.debug(f"解析车票条目失败: {e}")
            return None

    def _infer_train_type(self, train_no: str) -> str:
        """
        根据车次号推断车型
        
        Args:
            train_no: 车次号
            
        Returns:
            车型名称
        """
        if not train_no:
            return "未知"
        
        first_char = train_no[0].upper()
        
        type_map = {
            "G": "高铁",
            "D": "动车",
            "C": "城际",
            "Z": "直达",
            "T": "特快",
            "K": "快速",
            "Y": "旅游",
            "L": "临时",
            "W": "外局",
        }
        
        return type_map.get(first_char, "普速")

    def query_transfer(
        self,
        from_station: str,
        to_station: str,
        date: str,
    ) -> Optional[List[dict]]:
        """
        查询中转方案
        
        Args:
            from_station: 出发站
            to_station: 到达站
            date: 日期
            
        Returns:
            中转方案列表
        """
        from_code = self.get_station_code(from_station)
        to_code = self.get_station_code(to_station)
        
        if not from_code or not to_code:
            return None
        
        self._rate_limit()
        
        # 获取会话Cookie
        cookies = self._get_session_cookies()
        if not cookies:
            return None
        
        params = {
            "from_station_telecode": from_code,
            "to_station_telecode": to_code,
            "train_date": date,
            "middle_station": "",
            "isShowWZ": "N"
        }
        
        try:
            with httpx.Client(timeout=8, verify=False) as client:
                client.cookies.update(cookies)
                
                resp = client.get(
                    TRANSFER_URL,
                    headers=HEADERS,
                    params=params,
                    timeout=8
                )
                
                if resp.status_code == 200:
                    data = resp.json()
                    if data.get("httpstatus") == 200 and "data" in data:
                        return self._parse_transfer(data["data"], date)
                
                return None
                
        except Exception as e:
            logger.warning(f"中转查询失败: {e}")
            return None

    def _parse_transfer(self, raw_data: list, date: str) -> List[dict]:
        """
        解析中转方案数据
        
        Args:
            raw_data: 原始数据
            date: 查询日期
            
        Returns:
            标准化后的中转方案列表
        """
        results = []
        
        for item in raw_data:
            try:
                if not isinstance(item, dict):
                    continue
                
                # 提取中转站信息
                middle_station = item.get("middle_station_name", "")
                wait_time = item.get("wait_time", "")
                total_duration = item.get("all_lishi", "")
                
                # 提取两段行程
                segments = []
                for seg_key in ["0", "1", "first_leg", "second_leg"]:
                    seg = item.get(seg_key, {})
                    if seg and isinstance(seg, dict):
                        train_code = seg.get("station_train_code", seg.get("train_no", ""))
                        from_name = seg.get("from_station_name", "")
                        to_name = seg.get("to_station_name", "")
                        
                        remaining = {}
                        for field, name in SEAT_FIELDS.items():
                            val = seg.get(field, "")
                            if val and val != "--":
                                remaining[name] = val
                        
                        segments.append({
                            "train_no": train_code,
                            "train_code": train_code,
                            "from_station": from_name,
                            "to_station": to_name,
                            "departure_time": seg.get("start_time", ""),
                            "arrival_time": seg.get("arrive_time", ""),
                            "duration": seg.get("lishi", ""),
                            "remaining": remaining,
                            "is_realtime": True,
                        })
                
                if len(segments) >= 2:
                    results.append({
                        "transfer_station": middle_station,
                        "wait_time": wait_time,
                        "total_duration": total_duration,
                        "first_leg": segments[0],
                        "second_leg": segments[1],
                        "is_realtime": True,
                    })
                    
            except Exception as e:
                logger.debug(f"解析中转数据失败: {e}")
                continue
        
        return results

    def is_available(self) -> bool:
        """
        检测12306是否可达
        
        Returns:
            服务可用返回True
        """
        try:
            with httpx.Client(timeout=5, verify=False) as client:
                resp = client.get(
                    "https://kyfw.12306.cn/otn/leftTicket/init",
                    headers={"User-Agent": HEADERS["User-Agent"]},
                    follow_redirects=True,
                    timeout=5
                )
                return resp.status_code == 200
        except:
            return False


def create_realtime_client() -> RealtimeClient:
    """
    创建12306实时查询客户端的工厂函数
    
    Returns:
        RealtimeClient实例
    """
    return RealtimeClient()
