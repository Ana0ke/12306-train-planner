"""
路线规划引擎 - 核心模块
负责查询直达和换乘路线
支持Demo模式换乘查询
"""

from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
from api.client_12306 import Client12306
from api.cache import QueryCache
from loguru import logger

# 统一的换乘枢纽站列表（与demo_data.py、transfer.py保持一致）
TRANSFER_HUBS = [
    # 华北
    "北京", "北京西", "北京南",
    # 华东
    "上海", "上海虹桥",
    # 华南
    "广州", "广州南",
    "深圳", "深圳北",
    # 华中
    "武汉", "汉口", "武昌",
    "长沙", "长沙南",
    "郑州", "郑州东",
    # 西南
    "成都", "成都东",
    "重庆", "重庆北", "重庆西",
    # 西北
    "西安", "西安北",
    # 其他重要枢纽
    "南京", "南京南",
    "杭州", "杭州东",
    "合肥",
    "贵阳", "贵阳北",
    "昆明", "昆明南",
    "南昌", "南昌西",
    "济南",
    "青岛", "青岛北",
    "沈阳", "沈阳北",
    "大连",
    "哈尔滨", "哈尔滨西",
    "长春", "长春西",
    "福州", "福州南",
    "厦门", "厦门北",
    "兰州", "兰州西",
    "西宁",
    "太原", "太原南",
    "石家庄",
    "南宁",
    "海口", "海口东",
    "乌鲁木齐", "乌鲁木齐南",
]


@dataclass
class TrainRoute:
    """一条火车路线方案"""

    train_no: str                    # 车次号（如 G6075）
    from_station: str                # 出发站
    to_station: str                  # 到达站
    depart_time: str                 # 出发时间
    arrive_time: str                 # 到达时间
    duration: str                    # 历时
    train_type: str                  # 车型（高铁/动车/普速）
    transfers: int = 0               # 换乘次数
    transfer_details: list = field(default_factory=list)  # 换乘详情

    # 票价（元）
    price_yz: Optional[float] = None   # 硬座
    price_rw: Optional[float] = None  # 硬卧
    price_yw: Optional[float] = None  # 软卧
    price_edz: Optional[float] = None # 二等座
    price_ydz: Optional[float] = None # 一等座
    price_swb: Optional[float] = None  # 商务座

    # 评分
    score: float = 0.0

    # 数据来源标记
    is_realtime: bool = False

    @property
    def price_low(self) -> float:
        """最低票价"""
        prices = [p for p in [self.price_yz, self.price_rw, self.price_edz] if p]
        return min(prices) if prices else 0

    @property
    def price_high(self) -> float:
        """最高票价"""
        prices = [p for p in [self.price_swb, self.price_yw, self.price_ydz] if p]
        return max(prices) if prices else self.price_low

    @property
    def duration_minutes(self) -> int:
        """历时转分钟数"""
        try:
            parts = self.duration.split(":")
            if len(parts) == 2:
                return int(parts[0]) * 60 + int(parts[1])
        except (ValueError, IndexError):
            pass
        return 9999  # 解析失败返回大值


