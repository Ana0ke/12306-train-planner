"""
12306查询客户端
支持内嵌实时查询和Demo模式

查询策略（按优先级）：
1. 默认尝试真实查询（RealtimeClient），失败自动fallback到Demo模式
2. USE_REALTIME=false → 强制禁用真实查询，只用Demo数据
3. DEMO_MODE=true → 强制使用Demo数据
"""

import os
from loguru import logger
from typing import Optional, List
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 导入demo数据
from api.demo_data import get_demo_routes, has_demo_data, get_demo_transfer_routes

# 导入真实查询客户端
from api.realtime_client import RealtimeClient


class Client12306:
    """12306查询客户端"""

    # 12306官方站点数据URL（用于备用）
    STATION_URL = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js"

    # 请求头
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
        "Referer": "https://kyfw.12306.cn/otn/leftTicket/init",
    }

    def __init__(self, demo_mode: Optional[bool] = None, use_realtime: Optional[bool] = None):
        """
        初始化12306客户端
        
        Args:
            demo_mode: 是否启用Demo模式，None时从环境变量DEMO_MODE读取
            use_realtime: 是否使用真实查询，None时从环境变量USE_REALTIME读取
        """
        # Demo模式（默认关闭，真实查询失败时自动fallback）
        if demo_mode is None:
            demo_mode_str = os.getenv("DEMO_MODE", "false").lower()
            demo_mode = demo_mode_str in ("true", "1", "yes")
        self._demo_mode = demo_mode
        
        # 真实查询模式（默认开启，除非显式禁用）
        if use_realtime is None:
            use_realtime_str = os.getenv("USE_REALTIME", "true").lower()
            use_realtime = use_realtime_str not in ("false", "0", "no")
        self._use_realtime = use_realtime
        
        self._station_map: Optional[dict[str, str]] = None
        self._station_names: Optional[list[str]] = None
        
        # 初始化RealtimeClient
        self._realtime_client: Optional[RealtimeClient] = None
        if self._use_realtime:
            try:
                self._realtime_client = RealtimeClient()
                if self._realtime_client.is_available():
                    logger.info("12306客户端已启用实时查询模式")
                else:
                    logger.warning("12306服务不可用，将使用Demo模式")
                    self._use_realtime = False
                    self._demo_mode = True
            except Exception as e:
                logger.warning(f"初始化RealtimeClient失败: {e}，将使用Demo模式")
                self._use_realtime = False
                self._demo_mode = True
        
        if self._demo_mode:
            logger.info("12306客户端已启用Demo模式（模拟数据）")
    
    @property
    def use_realtime(self) -> bool:
        """是否使用真实查询"""
        return self._use_realtime and self._realtime_client is not None

    @property
    def demo_mode(self) -> bool:
        """是否处于Demo模式"""
        return self._demo_mode

    def query(
        self,
        from_station: str,
        to_station: str,
        date: str,
    ) -> List[dict]:
        """
        查询车次信息

        Args:
            from_station: 出发站名（如"长沙南"）
            to_station: 到达站名（如"广州南"）
            date: 日期（如"2026-06-12"）

        Returns:
            车次信息列表
        """
        # 实时查询优先
        if self.use_realtime:
            try:
                realtime_tickets = self._realtime_client.query_tickets(
                    from_station=from_station,
                    to_station=to_station,
                    date=date,
                )
                if realtime_tickets:
                    logger.info(
                        f"实时查询成功: {from_station}→{to_station}, "
                        f"{len(realtime_tickets)}条数据"
                    )
                    return realtime_tickets
            except Exception as e:
                logger.warning(f"实时查询失败: {e}，将fallback到Demo模式")
        
        # Demo模式fallback
        if self._demo_mode:
            return self._demo_query(from_station, to_station, date)
        
        return []

    def query_tickets(
        self,
        from_station: str,
        to_station: str,
        date: str,
    ) -> Optional[List[dict]]:
        """
        查询余票信息
        
        Args:
            from_station: 出发站
            to_station: 到达站
            date: 日期
            
        Returns:
            车次信息列表，查询失败时返回None
        """
        result = self.query(from_station, to_station, date)
        return result if result else None

    def _demo_query(
        self,
        from_station: str,
        to_station: str,
        date: str,
    ) -> List[dict]:
        """
        Demo模式查询：支持模糊匹配
        
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
        
        # 2. 尝试自动解析站名
        resolved_from = self._auto_resolve_station(from_station)
        resolved_to = self._auto_resolve_station(to_station)
        
        if resolved_from != from_station or resolved_to != to_station:
            routes = get_demo_routes(resolved_from, resolved_to)
            if routes:
                logger.info(f"Demo模式站名解析后找到路线: {resolved_from}→{resolved_to}, {len(routes)}条数据")
                return routes
        
        # 3. 尝试换乘匹配
        leg1, leg2 = get_demo_transfer_routes(from_station, to_station)
        if leg1:
            logger.info(f"Demo模式找到换乘路线（返回第一程）: {from_station}→..., {len(leg1)}条数据")
            return leg1
        
        logger.info(f"Demo模式: 暂无 {from_station}→{to_station} 的模拟数据")
        return []

    def _auto_resolve_station(self, station_name: str) -> str:
        """
        自动解析站名：精确匹配优先，否则模糊匹配取第一个
        
        Demo模式特殊处理：
        - "深圳" → "深圳北"（优先匹配Demo数据中存在的站）
        - "广州" → "广州南"
        """
        if not station_name:
            return station_name
        
        # 精确匹配
        if self._get_station_code(station_name):
            return station_name
        
        # Demo模式特殊映射
        demo_aliases = {
            "深圳": "深圳北",
            "广州": "广州南",
            "北京": "北京南",
            "上海": "上海虹桥",
            "长沙": "长沙南",
            "武汉": "武汉",
            "成都": "成都东",
            "重庆": "重庆北",
            "杭州": "杭州东",
            "南京": "南京南",
            "西安": "西安北",
            "郑州": "郑州东",
            "昆明": "昆明南",
            "贵阳": "贵阳北",
            "南昌": "南昌西",
            "济南": "济南",
            "青岛": "青岛北",
            "沈阳": "沈阳",
            "大连": "大连",
            "哈尔滨": "哈尔滨西",
            "长春": "长春",
            "福州": "福州",
            "厦门": "厦门北",
            "兰州": "兰州西",
            "西宁": "西宁",
            "太原": "太原",
            "石家庄": "石家庄",
            "南宁": "南宁东",
            "海口": "海口",
        }
        
        # 先检查别名
        alias_name = demo_aliases.get(station_name)
        if alias_name:
            if has_demo_data(alias_name, alias_name):
                return alias_name
        
        # 模糊匹配
        matches = self.fuzzy_search_stations(station_name)
        if matches:
            # Demo模式优先选择Demo数据中存在的站
            if self._demo_mode:
                from api.demo_data import DEMO_DATA
                for match in matches:
                    for route_key in DEMO_DATA:
                        parts = route_key.split("-", 1)
                        if len(parts) == 2 and match in parts:
                            logger.info(f"Demo模式站名模糊匹配: '{station_name}' → '{match}'")
                            return match
            
            logger.info(f"站名模糊匹配: '{station_name}' → '{matches[0]}'")
            return matches[0]
        
        return station_name

    def fuzzy_search_stations(self, keyword: str) -> List[str]:
        """
        模糊搜索站点名称
        
        Args:
            keyword: 关键词
            
        Returns:
            所有包含关键词的站名列表
        """
        if not keyword:
            return []
        
        if self._station_names is None:
            self._load_station_data()
        
        keyword_lower = keyword.lower()
        matches = []
        
        for name in self._station_names:
            if keyword_lower in name.lower():
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
        """加载站点数据"""
        self._station_map = {}
        self._station_names = []
        
        # 优先从本地JSON加载
        import json
        from pathlib import Path
        
        code_file = Path(__file__).resolve().parent.parent / "data" / "station_codes.json"
        if code_file.exists():
            try:
                with open(code_file, 'r', encoding='utf-8') as f:
                    self._station_map = json.load(f)
                self._station_names = list(self._station_map.keys())
                logger.info(f"从本地加载站点映射: {len(self._station_map)} 个站点")
                return
            except Exception as e:
                logger.warning(f"加载本地站点映射失败: {e}")
        
        # 备用：从12306获取
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
            "永州": "YNQ", "东安东": "DAZ",
            
            # 湖北省
            "武汉": "WHN", "武汉西": "WEF", "汉口": "HKN", "武昌": "WCN",
            
            # 河南省
            "郑州": "ZZF", "郑州东": "ZAF", "郑州西": "XPF",
            "洛阳": "LYF", "洛阳龙门": "LLF",
            
            # 江苏省
            "南京": "NJH", "南京南": "NKH", "南京北": "NJH",
            "苏州": "SZH", "苏州北": "OBH",
            "无锡": "WXH", "常州": "CZH", "镇江": "ZJH",
            
            # 浙江省
            "杭州": "HZH", "杭州东": "HGH", "杭州南": "XHH", "杭州西": "XGH",
            "宁波": "NGH", "宁波东": "GLH",
            "温州": "RZH", "温州南": "VRH", "义乌": "YWG",
            
            # 四川省
            "成都": "CDW", "成都东": "ICW", "成都南": "CNW", "成都西": "CXW",
            "绵阳": "MYW", "乐山": "USW", "宜宾": "YBW",
            
            # 贵州省
            "贵阳": "GIW", "贵阳北": "KQW", "贵阳东": "KEW",
            
            # 云南省
            "昆明": "KMM", "昆明南": "KOM", "昆明西": "KXM",
            "大理": "DKM", "丽江": "LJM",
            
            # 陕西省
            "西安": "XAY", "西安北": "EAO", "西安南": "CAY", "西安西": "EAS",
            "宝鸡": "BJY",
            
            # 甘肃省
            "兰州": "LZJ", "兰州西": "LAJ", "兰州东": "LDJ",
            "敦煌": "DHJ", "嘉峪关": "JXJ",
            
            # 青海省
            "西宁": "XNO", "格尔木": "GRO",
            
            # 西藏
            "拉萨": "LSO",
            
            # 新疆
            "乌鲁木齐": "WMR", "乌鲁木齐南": "WAR",
            "吐鲁番": "TFR", "哈密": "HMR",
            
            # 东北三省
            "哈尔滨": "HRB", "哈尔滨西": "VBB", "哈尔滨东": "VAB",
            "长春": "CCT", "长春西": "CRT",
            "沈阳": "SYT", "沈阳北": "SBT", "沈阳南": "SOD",
            "大连": "DLT", "大连北": "RRT",
            
            # 广西
            "南宁": "NNZ", "南宁东": "NFZ",
            "桂林": "GLZ", "桂林北": "GBZ", "柳州": "LZZ", "北海": "BHZ",
            
            # 福建省
            "福州": "FZS", "福州南": "FYS", "福州北": "FBZ",
            "厦门": "XMS", "厦门北": "XKS", "泉州": "QYS",
            
            # 江西省
            "南昌": "NCG", "南昌西": "NXG",
            "赣州": "GZG", "九江": "JJG",
            
            # 安徽省
            "合肥": "HFH", "合肥南": "ENH", "合肥西": "HTH",
            "黄山": "HKD", "芜湖": "WHH",
            
            # 山东省
            "济南": "JNK", "济南西": "JGK",
            "青岛": "QDK", "青岛北": "QHK",
            "烟台": "YAK", "威海": "WKK",
            
            # 山西省
            "太原": "TYV", "太原南": "TNV", "大同": "DTV",
            
            # 河北省
            "石家庄": "SJP", "石家庄东": "SXP",
            "保定": "BDP", "唐山": "TSP",
            
            # 内蒙古
            "呼和浩特": "HHC", "包头": "BTC",
            
            # 海南省
            "海口": "HMQ", "海口东": "KEQ", "三亚": "SEQ",
            
            # 宁夏
            "银川": "YIJ",
            
            # 香港
            "香港西九龙": "XJA",
        }
        self._station_names = list(self._station_map.keys())
