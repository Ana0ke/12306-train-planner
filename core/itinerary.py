"""
行程数据模型 - 定义AI生成的旅行计划数据结构
"""

from dataclasses import dataclass, field, asdict
from typing import Optional
import json
from loguru import logger


@dataclass
class Activity:
    """单个活动/景点"""
    time: str              # 时间，如 "09:00-12:00"
    name: str               # 活动名称，如 "布达拉宫参观"
    desc: str               # 详细描述
    tip: str = ""           # 小贴士


@dataclass
class DayPlan:
    """每日行程"""
    day_number: int                    # 第几天（1, 2, 3...）
    theme: str                          # 今日主题，如 "初识拉萨"
    activities: list[Activity] = field(default_factory=list)  # 活动列表
    food: list[str] = field(default_factory=list)  # 推荐美食
    accommodation: str = ""             # 住宿建议


@dataclass
class BudgetBreakdown:
    """费用明细"""
    transport: float = 0.0      # 交通费（含火车票）
    accommodation: float = 0.0  # 住宿费
    food: float = 0.0           # 餐饮费
    tickets: float = 0.0        # 门票/景点费
    total: float = 0.0          # 总费用

    def to_dict(self) -> dict:
        """转为字典"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "BudgetBreakdown":
        """从字典创建"""
        return cls(
            transport=data.get("transport", 0),
            accommodation=data.get("accommodation", 0),
            food=data.get("food", 0),
            tickets=data.get("tickets", 0),
            total=data.get("total", 0),
        )


@dataclass
class TrainRouteInfo:
    """火车路线信息（用于AI规划）"""
    train_no: str              # 车次号
    from_station: str          # 出发站
    to_station: str            # 到达站
    depart_time: str           # 出发时间
    arrive_time: str           # 到达时间
    duration: str              # 历时
    train_type: str            # 车型
    transfers: int = 0         # 换乘次数
    price_range: str = ""      # 票价区间，如 "硬座¥200-300/硬卧¥400-500"
    tips: str = ""             # 购票/乘坐提示


@dataclass
class TripPlan:
    """完整旅行计划"""
    title: str                 # 计划标题，如 "拉萨5日深度游"
    summary: str               # 简要概述
    destination: str          # 目的地
    days_count: int            # 天数
    days: list[DayPlan] = field(default_factory=list)  # 每日行程
    train_route: Optional[TrainRouteInfo] = None  # 推荐火车路线
    budget_breakdown: BudgetBreakdown = field(default_factory=BudgetBreakdown)  # 费用预估
    packing_list: list[str] = field(default_factory=list)  # 装备清单
    tips: list[str] = field(default_factory=list)  # 出行Tips
    travel_date: Optional[str] = None  # 出行日期，格式YYYY-MM-DD
    season_info: Optional[dict] = None  # 季节信息，包含season、weather、temp、clothes、tips

    def to_dict(self) -> dict:
        """转为字典（用于JSON序列化）"""
        result = {
            "title": self.title,
            "summary": self.summary,
            "destination": self.destination,
            "days_count": self.days_count,
            "days": [
                {
                    "day_number": d.day_number,
                    "theme": d.theme,
                    "activities": [
                        {
                            "time": a.time,
                            "name": a.name,
                            "desc": a.desc,
                            "tip": a.tip,
                        }
                        for a in d.activities
                    ],
                    "food": d.food,
                    "accommodation": d.accommodation,
                }
                for d in self.days
            ],
            "budget_breakdown": self.budget_breakdown.to_dict(),
            "packing_list": self.packing_list,
            "tips": self.tips,
            "travel_date": self.travel_date,
            "season_info": self.season_info,
        }
        if self.train_route:
            result["train_route"] = asdict(self.train_route)
        return result

    def to_json(self) -> str:
        """转为JSON字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    @classmethod
    def from_dict(cls, data: dict) -> "TripPlan":
        """从字典创建"""
        days = []
        for d in data.get("days", []):
            activities = [
                Activity(
                    time=a.get("time", ""),
                    name=a.get("name", ""),
                    desc=a.get("desc", ""),
                    tip=a.get("tip", ""),
                )
                for a in d.get("activities", [])
            ]
            days.append(DayPlan(
                day_number=d.get("day_number", 0),
                theme=d.get("theme", ""),
                activities=activities,
                food=d.get("food", []),
                accommodation=d.get("accommodation", ""),
            ))

        train_route = None
        if "train_route" in data and data["train_route"]:
            tr = data["train_route"]
            train_route = TrainRouteInfo(
                train_no=tr.get("train_no", ""),
                from_station=tr.get("from_station", ""),
                to_station=tr.get("to_station", ""),
                depart_time=tr.get("depart_time", ""),
                arrive_time=tr.get("arrive_time", ""),
                duration=tr.get("duration", ""),
                train_type=tr.get("train_type", ""),
                transfers=tr.get("transfers", 0),
                price_range=tr.get("price_range", ""),
                tips=tr.get("tips", ""),
            )

        budget = BudgetBreakdown.from_dict(data.get("budget_breakdown", {}))

        return cls(
            title=data.get("title", ""),
            summary=data.get("summary", ""),
            destination=data.get("destination", ""),
            days_count=data.get("days_count", 0),
            days=days,
            train_route=train_route,
            budget_breakdown=budget,
            packing_list=data.get("packing_list", []),
            tips=data.get("tips", []),
            travel_date=data.get("travel_date"),
            season_info=data.get("season_info"),
        )

    @classmethod
    def from_json(cls, json_str: str) -> "TripPlan":
        """从JSON字符串创建"""
        try:
            data = json.loads(json_str)
            return cls.from_dict(data)
        except json.JSONDecodeError as e:
            logger.error(f"JSON解析失败: {e}")
            raise ValueError(f"无效的JSON格式: {e}")

    def validate(self) -> tuple[bool, list[str]]:
        """
        验证旅行计划的有效性

        Returns:
            (is_valid, error_messages)
        """
        errors = []

        # 检查天数匹配
        if len(self.days) != self.days_count:
            errors.append(f"行程天数不匹配：声明{self.days_count}天，实际{len(self.days)}天")

        # 检查每日行程不为空
        for day in self.days:
            if not day.activities:
                errors.append(f"第{day.day_number}天没有安排任何活动")
            if not day.theme:
                errors.append(f"第{day.day_number}天缺少主题")

        # 检查预算合理性（简单校验）
        if self.budget_breakdown.total > 0:
            calculated_total = (
                self.budget_breakdown.transport +
                self.budget_breakdown.accommodation +
                self.budget_breakdown.food +
                self.budget_breakdown.tickets
            )
            # 允许10%的误差
            if abs(calculated_total - self.budget_breakdown.total) > calculated_total * 0.1:
                errors.append(f"预算明细之和与总额不符")

        return len(errors) == 0, errors

    def get_daily_summary(self) -> list[dict]:
        """
        获取每日行程摘要

        Returns:
            每日摘要列表，包含时间线、活动数、美食数
        """
        summary = []
        for day in self.days:
            times = [a.time for a in day.activities if a.time]
            summary.append({
                "day": day.day_number,
                "theme": day.theme,
                "activity_count": len(day.activities),
                "time_range": f"{times[0].split('-')[0] if times else '?'} - {times[-1].split('-')[-1] if times else '?'}",
                "food_count": len(day.food),
            })
        return summary


