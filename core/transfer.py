"""
换乘计算模块
"""

from core.planner import TrainRoute

# 统一的换乘枢纽站列表（与planner.py、demo_data.py保持一致）
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


class TransferCalculator:
    """换乘方案计算器"""

    # 同城异站映射
    SAME_CITY_STATIONS = {
        "北京": ["北京", "北京西", "北京南", "北京北", "北京东", "北京丰台"],
        "上海": ["上海", "上海虹桥", "上海南", "上海西"],
        "广州": ["广州", "广州南", "广州东", "广州北", "广州白云"],
        "深圳": ["深圳", "深圳北", "深圳东", "深圳西"],
        "成都": ["成都", "成都东", "成都南", "成都西"],
        "重庆": ["重庆", "重庆西", "重庆北", "重庆南"],
        "武汉": ["武汉", "汉口", "武昌"],
        "长沙": ["长沙", "长沙南"],
        "南京": ["南京", "南京南", "南京西"],
        "杭州": ["杭州", "杭州东", "杭州南"],
        "西安": ["西安", "西安北", "西安南"],
    }

    @classmethod
    def is_same_city(cls, station_a: str, station_b: str) -> bool:
        """判断两个站是否同城"""
        for city, stations in cls.SAME_CITY_STATIONS.items():
            if station_a in stations and station_b in stations:
                return True
        return False

    @classmethod
    def get_transfer_type(cls, arrive_station: str, depart_station: str) -> str:
        """
        判断换乘类型
        Returns:
            'same_station': 同站换乘
            'same_city': 同城异站换乘
            'different_city': 跨城换乘（不太现实）
        """
        if arrive_station == depart_station:
            return "same_station"
        if cls.is_same_city(arrive_station, depart_station):
            return "same_city"
        return "different_city"

    @classmethod
    def min_transfer_time(cls, transfer_type: str) -> int:
        """
        最小换乘时间（分钟）
        """
        times = {
            "same_station": 15,
            "same_city": 40,
            "different_city": 90,
        }
        return times.get(transfer_type, 60)

    @classmethod
    def max_transfer_time(cls, transfer_type: str) -> int:
        """
        最大合理换乘时间（分钟）
        超过这个时间的换乘方案不建议
        """
        times = {
            "same_station": 4 * 60,   # 4小时
            "same_city": 6 * 60,      # 6小时
            "different_city": 12 * 60, # 12小时
        }
        return times.get(transfer_type, 12 * 60)

    @classmethod
    def time_to_minutes(cls, time_str: str) -> int:
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
        except (ValueError, IndexError):
            pass
        return 0

    @classmethod
    def can_connect(cls, leg1: TrainRoute, leg2: TrainRoute) -> tuple[bool, str]:
        """
        判断两程是否可以衔接

        Returns:
            (能否衔接, 换乘类型说明)
        """
        transfer_type = cls.get_transfer_type(leg1.to_station, leg2.from_station)
        min_wait = cls.min_transfer_time(transfer_type)
        max_wait = cls.max_transfer_time(transfer_type)

        # 计算等待时间
        try:
            arrive_mins = cls.time_to_minutes(leg1.arrive_time)
            depart_mins = cls.time_to_minutes(leg2.depart_time)
            wait = depart_mins - arrive_mins
            
            # 处理跨天
            if wait < 0:
                wait += 1440
                reason = f"跨天换乘"
            else:
                reason = f"{'同站' if transfer_type == 'same_station' else '同城异站'}换乘"
            
            # 检查等待时间是否合理
            if wait < min_wait:
                return False, f"{reason}，等待{wait}分钟过短，建议预留{min_wait}分钟"
            
            if wait > max_wait:
                return False, f"{reason}，等待{wait // 60}小时过长，不建议"
            
            return True, f"{reason}，预留{wait}分钟"
            
        except Exception:
            return False, "时间解析失败"

    @classmethod
    def is_cross_day_transfer(cls, leg1: TrainRoute, leg2: TrainRoute) -> bool:
        """
        判断是否为跨天换乘
        
        Args:
            leg1: 第一程
            leg2: 第二程
            
        Returns:
            是否跨天（第二程在次日）
        """
        try:
            arrive_mins = cls.time_to_minutes(leg1.arrive_time)
            depart_mins = cls.time_to_minutes(leg2.depart_time)
            return depart_mins < arrive_mins
        except Exception:
            return False