class RoutePlanner:
    """路线规划引擎"""

    def __init__(self):
        self.client = Client12306()
        self.cache = QueryCache()

    def search(
        self,
        from_station: str,
        to_station: str,
        travel_date: str,
    ) -> list[TrainRoute]:
        """查询直达路线"""
        cache_key = f"direct:{from_station}:{to_station}:{travel_date}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached

        try:
            raw_routes = self.client.query(
                from_station=from_station,
                to_station=to_station,
                date=travel_date,
            )
            routes = [self._parse_route(r) for r in raw_routes]
            self.cache.set(cache_key, routes, ttl=300)
            return routes
        except Exception as e:
            logger.error(f"查询直达路线失败: {e}")
            return []

    def search_with_transfer(
        self,
        from_station: str,
        to_station: str,
        travel_date: str,
        max_transfers: int = 1,
    ) -> list[TrainRoute]:
        """
        查询换乘路线（目前支持1次换乘）
        
        Demo模式特殊处理：
        - 当直达路线不存在时，自动尝试换乘方案
        - 换乘站点使用 Demo 数据中已有的大站中转
        """
        cache_key = f"transfer:{from_station}:{to_station}:{travel_date}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached

        # 首先尝试直达
        direct_routes = self.search(from_station, to_station, travel_date)
        if direct_routes:
            logger.info(f"直达路线找到: {from_station}→{to_station}, {len(direct_routes)}条")
            return direct_routes

        # Demo模式特殊处理：尝试两段式换乘
        if self.client.demo_mode:
            demo_transfer = self._demo_transfer_search(from_station, to_station, travel_date)
            if demo_transfer:
                self.cache.set(cache_key, demo_transfer, ttl=300)
                return demo_transfer

        # 获取可中转站点
        transfer_stations = self._get_transfer_stations(from_station, to_station)
        logger.info(f"尝试换乘站点: {transfer_stations[:5]}...")

        combined_routes = []
        for mid_station in transfer_stations:
            # 跳过相同站
            if mid_station == from_station or mid_station == to_station:
                continue
                
            try:
                # 查第一程
                leg1_list = self.search(from_station, mid_station, travel_date)
                if not leg1_list:
                    continue
                    
                # 查第二程
                leg2_list = self.search(mid_station, to_station, travel_date)
                if not leg2_list:
                    continue

                # 组合换乘方案
                for leg1 in leg1_list:
                    for leg2 in leg2_list:
                        # 检查时间是否衔接（第二程出发要在第一程到达后至少min_wait分钟）
                        if self._can_transfer(leg1, leg2, min_wait=15):
                            combined = self._combine_routes(leg1, leg2)
                            combined_routes.append(combined)
            except Exception as e:
                logger.warning(f"查询 {from_station}→{mid_station}→{to_station} 失败: {e}")
                continue

        # 按总耗时排序
        combined_routes.sort(key=lambda r: r.duration_minutes)
        self.cache.set(cache_key, combined_routes[:20], ttl=300)
        return combined_routes[:20]

    def _demo_transfer_search(
        self,
        from_station: str,
        to_station: str,
        travel_date: str,
    ) -> list[TrainRoute]:
        """
        Demo模式专用换乘搜索
        
        Demo数据中的换乘路线：
        - 通过长沙南/广州南/武汉/杭州东等枢纽站中转
        
        Args:
            from_station: 出发站
            to_station: 到达站
            travel_date: 旅行日期
            
        Returns:
            换乘方案列表
        """
        from api.demo_data import get_demo_transfer_routes
        
        # 尝试获取换乘路线
        leg1_data, leg2_data = get_demo_transfer_routes(from_station, to_station)
        
        if not leg1_data or not leg2_data:
            return []
        
        # 解析为 TrainRoute
        leg1_list = [self._parse_route(r) for r in leg1_data]
        leg2_list = [self._parse_route(r) for r in leg2_data]
        
        combined_routes = []
        for leg1 in leg1_list:
            for leg2 in leg2_list:
                # Demo模式：假设换乘等待时间足够（30分钟）
                if self._can_transfer(leg1, leg2, min_wait=10):
                    combined = self._combine_routes(leg1, leg2)
                    combined_routes.append(combined)
        
        logger.info(f"Demo换乘找到 {len(combined_routes)} 条方案")
        return combined_routes

    def _parse_route(self, raw: dict) -> TrainRoute:
        """解析原始数据为TrainRoute对象"""
        return TrainRoute(
            train_no=raw.get("train_no", ""),
            from_station=raw.get("from_station", ""),
            to_station=raw.get("to_station", ""),
            depart_time=raw.get("depart_time", ""),
            arrive_time=raw.get("arrive_time", ""),
            duration=raw.get("duration", ""),
            train_type=raw.get("train_type", ""),
            price_yz=raw.get("price_yz"),
            price_rw=raw.get("price_rw"),
            price_yw=raw.get("price_yw"),
            price_edz=raw.get("price_edz"),
            price_ydz=raw.get("price_ydz"),
            price_swb=raw.get("price_swb"),
            is_realtime=raw.get("is_realtime", False),
        )

    def _time_to_minutes(self, time_str: str) -> int:
        """
        将时间字符串（格式如 "09:30"）转换为当日分钟数
        
        Args:
            time_str: 时间字符串，格式为 HH:MM
            
        Returns:
            当日分钟数（0-1439）
        """
        try:
            parts = time_str.split(":")
            if len(parts) == 2:
                hours = int(parts[0])
                minutes = int(parts[1])
                return hours * 60 + minutes
        except (ValueError, IndexError) as e:
            logger.warning(f"解析时间失败: {time_str}, {e}")
        return 0

    def _combine_routes(self, leg1: TrainRoute, leg2: TrainRoute) -> TrainRoute:
        """组合两程路线为一个换乘方案"""
        total_price_yz = (leg1.price_yz or 0) + (leg2.price_yz or 0)
        total_price_rw = (leg1.price_rw or 0) + (leg2.price_rw or 0)
        total_price_edz = (leg1.price_edz or 0) + (leg2.price_edz or 0)
        total_price_ydz = (leg1.price_ydz or 0) + (leg2.price_ydz or 0)
        total_price_yw = (leg1.price_yw or 0) + (leg2.price_yw or 0)
        total_price_swb = (leg1.price_swb or 0) + (leg2.price_swb or 0)

        transfer_desc = (
            f"{leg1.train_no} {leg1.from_station}→{leg1.to_station} "
            f"({leg1.depart_time}-{leg1.arrive_time})，"
            f"换乘 {leg2.train_no} {leg2.from_station}→{leg2.to_station} "
            f"({leg2.depart_time}-{leg2.arrive_time})"
        )

        # 计算总历时：第一程出发到第二程到达
        total_duration_minutes = self._calculate_total_duration(
            leg1.depart_time, leg1.arrive_time,
            leg2.depart_time, leg2.arrive_time
        )
        hours = total_duration_minutes // 60
        mins = total_duration_minutes % 60
        total_duration = f"{hours:02d}:{mins:02d}"

        return TrainRoute(
            train_no=f"{leg1.train_no}+{leg2.train_no}",
            from_station=leg1.from_station,
            to_station=leg2.to_station,
            depart_time=leg1.depart_time,
            arrive_time=leg2.arrive_time,
            duration=total_duration,
            train_type="换乘",
            transfers=1,
            transfer_details=[transfer_desc],
            price_yz=total_price_yz if total_price_yz else None,
            price_rw=total_price_rw if total_price_rw else None,
            price_yw=total_price_yw if total_price_yw else None,
            price_edz=total_price_edz if total_price_edz else None,
            price_ydz=total_price_ydz if total_price_ydz else None,
            price_swb=total_price_swb if total_price_swb else None,
            is_realtime=leg1.is_realtime or leg2.is_realtime,
        )

    def _calculate_total_duration(
        self, 
        leg1_depart: str, 
        leg1_arrive: str,
        leg2_depart: str, 
        leg2_arrive: str
    ) -> int:
        """
        计算换乘方案的总历时（分钟）
        从第一程出发到第二程到达
        
        Args:
            leg1_depart: 第一程出发时间
            leg1_arrive: 第一程到达时间  
            leg2_depart: 第二程出发时间
            leg2_arrive: 第二程到达时间
            
        Returns:
            总历时分钟数
        """
        try:
            # 第一程历时
            leg1_minutes = self._time_to_minutes(leg1_arrive) - self._time_to_minutes(leg1_depart)
            if leg1_minutes < 0:
                leg1_minutes += 1440  # 跨天修正
            
            # 等待时间
            wait_minutes = self._can_transfer_minutes(leg1_arrive, leg2_depart)
            
            # 第二程历时
            leg2_minutes = self._time_to_minutes(leg2_arrive) - self._time_to_minutes(leg2_depart)
            if leg2_minutes < 0:
                leg2_minutes += 1440  # 跨天修正
            
            return leg1_minutes + wait_minutes + leg2_minutes
        except Exception as e:
            logger.warning(f"计算总历时失败: {e}")
            return 9999

    def _can_transfer_minutes(self, arrive_time: str, depart_time: str) -> int:
        """
        计算等待时间（分钟），处理跨天情况
        
        Args:
            arrive_time: 到达时间（格式 "HH:MM"）
            depart_time: 出发时间（格式 "HH:MM"）
            
        Returns:
            等待分钟数（可能是负数，如果出发在到达之前）
        """
        arrive_mins = self._time_to_minutes(arrive_time)
        depart_mins = self._time_to_minutes(depart_time)
        
        wait = depart_mins - arrive_mins
        if wait < 0:
            # 跨天情况：第二程在次日出发
            wait += 1440
            
        return wait

    def _can_transfer(self, leg1: TrainRoute, leg2: TrainRoute, min_wait: int = 15) -> bool:
        """
        检查两程是否可以衔接
        
        规则：
        1. 第二程出发时间 >= 第一程到达时间 + min_wait分钟
        2. 需要处理跨天情况（如第一程23:50到达，第二程00:30出发）
        3. 如果等待时间超过12小时，不建议换乘（太久不合理）
        
        Args:
            leg1: 第一程路线
            leg2: 第二程路线
            min_wait: 最小等待时间（分钟）
            
        Returns:
            是否可以衔接
        """
        try:
            wait_minutes = self._can_transfer_minutes(leg1.arrive_time, leg2.depart_time)
            
            # 判断是否跨天：如果第二程出发时间 < 第一程到达时间，说明是次日发车
            arrive_mins = self._time_to_minutes(leg1.arrive_time)
            depart_mins = self._time_to_minutes(leg2.depart_time)
            is_cross_day = depart_mins < arrive_mins
            
            # 如果跨天，等待时间已经+1440（24小时）
            # 检查是否满足最小等待时间
            if wait_minutes < min_wait:
                logger.debug(
                    f"换乘不可行: {leg1.arrive_time}→{leg2.depart_time}, "
                    f"等待{wait_minutes}分钟 < {min_wait}分钟"
                )
                return False
            
            # 检查等待时间是否过长（超过12小时不合理）
            max_reasonable_wait = 12 * 60  # 12小时
            if wait_minutes > max_reasonable_wait:
                logger.debug(
                    f"换乘等待时间过长: {leg1.arrive_time}→{leg2.depart_time}, "
                    f"等待{wait_minutes}分钟 > {max_reasonable_wait}分钟（{('跨天' if is_cross_day else '同日')}）"
                )
                return False
                
            return True
            
        except Exception as e:
            logger.warning(f"检查换乘衔接失败: {e}")
            return False

    def _get_transfer_stations(self, from_station: str, to_station: str) -> list[str]:
        """
        获取可能的换乘站点列表
        
        Demo模式特殊处理：优先使用有Demo数据的中转站
        
        Args:
            from_station: 出发站
            to_station: 到达站
            
        Returns:
            可能的换乘站点列表（按优先级排序）
        """
        # 过滤掉起终点
        return [s for s in TRANSFER_HUBS if s != from_station and s != to_station]
