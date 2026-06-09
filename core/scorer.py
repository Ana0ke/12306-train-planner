"""
方案评分系统 - 综合评估路线方案质量
"""

from core.planner import TrainRoute


class RouteScorer:
    """路线方案综合评分"""

    # 默认权重
    DEFAULT_WEIGHTS = {
        "price": 0.30,       # 价格
        "time": 0.30,        # 时间
        "transfer": 0.25,    # 换乘
        "comfort": 0.15,     # 舒适度
    }

    # 偏好权重调整
    PREFERENCE_WEIGHTS = {
        "cheapest": {"price": 0.50, "time": 0.15, "transfer": 0.20, "comfort": 0.15},
        "fastest": {"price": 0.15, "time": 0.50, "transfer": 0.20, "comfort": 0.15},
        "fewest_transfer": {"price": 0.15, "time": 0.20, "transfer": 0.50, "comfort": 0.15},
        "balanced": {"price": 0.30, "time": 0.30, "transfer": 0.25, "comfort": 0.15},
        "comfortable": {"price": 0.10, "time": 0.20, "transfer": 0.20, "comfort": 0.50},
    }

    @classmethod
    def score_all(
        cls,
        routes: list[TrainRoute],
        preference: str = "balanced",
    ) -> list[TrainRoute]:
        """批量评分"""
        if not routes:
            return routes

        # 计算基准值
        prices = [r.price_low for r in routes if r.price_low > 0]
        durations = [r.duration_minutes for r in routes]

        min_price = min(prices) if prices else 0
        max_price = max(prices) if prices else 1
        min_duration = min(durations) if durations else 0
        max_duration = max(durations) if durations else 1

        # 避免除零
        price_range = max(max_price - min_price, 1)
        duration_range = max(max_duration - min_duration, 1)

        # 获取权重
        weights = cls.PREFERENCE_WEIGHTS.get(preference, cls.DEFAULT_WEIGHTS)

        # 逐个评分
        for route in routes:
            price_score = 1.0 - (route.price_low - min_price) / price_range if route.price_low else 0.5
            time_score = 1.0 - (route.duration_minutes - min_duration) / duration_range
            transfer_score = 1.0 - (route.transfers * 0.4)
            transfer_score = max(transfer_score, 0)
            comfort_score = cls._comfort_score(route)

            route.score = (
                weights["price"] * price_score
                + weights["time"] * time_score
                + weights["transfer"] * transfer_score
                + weights["comfort"] * comfort_score
            ) * 100

        return routes

    @staticmethod
    def _comfort_score(route: TrainRoute) -> float:
        """舒适度评分 0-1"""
        if route.price_swb:
            return 1.0     # 商务座
        elif route.price_yw:
            return 0.85    # 软卧
        elif route.price_ydz:
            return 0.75    # 一等座
        elif route.price_rw:
            return 0.60    # 硬卧
        elif route.price_edz:
            return 0.50    # 二等座
        elif route.price_yz:
            return 0.20    # 硬座
        return 0.3
