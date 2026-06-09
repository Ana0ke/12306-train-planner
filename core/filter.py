"""
多维筛选器 - 按用户偏好排序路线方案
"""

from core.planner import TrainRoute


class RouteFilter:
    """路线筛选和排序"""

    def __init__(self, preference: str = "balanced"):
        """
        Args:
            preference: 偏好类型
                - cheapest: 最便宜
                - fastest: 最快速
                - fewest_transfer: 最少换乘
                - balanced: 性价比最高（默认）
                - comfortable: 最舒适
        """
        self.preference = preference

    def sort(self, routes: list[TrainRoute]) -> list[TrainRoute]:
        """按偏好排序路线"""
        if not routes:
            return routes

        sort_key = {
            "cheapest": self._key_cheapest,
            "fastest": self._key_fastest,
            "fewest_transfer": self._key_fewest_transfer,
            "balanced": self._key_balanced,
            "comfortable": self._key_comfortable,
        }.get(self.preference, self._key_balanced)

        return sorted(routes, key=sort_key)

    def _key_cheapest(self, route: TrainRoute) -> float:
        """按价格升序（越便宜越好）"""
        return route.price_low

    def _key_fastest(self, route: TrainRoute) -> int:
        """按耗时升序（越快越好）"""
        return route.duration_minutes

    def _key_fewest_transfer(self, route: TrainRoute) -> int:
        """按换乘次数升序，同次数按耗时"""
        return (route.transfers * 10000 + route.duration_minutes)

    def _key_balanced(self, route: TrainRoute) -> float:
        """性价比排序（综合评分越高排越前，取负）"""
        return -route.score if route.score > 0 else route.duration_minutes

    def _key_comfortable(self, route: TrainRoute) -> float:
        """舒适度排序：软卧>硬卧>高铁一等>高铁二等>硬座"""
        comfort_order = {
            "swb": 0,    # 商务座最舒适
            "yw": 1,     # 软卧
            "ydz": 2,    # 一等座
            "rw": 3,     # 硬卧
            "edz": 4,    # 二等座
            "yz": 5,     # 硬座最不舒适
        }
        # 判断最高舒适等级
        if route.price_swb:
            return comfort_order["swb"]
        elif route.price_yw:
            return comfort_order["yw"]
        elif route.price_ydz:
            return comfort_order["ydz"]
        elif route.price_rw:
            return comfort_order["rw"]
        elif route.price_edz:
            return comfort_order["edz"]
        else:
            return comfort_order["yz"]
