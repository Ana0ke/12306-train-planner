"""
换乘计算模块
"""

from core.planner import TrainRoute


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

    # 常用换乘枢纽
    TRANSFER_HUBS = [
        "武汉", "长沙南", "郑州东", "广州南", "北京西",
        "上海虹桥", "南京南", "杭州东", "成都东", "西安北",
        "贵阳北", "南宁东", "衡阳东", "株洲西",
    ]

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
    def can_connect(cls, leg1: TrainRoute, leg2: TrainRoute) -> tuple[bool, str]:
        """
        判断两程是否可以衔接

        Returns:
            (能否衔接, 换乘类型说明)
        """
        transfer_type = cls.get_transfer_type(leg1.to_station, leg2.from_station)
        min_wait = cls.min_transfer_time(transfer_type)

        # TODO: 解析具体时间计算等车时长
        # MVP阶段简化处理
        if transfer_type == "different_city":
            return False, "跨城换乘不可行"

        return True, f"{'同站' if transfer_type == 'same_station' else '同城异站'}换乘，建议预留{min_wait}分钟"
