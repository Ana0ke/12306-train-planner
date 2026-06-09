"""
12306 MCP客户端
封装mcp-server-12306 (by drfccv) 的HTTP API
提供真实12306数据查询能力

使用方法：
1. 本地部署 mcp-server-12306 服务（默认端口8000）
2. 配置 MCP_SERVER_URL 环境变量
3. Client12306 会自动检测并优先使用MCP查询

API文档：
- GET /search_stations?keyword=北京南  # 搜索车站
- GET /query_tickets?from=xxx&to=xxx&date=2025-07-17  # 查询余票
- GET /query_transfer?from=xxx&to=xxx&date=xxx  # 查询中转
- GET /get_train_route_stations?trainCode=G101&departDate=2025-07-17  # 经停站
- GET /health  # 健康检查
- GET /get_current_time  # 当前时间
"""

import httpx
import os
import time
from typing import Optional, Union
from loguru import logger

# 请求配置
REQUEST_TIMEOUT_CONNECT = 5.0   # 连接超时（秒）
REQUEST_TIMEOUT_READ = 10.0     # 读取超时（秒）
REQUEST_INTERVAL = 1.0           # 请求间隔（秒），避免触发反爬


class MCPClient:
    """
    12306 MCP客户端
    
    封装 mcp-server-12306 的HTTP API，提供真实12306数据查询。
    所有方法都包含超时设置和异常处理，查询失败时返回None。
    """

    def __init__(self, base_url: Optional[str] = None):
        """
        初始化MCP客户端
        
        Args:
            base_url: MCP服务地址，如 "http://localhost:8000"
                     如果为None，从环境变量 MCP_SERVER_URL 读取
        """
        if base_url is None:
            base_url = os.getenv("MCP_SERVER_URL", "").strip()
        
        self._base_url = base_url.rstrip("/") if base_url else ""
        self._last_request_time = 0.0
        self._available: Optional[bool] = None  # 缓存健康状态
        
        if self._base_url:
            logger.info(f"MCP客户端初始化: {self._base_url}")
        else:
            logger.info("MCP客户端初始化: 未配置 MCP_SERVER_URL")
    
    @property
    def configured(self) -> bool:
        """是否已配置MCP服务地址"""
        return bool(self._base_url)
    
    def is_available(self) -> bool:
        """
        检查MCP服务是否可用（健康检查）
        
        使用缓存避免频繁请求，缓存5秒内有效。
        
        Returns:
            服务可用返回True，否则返回False
        """
        # 使用缓存
        if self._available is not None:
            return self._available
        
        if not self._base_url:
            self._available = False
            return False
        
        try:
            with httpx.Client(timeout=REQUEST_TIMEOUT_CONNECT) as client:
                resp = client.get(f"{self._base_url}/health")
                resp.raise_for_status()
                data = resp.json()
                
                # health接口返回 {"status": "ok"} 或类似
                self._available = data.get("status") == "ok" or resp.status_code == 200
                
                if self._available:
                    logger.info("MCP服务健康检查通过")
                else:
                    logger.warning(f"MCP服务健康检查失败: {data}")
                    
                return self._available
                
        except httpx.TimeoutException:
            logger.warning("MCP服务健康检查超时")
            self._available = False
            return False
        except httpx.HTTPError as e:
            logger.warning(f"MCP服务健康检查失败: {e}")
            self._available = False
            return False
        except Exception as e:
            logger.warning(f"MCP服务健康检查异常: {e}")
            self._available = False
            return False
    
    def _wait_for_interval(self):
        """确保请求间隔至少1秒（避免触发12306反爬）"""
        elapsed = time.time() - self._last_request_time
        if elapsed < REQUEST_INTERVAL:
            time.sleep(REQUEST_INTERVAL - elapsed)
        self._last_request_time = time.time()
    
    def _make_request(self, method: str, path: str, **kwargs) -> Optional[dict]:
        """
        发起HTTP请求的通用方法
        
        包含：
        - 超时设置
        - 请求间隔控制
        - 异常处理
        
        Args:
            method: HTTP方法 (GET/POST等)
            path: API路径
            **kwargs: 其他传递给httpx的参数
            
        Returns:
            成功返回响应JSON，失败返回None
        """
        if not self._base_url:
            return None
        
        self._wait_for_interval()
        
        url = f"{self._base_url}{path}"
        
        try:
            with httpx.Client(timeout=(REQUEST_TIMEOUT_CONNECT, REQUEST_TIMEOUT_READ)) as client:
                resp = client.request(method, url, **kwargs)
                resp.raise_for_status()
                return resp.json()
                
        except httpx.TimeoutException:
            logger.warning(f"MCP请求超时: {url}")
            return None
        except httpx.HTTPError as e:
            logger.warning(f"MCP请求失败: {url}, {e}")
            return None
        except Exception as e:
            logger.warning(f"MCP请求异常: {url}, {e}")
            return None
    
    def search_station(self, keyword: str) -> Optional[dict]:
        """
        搜索车站
        
        支持中文、拼音、简拼模糊搜索。
        优先精确匹配，否则取第一个结果。
        
        Args:
            keyword: 搜索关键词（如"北京南"、"beijingnan"、"bjN"）
            
        Returns:
            匹配的车站信息，格式：
            {
                "name": "北京南",
                "code": "VNP",
                "pinyin": "beijingnan",
                "spell": "BJN"
            }
            搜索失败返回None
        """
        if not keyword:
            return None
        
        data = self._make_request("GET", f"/search_stations?keyword={keyword}")
        
        if data is None:
            return None
        
        # MCP可能返回列表或 {"stations": [...]} 格式
        stations = None
        if isinstance(data, list):
            stations = data
        elif isinstance(data, dict):
            stations = data.get("stations") or data.get("data") or data.get("result")
        
        if not stations:
            logger.warning(f"MCP搜索车站无结果: {keyword}")
            return None
        
        # 精确匹配优先
        keyword_lower = keyword.lower()
        for station in stations:
            name = station.get("name", "").lower()
            if name == keyword_lower:
                logger.info(f"MCP精确匹配车站: {keyword} -> {station.get('name')}")
                return station
        
        # 取第一个结果
        first = stations[0]
        logger.info(f"MCP模糊匹配车站: {keyword} -> {first.get('name')}")
        return first
    
    def search_station_code(self, station_name: str) -> Optional[str]:
        """
        根据站名获取车站代码
        
        Args:
            station_name: 站名（如"北京南"）
            
        Returns:
            车站代码（如"VNP"），未找到返回None
        """
        station = self.search_station(station_name)
        if station:
            return station.get("code")
        return None
    
    def query_tickets(
        self,
        from_station: Union[str, dict],
        to_station: Union[str, dict],
        date: str,
        train_filter: str = "",
    ) -> Optional[list[dict]]:
        """
        查询余票
        
        Args:
            from_station: 出发站，可以是：
                         - 站名（如"北京南"）
                         - 车站代码（如"VNP"）
                         - 已查询的车站信息dict
            to_station: 到达站，同from_station
            date: 日期，格式 yyyy-MM-dd
            train_filter: 车次类型筛选，如 "G"（高铁）、"D"（动车）、"Z"（直达）等
            
        Returns:
            标准化的车次列表，每个元素包含：
            {
                "train_no": "G1",
                "train_code": "G1",
                "from_station": "北京南",
                "to_station": "上海虹桥",
                "from_code": "VNP",
                "to_code": "AOH",
                "depart_time": "09:00",
                "arrive_time": "13:28",
                "duration": "04:28",
                "train_type": "高铁",
                "prices": {
                    "二等座": 553.0,
                    "一等座": 933.0,
                    "商务座": 1748.0
                },
                "remaining": {
                    "二等座": "有",
                    "一等座": "5"
                }
            }
            查询失败返回None
        """
        # 解析出发/到达站
        from_code = self._resolve_station_code(from_station)
        to_code = self._resolve_station_code(to_station)
        
        if not from_code:
            logger.warning(f"无法解析出发站: {from_station}")
            return None
        if not to_code:
            logger.warning(f"无法解析到达站: {to_station}")
            return None
        
        # 构建查询参数
        params = f"?from={from_code}&to={to_code}&date={date}"
        
        data = self._make_request("GET", f"/query_tickets{params}")
        
        if data is None:
            return None
        
        # 解析返回数据
        tickets = self._parse_tickets_response(data, train_filter)
        
        if tickets:
            logger.info(f"MCP查询余票成功: {from_code}->{to_code} {date}, {len(tickets)}条数据")
        else:
            logger.warning(f"MCP查询余票无数据: {from_code}->{to_code} {date}")
        
        return tickets
    
    def _resolve_station_code(self, station: Union[str, dict]) -> Optional[str]:
        """
        解析车站为代码
        
        Args:
            station: 站名、代码或车站信息dict
            
        Returns:
            车站代码
        """
        if isinstance(station, dict):
            return station.get("code")
        if isinstance(station, str):
            if len(station) <= 6 and station.isupper():
                # 看起来像是代码
                return station
            # 尝试搜索
            return self.search_station_code(station)
        return None
    
    def _parse_tickets_response(self, data: dict, train_filter: str) -> Optional[list[dict]]:
        """
        解析MCP余票查询响应
        
        MCP返回格式可能有多种，需要适配：
        1. {"tickets": [...]} 格式
        2. {"data": [...]} 格式
        3. 直接是列表格式
        
        Args:
            data: 响应数据
            train_filter: 车次类型筛选
            
        Returns:
            标准化后的车次列表
        """
        tickets = None
        
        # 尝试提取车次列表
        if isinstance(data, list):
            tickets = data
        elif isinstance(data, dict):
            tickets = (
                data.get("tickets") or 
                data.get("data") or 
                data.get("result") or
                data.get("trains")
            )
        
        if not tickets:
            return None
        
        # 过滤车次类型
        if train_filter:
            filtered = []
            for t in tickets:
                train_code = t.get("train_code") or t.get("train_no") or ""
                if train_code and train_code[0].upper() == train_filter.upper():
                    filtered.append(t)
            tickets = filtered
        
        # 标准化处理
        normalized = []
        for t in tickets:
            normalized_t = self._normalize_ticket(t)
            if normalized_t:
                normalized.append(normalized_t)
        
        return normalized if normalized else None
    
    def _normalize_ticket(self, ticket: dict) -> Optional[dict]:
        """
        将MCP返回的车票数据标准化
        
        目标格式兼容demo_data.py：
        {
            "train_no": "G1",
            "train_code": "G1",
            "from_station": "北京南",
            "to_station": "上海虹桥",
            "depart_time": "09:00",
            "arrive_time": "13:28",
            "duration": "04:28",
            "train_type": "高铁",
            "price_edz": 553.0,
            "price_ydz": 933.0,
            "price_swb": 1748.0,
        }
        
        Args:
            ticket: 原始车票数据
            
        Returns:
            标准化后的数据
        """
        try:
            # 提取车次号
            train_no = (
                ticket.get("train_code") or 
                ticket.get("train_no") or 
                ticket.get("trainNumber") or
                ticket.get("code") or
                ""
            )
            
            if not train_no:
                return None
            
            # 提取时间
            depart_time = ticket.get("depart_time") or ticket.get("departTime") or ""
            arrive_time = ticket.get("arrive_time") or ticket.get("arriveTime") or ""
            duration = ticket.get("duration") or self._calc_duration(depart_time, arrive_time)
            
            # 提取站点信息
            from_station = ticket.get("from_station") or ticket.get("start_station") or ticket.get("from") or ""
            to_station = ticket.get("to_station") or ticket.get("end_station") or ticket.get("to") or ""
            from_code = ticket.get("from_code") or ticket.get("fromStation") or ""
            to_code = ticket.get("to_code") or ticket.get("toStation") or ""
            
            # 提取票价
            prices = ticket.get("prices") or ticket.get("price") or {}
            seat_prices = self._parse_prices(prices)
            
            # 确定车型
            train_type = self._infer_train_type(train_no)
            
            # 构建标准化数据
            result = {
                "train_no": train_no,
                "train_code": train_no,
                "from_station": from_station,
                "to_station": to_station,
                "from_code": from_code,
                "to_code": to_code,
                "depart_time": depart_time,
                "arrive_time": arrive_time,
                "duration": duration,
                "train_type": train_type,
            }
            
            # 添加票价
            result.update(seat_prices)
            
            return result
            
        except Exception as e:
            logger.warning(f"标准化车票数据失败: {ticket}, {e}")
            return None
    
    def _parse_prices(self, prices: Union[dict, float, int]) -> dict:
        """
        解析票价数据
        
        Args:
            prices: 原始票价，可以是dict或单一数值
            
        Returns:
            标准化票价dict
        """
        result = {}
        
        if isinstance(prices, (float, int)):
            # 单一数值作为二等座价格
            result["price_edz"] = float(prices)
            return result
        
        if not isinstance(prices, dict):
            return result
        
        # 座位类型映射（支持多种命名方式）
        seat_mappings = {
            "price_edz": ["二等座", "二等", "edz", "二等座价格", "二等票价"],
            "price_ydz": ["一等座", "一等", "ydz", "一等座价格", "一等票价"],
            "price_swb": ["商务座", "swb", "商务", "商务座价格", "商务票价"],
            "price_yz": ["硬座", "yz", "硬座价格"],
            "price_rw": ["软座", "rw", "软座价格"],
            "price_yw": ["硬卧", "yw", "硬卧价格"],
            "price_gg": ["高级软卧", "gg", "高软"],
        }
        
        for price_key, names in seat_mappings.items():
            for name in names:
                if name in prices:
                    try:
                        result[price_key] = float(prices[name])
                        break
                    except (ValueError, TypeError):
                        pass
        
        return result
    
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
        }
        
        return type_map.get(first_char, "普速")
    
    def _calc_duration(self, depart: str, arrive: str) -> str:
        """
        计算历时（HH:MM格式）
        
        Args:
            depart: 出发时间（HH:MM）
            arrive: 到达时间（HH:MM）
            
        Returns:
            历时字符串（HH:MM）
        """
        try:
            d_parts = depart.split(":")
            a_parts = arrive.split(":")
            
            if len(d_parts) != 2 or len(a_parts) != 2:
                return "00:00"
            
            d_mins = int(d_parts[0]) * 60 + int(d_parts[1])
            a_mins = int(a_parts[0]) * 60 + int(a_parts[1])
            
            # 处理跨天
            if a_mins < d_mins:
                a_mins += 1440
            
            duration_mins = a_mins - d_mins
            hours = duration_mins // 60
            mins = duration_mins % 60
            
            return f"{hours}:{mins:02d}"
            
        except (ValueError, IndexError):
            return "00:00"
    
    def query_transfer(
        self,
        from_station: Union[str, dict],
        to_station: Union[str, dict],
        date: str,
    ) -> Optional[list[dict]]:
        """
        查询中转方案
        
        Args:
            from_station: 出发站
            to_station: 到达站
            date: 日期（yyyy-MM-dd格式）
            
        Returns:
            标准化的中转方案列表，每个元素包含：
            {
                "first_leg": {...},  # 第一程车次信息
                "transfer_station": "武汉",  # 中转站
                "second_leg": {...},  # 第二程车次信息
                "total_duration": "08:30",  # 总历时
                "total_price": 577.0,  # 总价（取二等座之和）
                "wait_time": "00:30"  # 等待时间
            }
            查询失败返回None
        """
        from_code = self._resolve_station_code(from_station)
        to_code = self._resolve_station_code(to_station)
        
        if not from_code or not to_code:
            return None
        
        params = f"?from={from_code}&to={to_code}&date={date}"
        
        data = self._make_request("GET", f"/query_transfer{params}")
        
        if data is None:
            return None
        
        # 解析中转响应
        transfers = self._parse_transfer_response(data)
        
        if transfers:
            logger.info(f"MCP查询中转成功: {from_code}->{to_code} {date}, {len(transfers)}条方案")
        
        return transfers
    
    def _parse_transfer_response(self, data: dict) -> Optional[list[dict]]:
        """
        解析中转查询响应
        
        Args:
            data: 响应数据
            
        Returns:
            标准化后的中转方案列表
        """
        transfers = None
        
        if isinstance(data, list):
            transfers = data
        elif isinstance(data, dict):
            transfers = (
                data.get("transfers") or
                data.get("transfer") or
                data.get("data") or
                data.get("result")
            )
        
        if not transfers:
            return None
        
        normalized = []
        for t in transfers:
            try:
                normalized_t = {
                    "first_leg": self._normalize_ticket(t.get("first_leg") or t.get("leg1") or t),
                    "transfer_station": t.get("transfer_station") or t.get("transfer") or "",
                    "second_leg": self._normalize_ticket(t.get("second_leg") or t.get("leg2")),
                    "total_duration": t.get("total_duration") or t.get("duration") or "00:00",
                    "total_price": float(t.get("total_price") or 0),
                    "wait_time": t.get("wait_time") or t.get("waiting") or "00:00",
                }
                normalized.append(normalized_t)
            except Exception as e:
                logger.warning(f"标准化中转方案失败: {t}, {e}")
        
        return normalized if normalized else None


def test_mcp_client():
    """测试MCP客户端（本地调试用）"""
    import os
    
    # 从环境变量或使用默认值
    base_url = os.getenv("MCP_SERVER_URL", "http://localhost:8000")
    
    client = MCPClient(base_url)
    
    print(f"MCP配置: {base_url}")
    print(f"服务可用: {client.is_available()}")
    
    if client.is_available():
        # 测试搜索车站
        station = client.search_station("北京")
        print(f"搜索北京: {station}")
        
        # 测试查询余票
        tickets = client.query_tickets("北京南", "上海虹桥", "2025-07-17")
        print(f"查询余票: {len(tickets) if tickets else 0} 条")
        if tickets:
            print(f"  第一条: {tickets[0]}")


if __name__ == "__main__":
    test_mcp_client()
