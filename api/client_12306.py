"""
12306查询客户端
封装12306查询接口，支持余票和时刻查询
支持Demo模式（模拟数据）
"""

import httpx
import os
from loguru import logger
from typing import Optional
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 导入demo数据
from api.demo_data import get_demo_routes, has_demo_data, get_demo_transfer_routes


class Client12306:
    """12306查询客户端"""

    # 12306查询接口
    QUERY_URL = "https://kyfw.12306.cn/otn/leftTicket/query"
    STATION_URL = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js"

    # 请求头
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
        "Referer": "https://kyfw.12306.cn/otn/leftTicket/init",
    }

    def __init__(self, demo_mode: Optional[bool] = None):
        """
        初始化12306客户端
        
        Args:
            demo_mode: 是否启用Demo模式，None时从环境变量DEMO_MODE读取
        """
        # 如果未指定demo_mode，从环境变量读取
        if demo_mode is None:
            demo_mode_str = os.getenv("DEMO_MODE", "false").lower()
            demo_mode = demo_mode_str in ("true", "1", "yes")
        
        self._demo_mode = demo_mode
        self._station_map: Optional[dict[str, str]] = None
        self._station_names: Optional[list[str]] = None  # 用于模糊搜索
        
        if self._demo_mode:
            logger.info("12306客户端已启用Demo模式（模拟数据）")

    @property
    def demo_mode(self) -> bool:
        """是否处于Demo模式"""
        return self._demo_mode

    def query(
        self,
        from_station: str,
        to_station: str,
        date: str,
    ) -> list[dict]:
        """
        查询车次信息

        Args:
            from_station: 出发站名（如"长沙南"）
            to_station: 到达站名（如"广州南"）
            date: 日期（如"2026-06-12"）

        Returns:
            车次信息列表
        """
        # Demo模式：使用模糊匹配查询模拟数据
        if self._demo_mode:
            return self._demo_query(from_station, to_station, date)
        
        try:
            # 获取站点代码
            from_code = self._get_station_code(from_station)
            to_code = self._get_station_code(to_station)

            if not from_code or not to_code:
                logger.warning(f"未找到站点代码: {from_station}({from_code}) → {to_station}({to_code})")
                return []

            # 构建查询URL
            url = f"{self.QUERY_URL}"
            params = {
                "leftTicketDTO.train_date": date,
                "leftTicketDTO.from_station": from_code,
                "leftTicketDTO.to_station": to_code,
                "purpose_codes": "ADULT",
            }

            with httpx.Client(timeout=10) as client:
                resp = client.get(url, params=params, headers=self.HEADERS, follow_redirects=True)
                resp.raise_for_status()
                data = resp.json()

            if data.get("httpstatus") != 200:
                logger.error(f"12306查询失败: {data}")
                return []

            # 解析结果
            results = data.get("data", {}).get("result", [])
            return [self._parse_train_info(r) for r in results]

        except httpx.HTTPError as e:
            logger.error(f"12306请求失败: {e}")
            return []
        except Exception as e:
            logger.error(f"12306查询异常: {e}")
            return []

    def _demo_query(
        self,
        from_station: str,
        to_station: str,
        date: str,
    ) -> list[dict]:
        """
        Demo模式查询：支持模糊匹配
        
        策略：
        1. 先用原始站名精确/模糊匹配
        2. 如果没找到，尝试自动解析站名
        3. Demo模式特殊处理：如果两段都有数据，返回第一程（换乘将由planner处理）
        
        Args:
            from_station: 出发站
            to_station: 到达站
            date: 日期
            
        Returns:
            车次信息列表
        """
        # 1. 尝试直接模糊匹配
        routes = get_demo_routes(from_station, to_station)
        if routes:
            logger.info(f"Demo模式找到直达路线: {from_station}→{to_station}, {len(routes)}条数据")
            return routes
        
        # 2. 尝试自动解析站名（处理"深圳" → "深圳北"等）
        resolved_from = self._auto_resolve_station(from_station)
        resolved_to = self._auto_resolve_station(to_station)
        
        if resolved_from != from_station or resolved_to != to_station:
            routes = get_demo_routes(resolved_from, resolved_to)
            if routes:
                logger.info(f"Demo模式站名解析后找到路线: {resolved_from}→{resolved_to}, {len(routes)}条数据")
                return routes
        
        # 3. 尝试换乘匹配（返回第一程）
        leg1, leg2 = get_demo_transfer_routes(from_station, to_station)
        if leg1:
            logger.info(f"Demo模式找到换乘路线（返回第一程）: {from_station}→..., {len(leg1)}条数据")
            # 返回第一程，planner会组合换乘
            return leg1
        
        logger.info(f"Demo模式: 暂无 {from_station}→{to_station} 的模拟数据")
        return []

    def _auto_resolve_station(self, station_name: str) -> str:
        """
        自动解析站名：精确匹配优先，否则模糊匹配取第一个
        
        Demo模式特殊处理：
        - "深圳" → "深圳北"（优先匹配Demo数据中存在的站）
        - "广州" → "广州南"
        
        Args:
            station_name: 用户输入的站名
            
        Returns:
            解析后的标准站名
        """
        if not station_name:
            return station_name
        
        # 精确匹配
        if self._get_station_code(station_name):
            return station_name
        
        # Demo模式特殊映射（将常见简称映射到Demo数据中的站名）
        demo_aliases = {
            "深圳": "深圳北",
            "广州": "广州南",
            "北京": "北京西",
            "上海": "上海虹桥",
            "长沙": "长沙南",
            "武汉": "武汉",
            "成都": "成都东",
            "重庆": "重庆北",
            "杭州": "杭州东",
            "南京": "南京南",
            "西安": "西安北",
            "郑州": "郑州东",
        }
        
        # 先检查别名
        alias_name = demo_aliases.get(station_name)
        if alias_name:
            # 检查别名对应的路线是否在demo数据中存在
            if has_demo_data(alias_name, alias_name):
                return alias_name
        
        # 模糊匹配
        matches = self.fuzzy_search_stations(station_name)
        if matches:
            # Demo模式优先选择Demo数据中存在的站
            if self._demo_mode:
                for match in matches:
                    # 检查该站是否出现在任何demo路线中
                    from api.demo_data import DEMO_DATA
                    for route_key in DEMO_DATA:
                        parts = route_key.split("-", 1)
                        if len(parts) == 2 and match in parts:
                            logger.info(f"Demo模式站名模糊匹配: '{station_name}' → '{match}'")
                            return match
            
            logger.info(f"站名模糊匹配: '{station_name}' → '{matches[0]}'")
            return matches[0]
        
        # 无法匹配，返回原值
        logger.warning(f"无法匹配站名: {station_name}")
        return station_name

    def fuzzy_search_stations(self, keyword: str) -> list[str]:
        """
        模糊搜索站点名称
        
        Args:
            keyword: 关键词
            
        Returns:
            所有包含关键词的站名列表（按相关性排序）
        """
        if not keyword:
            return []
        
        # 确保站点数据已加载
        if self._station_names is None:
            self._load_station_data()
        
        keyword_lower = keyword.lower()
        matches = []
        
        for name in self._station_names:
            if keyword_lower in name.lower():
                # 优先完全匹配的
                if name == keyword:
                    matches.insert(0, name)
                else:
                    matches.append(name)
        
        return matches

    def _get_station_code(self, station_name: str) -> Optional[str]:
        """获取站点电报码"""
        if self._station_map is None:
            self._load_station_data()
        return self._station_map.get(station_name)

    def _load_station_data(self):
        """加载站点数据（名称→电报码映射 + 站名列表）"""
        self._station_map = {}
        self._station_names = []
        
        try:
            with httpx.Client(timeout=15) as client:
                resp = client.get(self.STATION_URL, headers=self.HEADERS, follow_redirects=True)
                resp.raise_for_status()
                text = resp.text

            # 解析 station_name.js 格式
            # 格式: @bjb|北京北|VAP|beijingbei|bjb|0
            for entry in text.split("@")[1:]:
                parts = entry.split("|")
                if len(parts) >= 3:
                    name = parts[1]       # 站名
                    code = parts[2]       # 电报码
                    self._station_map[name] = code
                    self._station_names.append(name)

            logger.info(f"加载站点映射: {len(self._station_map)} 个站点")

        except Exception as e:
            logger.error(f"加载站点映射失败: {e}")
            # 使用预置常用站点
            self._fallback_station_map()

    def _fallback_station_map(self):
        """使用预置的常用站点"""
        self._station_map = {
            # 直辖市
            "北京": "BJP", "北京西": "BXP", "北京南": "VNP", "北京北": "VAP", "北京东": "BDP",
            "上海": "SHH", "上海虹桥": "AOH", "上海南": "SNH", "上海西": "SXH",
            "天津": "TJP", "天津西": "TXF", "天津南": "TIP",
            "重庆": "CQW", "重庆北": "CUW", "重庆西": "CXW",
            
            # 广东省
            "广州": "GZQ", "广州南": "IZQ", "广州东": "GGQ", "广州西": "GXQ", "广州北": "BBQ",
            "深圳": "SZQ", "深圳北": "IOQ", "深圳东": "BJQ", "深圳西": "SJQ",
            
            # 湖南省
            "长沙": "CSQ", "长沙南": "CWQ", "长沙西": "CXQ",
            "衡阳": "HYC", "衡阳东": "HVQ",
            "株洲": "ZZC", "株洲西": "ZAQ",
            "永州": "YNQ",
            "东安东": "DAZ",
            
            # 湖北省
            "武汉": "WHN", "武汉西": "WEF", "汉口": "HKN", "武昌": "WCN",
            
            # 河南省
            "郑州": "ZZF", "郑州东": "ZAF", "郑州西": "XPF",
            "洛阳": "LYF", "洛阳龙门": "LLF",
            
            # 江苏省
            "南京": "NJH", "南京南": "NKH", "南京北": "NJH",
            "苏州": "SZH", "苏州北": "OBH",
            "无锡": "WXH",
            "常州": "CZH",
            "镇江": "ZJH",
            
            # 浙江省
            "杭州": "HZH", "杭州东": "HGH", "杭州南": "XHH", "杭州西": "XGH",
            "宁波": "NGH", "宁波东": "GLH",
            "温州": "RZH", "温州南": "VRH",
            "义乌": "YWG",
            
            # 四川省
            "成都": "CDW", "成都东": "ICW", "成都南": "CNW", "成都西": "CXW",
            "绵阳": "MYW",
            "乐山": "USW",
            "宜宾": "YBW",
            
            # 重庆市辖区
            "万州": "WYW",
            
            # 贵州省
            "贵阳": "GIW", "贵阳北": "KQW", "贵阳东": "KEW",
            
            # 云南省
            "昆明": "KMM", "昆明南": "KOM", "昆明西": "KXM",
            "大理": "DKM",
            "丽江": "LJM",
            
            # 陕西省
            "西安": "XAY", "西安北": "EAO", "西安南": "CAY",
            "西安西": "EAS",
            "宝鸡": "BJY",
            
            # 甘肃省
            "兰州": "LZJ", "兰州西": "LAJ", "兰州东": "LDJ",
            "敦煌": "DHJ",
            "嘉峪关": "JXJ",
            
            # 青海省
            "西宁": "XNO",
            "格尔木": "GRO",
            
            # 西藏
            "拉萨": "LSO",
            
            # 新疆
            "乌鲁木齐": "WMR", "乌鲁木齐南": "WAR",
            "吐鲁番": "TFR",
            "哈密": "HMR",
            
            # 东北三省
            "哈尔滨": "HRB", "哈尔滨西": "VBB", "哈尔滨东": "VAB",
            "长春": "CCT", "长春西": "CRT",
            "沈阳": "SYT", "沈阳北": "SBT", "沈阳南": "SOD",
            "大连": "DLT", "大连北": "RRT",
            
            # 广西
            "南宁": "NNZ", "南宁东": "NFZ",
            "桂林": "GLZ", "桂林北": "GBZ",
            "柳州": "LZZ",
            "北海": "BHZ",
            
            # 福建省
            "福州": "FZS", "福州南": "FYS", "福州北": "FBZ",
            "厦门": "XMS", "厦门北": "XKS",
            "泉州": "QYS",
            
            # 江西省
            "南昌": "NCG", "南昌西": "NXG",
            "赣州": "GZG",
            "九江": "JJG",
            
            # 安徽省
            "合肥": "HFH", "合肥南": "ENH", "合肥西": "HTH",
            "黄山": "HKD",
            "芜湖": "WHH",
            
            # 山东省
            "济南": "JNK", "济南西": "JGK",
            "青岛": "QDK", "青岛北": "QHK",
            "烟台": "YAK",
            "威海": "WKK",
            
            # 山西省
            "太原": "TYV", "太原南": "TNV",
            "大同": "DTV",
            
            # 河北省
            "石家庄": "SJP", "石家庄东": "SXP",
            "保定": "BDP",
            "唐山": "TSP",
            
            # 内蒙古
            "呼和浩特": "HHC",
            "包头": "BTC",
            
            # 海南省
            "海口": "HMQ", "海口东": "KEQ",
            "三亚": "SEQ",
            
            # 宁夏
            "银川": "YIJ",
            
            # 香港（高铁）
            "香港西九龙": "XJA",
        }
        self._station_names = list(self._station_map.keys())

    def _parse_train_info(self, raw_str: str) -> dict:
        """
        解析12306返回的车次信息字符串
        格式: 预订|车次|出发站|到达站|出发时间|到达时间|历时|...
        """
        try:
            fields = raw_str.split("|")
            return {
                "train_no": fields[3] if len(fields) > 3 else "",
                "from_station_code": fields[6] if len(fields) > 6 else "",
                "to_station_code": fields[7] if len(fields) > 7 else "",
                "depart_time": fields[8] if len(fields) > 8 else "",
                "arrive_time": fields[9] if len(fields) > 9 else "",
                "duration": fields[10] if len(fields) > 10 else "",
            }
        except Exception as e:
            logger.warning(f"解析车次信息失败: {e}")
            return {}