def create_sample_trip_plan() -> TripPlan:
    """
    创建一个示例旅行计划（用于测试）

    Returns:
        示例TripPlan对象
    """
    return TripPlan(
        title="拉萨5日深度游",
        summary="从长沙南出发，乘坐Z264次列车穿越青藏高原，感受世界屋脊的壮美与神秘。这是一次洗涤心灵的旅程，适合喜欢慢旅行、摄影和文化探索的朋友。",
        destination="拉萨",
        days_count=5,
        days=[
            DayPlan(
                day_number=1,
                theme="启程 · 天路之旅",
                activities=[
                    Activity(
                        time="08:00-09:00",
                        name="长沙南站出发",
                        desc="提前1小时到站，取票安检，准备登车",
                        tip="记得带身份证，刷身份证进站"
                    ),
                    Activity(
                        time="09:00-09:30",
                        name="火车上的上午",
                        desc="欣赏沿途风景，从湖南的山水逐渐过渡到云贵高原",
                        tip="可以开始服用红景天，预防高原反应"
                    ),
                ],
                food=["火车餐", "自带零食"],
                accommodation="Z264次列车硬卧",
            ),
            DayPlan(
                day_number=2,
                theme="穿越可可西里",
                activities=[
                    Activity(
                        time="全天",
                        name="青藏铁路精华段",
                        desc="翻越唐古拉山，穿越可可西里无人区，有机会看到藏羚羊",
                        tip="海拔最高处超过5000米，多喝水少走动"
                    ),
                ],
                food=["火车餐", "巧克力补充能量"],
                accommodation="Z264次列车软卧",
            ),
        ],
        train_route=TrainRouteInfo(
            train_no="Z264",
            from_station="长沙南",
            to_station="拉萨",
            depart_time="08:30",
            arrive_time="11:50",
            duration="51:20",
            train_type="直达特快",
            transfers=0,
            price_range="硬座¥341/硬卧¥682/软卧¥1084",
            tips="建议购买硬卧，舒适度较好。记得带润唇膏和防晒霜！"
        ),
        budget_breakdown=BudgetBreakdown(
            transport=1200,
            accommodation=600,
            food=400,
            tickets=300,
            total=2500,
        ),
        packing_list=[
            "身份证、学生证（景区可能有优惠）",
            "红景天（进藏前3-5天开始服用）",
            "防晒霜SPF50+",
            "润唇膏",
            "墨镜",
            "厚外套（即使是夏天也要带）",
            "常用药品（感冒药、止泻药、创可贴）",
            "充电宝",
            "洗漱用品",
        ],
        tips=[
            "第一天到拉萨多休息，不要洗澡",
            "布达拉宫需提前1天预约",
            "尊重当地宗教习俗",
        ],
    )
