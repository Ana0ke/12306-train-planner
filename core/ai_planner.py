"""
AI旅行规划引擎 - 基于LLM生成个性化旅行方案
支持多城市联程规划和季节信息注入
"""

import json
import re
from typing import Optional, Union
from pathlib import Path

from loguru import logger

from api.llm_client import get_llm_client, LLMNotConfiguredError, LLMRequestError
from core.itinerary import TripPlan, DayPlan, Activity, BudgetBreakdown, TrainRouteInfo
from core.season_engine import get_season_engine, get_holiday_alert


class AIPlanner:
    """
    AI旅行规划引擎

    功能：
    - 根据目的地、天数、预算生成完整旅行方案
    - 结合城市攻略数据和火车路线信息
    - 支持对话式调整方案
    """

    def __init__(self):
        self.llm_client = get_llm_client()
        self.city_guides = self._load_city_guides()

    def _load_city_guides(self) -> dict:
        """加载城市攻略数据"""
        data_path = Path(__file__).parent.parent / "data" / "city_guide.json"
        try:
            with open(data_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                # 转为字典，方便查询
                return {guide["city"]: guide for guide in data.get("city_guides", [])}
        except Exception as e:
            logger.error(f"加载城市攻略失败: {e}")
            return {}

    def _get_city_guide(self, city: str) -> Optional[dict]:
        """
        获取城市攻略

        Args:
            city: 城市名称

        Returns:
            城市攻略字典，未找到返回None
        """
        # 精确匹配
        if city in self.city_guides:
            return self.city_guides[city]

        # 模糊匹配（包含关系）
        for guide_city, guide in self.city_guides.items():
            if city in guide_city or guide_city in city:
                return guide

        return None

    def plan_trip(
        self,
        destination: str,
        days: int,
        budget: Optional[float] = None,
        preferences: Optional[list[str]] = None,
        train_info: Optional[dict] = None,
        travel_date: Optional[str] = None,
    ) -> TripPlan:
        """
        生成旅行计划

        Args:
            destination: 目的地（支持多城市，如"成都+九寨沟"、"拉萨→纳木错"）
            days: 天数
            budget: 预算（元），可选
            preferences: 偏好标签列表，如 ["美食优先", "文化历史"]
            train_info: 火车路线信息，可选
            travel_date: 出行日期，格式YYYY-MM-DD，可选

        Returns:
            TripPlan对象

        Raises:
            LLMNotConfiguredError: LLM未配置
            LLMRequestError: LLM请求失败
        """
        # 检查是否为多目的地
        destinations = self._parse_multi_destination(destination)

        if len(destinations) > 1:
            # 多城市联程规划
            logger.info(f"检测到多目的地: {destinations}")
            return self._plan_multi_city_trip(
                destinations=destinations,
                total_days=days,
                budget=budget,
                preferences=preferences or [],
                travel_date=travel_date,
            )

        # 单目的地规划
        destination = destinations[0] if destinations else destination

        # 构建系统提示
        system_prompt = self._build_system_prompt()

        # 构建用户提示（注入季节信息）
        user_prompt = self._build_user_prompt(
            destination=destination,
            days=days,
            budget=budget,
            preferences=preferences or [],
            train_info=train_info,
            travel_date=travel_date,
        )

        logger.info(f"开始生成{destination}{days}日游计划...")

        # 获取季节信息
        season_info = None
        if travel_date:
            try:
                month = int(travel_date.split("-")[1])
                season_info = get_season_engine().get_season_info(destination, month)
            except Exception as e:
                logger.warning(f"获取季节信息失败: {e}")

        try:
            # 调用LLM
            response = self.llm_client.chat(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.7,
                max_tokens=4096,
            )

            # 解析响应
            trip_plan = self._parse_llm_response(response, destination, days, train_info)
            # 添加季节信息
            trip_plan.travel_date = travel_date
            trip_plan.season_info = season_info
            return trip_plan

        except (LLMNotConfiguredError, LLMRequestError):
            # LLM不可用，返回静态推荐
            logger.warning("LLM不可用，返回基于静态数据的推荐")
            plan = self._fallback_plan(destination, days, budget, preferences, train_info)
            plan.travel_date = travel_date
            plan.season_info = season_info
            return plan

    def _parse_multi_destination(self, destination: str) -> list[str]:
        """
        解析多目的地输入

        Args:
            destination: 目的地字符串，如"成都+九寨沟"、"拉萨→纳木错"

        Returns:
            目的地列表
        """
        # 定义分隔符
        separators = ['+', '→', '->', '/', '，', ',']

        result = destination
        for sep in separators:
            if sep in result:
                # 分割并清理
                parts = [p.strip() for p in result.split(sep)]
                # 过滤空字符串
                return [p for p in parts if p]

        # 单目的地
        return [destination.strip()]

    def _plan_multi_city_trip(
        self,
        destinations: list[str],
        total_days: int,
        budget: Optional[float],
        preferences: list[str],
        travel_date: Optional[str],
    ) -> TripPlan:
        """
        多城市联程规划

        Args:
            destinations: 目的地列表
            total_days: 总天数
            budget: 预算
            preferences: 偏好
            travel_date: 出行日期

        Returns:
            多城市旅行计划
        """
        num_cities = len(destinations)

        # 分配天数（第一个城市多半天，最后一个城市少半天）
        if num_cities == 2:
            days_list = [total_days // 2 + 1, total_days // 2]
        else:
            base_days = total_days // num_cities
            remainder = total_days % num_cities
            days_list = [base_days + (1 if i < remainder else 0) for i in range(num_cities)]

        logger.info(f"多城市天数分配: {dict(zip(destinations, days_list))}")

        # 获取季节信息
        season_info = None
        if travel_date:
            try:
                month = int(travel_date.split("-")[1])
                # 使用第一个目的地作为季节参考
                season_info = get_season_engine().get_season_info(destinations[0], month)
            except Exception:
                pass

        # 获取节假日提醒
        holiday_info = None
        if travel_date:
            try:
                from datetime import datetime
                date_obj = datetime.strptime(travel_date, "%Y-%m-%d").date()
                holiday_info = get_holiday_alert(date_obj)
            except Exception:
                pass

        # 构建标题
        if num_cities <= 3:
            title = f"{'→'.join(destinations)}{total_days}日游"
        else:
            title = f"{destinations[0]}等{num_cities}地{total_days}日游"

        # 构建概述
        summary = f"一次玩转{num_cities}个城市，{'、'.join(destinations)}。"

        # 构建每日行程（模拟多城市路线）
        all_days = []
        current_day = 1

        for i, city in enumerate(destinations):
            city_days = days_list[i]

            # 获取城市攻略
            city_guide = self._get_city_guide(city)
            highlights = city_guide.get("highlights", []) if city_guide else []
            food = city_guide.get("food", []) if city_guide else []

            # 为每个城市生成行程
            for d in range(1, city_days + 1):
                # 判断是到达日还是游览日
                if d == 1 and i > 0:
                    # 到达日
                    theme = f"抵达{city}"
                    activities = [
                        Activity(
                            time="上午/下午",
                            name=f"前往{city}",
                            desc=f"从{destinations[i-1]}出发前往{city}，根据交通方式安排行程。",
                            tip="记得提前查好交通信息"
                        ),
                        Activity(
                            time="傍晚",
                            name="入住休息",
                            desc=f"抵达{city}后入住酒店，休整一下。",
                            tip="不要安排太紧凑的行程"
                        ),
                    ]
                    day_food = ["当地美食"]
                elif d == city_days and i < num_cities - 1:
                    # 离开日（如果是最后一个城市则不是）
                    theme = f"告别{city}"
                    activities = [
                        Activity(
                            time="上午",
                            name="最后游览",
                            desc=f"抓紧时间再看看{city}的景点。",
                            tip="注意退房时间"
                        ),
                    ]
                    day_food = food[:2] if food else ["当地美食"]
                else:
                    # 正常游览日
                    if highlights:
                        theme = f"深度游{city}"
                        activities = [
                            Activity(
                                time="上午",
                                name=highlights[0] if len(highlights) > 0 else f"{city}景点",
                                desc=f"游览{highlights[0] if len(highlights) > 0 else city}，感受当地特色。",
                                tip="建议请导游讲解"
                            ),
                            Activity(
                                time="下午",
                                name=highlights[1] if len(highlights) > 1 else f"{city}特色体验",
                                desc=f"继续探索{highlights[1] if len(highlights) > 1 else city}。",
                                tip="可以尝试当地特色活动"
                            ),
                        ]
                    else:
                        theme = f"探索{city}"
                        activities = [
                            Activity(
                                time="全天",
                                name=f"{city}自由行",
                                desc=f"全天在{city}自由活动。",
                                tip="根据个人兴趣安排"
                            ),
                        ]
                    day_food = food[:3] if food else ["当地特色美食"]

                all_days.append(DayPlan(
                    day_number=current_day,
                    theme=theme,
                    activities=activities,
                    food=day_food,
                    accommodation=f"{city}酒店" if d != city_days or i < num_cities - 1 else "无（返程日）",
                ))
                current_day += 1

        # 构建Tips
        tips = [
            f"全程{total_days}天，游览{num_cities}个城市",
            "城市间交通建议提前预订",
            "注意保管好个人财物",
        ]

        # 添加节假日提醒
        if holiday_info and holiday_info.get("is_holiday"):
            tips.insert(0, holiday_info.get("alert", ""))

        # 预算估算
        per_city_budget = (budget or 2000) / num_cities
        budget_breakdown = BudgetBreakdown(
            transport=budget * 0.4 if budget else per_city_budget * 0.4 * num_cities,
            accommodation=per_city_budget * 0.3 * num_cities if budget else 100 * total_days,
            food=per_city_budget * 0.2 * num_cities if budget else 80 * total_days,
            tickets=per_city_budget * 0.1 * num_cities if budget else 50 * total_days,
            total=budget or (2000 * num_cities),
        )

        # 装备清单
        packing_list = [
            "身份证、护照",
            "手机、充电宝",
            "换洗衣物",
            "洗漱用品",
            "常用药品",
            "相机（可选）",
        ]

        return TripPlan(
            title=title,
            summary=summary,
            destination=f"{'→'.join(destinations)}",
            days_count=total_days,
            days=all_days,
            train_route=None,  # 多城市路由信息复杂，暂不生成
            budget_breakdown=budget_breakdown,
            packing_list=packing_list,
            tips=tips,
            travel_date=travel_date,
            season_info=season_info,
        )

    def refine_plan(
        self,
        current_plan: TripPlan,
        user_feedback: str,
    ) -> TripPlan:
        """
        根据用户反馈调整旅行计划

        Args:
            current_plan: 当前计划
            user_feedback: 用户反馈，如"第二天太满了"、"加个美食推荐"

        Returns:
            调整后的TripPlan对象
        """
        # 构建提示
        system_prompt = """你是一个旅行规划专家。用户会对当前旅行计划提出修改意见，
请根据用户反馈调整计划，保持其他部分不变。
输出必须是有效的JSON格式，直接返回完整的旅行计划，不要有任何额外解释。"""

        # 将当前计划转为JSON
        current_plan_json = json.dumps(current_plan.to_dict(), ensure_ascii=False, indent=2)

        user_prompt = f"""当前旅行计划：
{current_plan_json}

用户反馈：{user_feedback}

请根据用户反馈调整计划，保持JSON格式不变。"""

        try:
            response = self.llm_client.chat(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.5,
                max_tokens=4096,
            )

            return self._parse_llm_response(response, current_plan.destination, current_plan.days_count, None)

        except (LLMNotConfiguredError, LLMRequestError):
            logger.warning("LLM不可用，无法调整计划")
            return current_plan

    def _build_system_prompt(self) -> str:
        """构建系统提示"""
        return """你是一个热情友好的旅行规划师，擅长根据用户需求设计实用的旅行方案。

设计原则：
1. 行程安排要合理，不要太紧凑，早晨8-9点开始活动，晚上留出休息时间
2. 推荐要具体，给出具体的店名、位置、价格区间，不要泛泛而谈
3. 费用预估要有依据，基于实际消费水平
4. 突出当地特色，结合城市攻略中的美食和景点

输出格式：
必须输出有效的JSON字符串，格式如下（不要有任何额外解释）：
{
    "title": "计划标题",
    "summary": "简要概述，50字左右",
    "destination": "目的地",
    "days_count": 天数,
    "days": [
        {
            "day_number": 1,
            "theme": "今日主题",
            "activities": [
                {
                    "time": "09:00-12:00",
                    "name": "活动名称",
                    "desc": "详细描述，包括位置、门票等信息",
                    "tip": "小贴士"
                }
            ],
            "food": ["推荐美食1", "推荐美食2"],
            "accommodation": "住宿建议"
        }
    ],
    "budget_breakdown": {
        "transport": 交通费,
        "accommodation": 住宿费,
        "food": 餐饮费,
        "tickets": 门票,
        "total": 总费用
    },
    "packing_list": ["装备1", "装备2"],
    "tips": ["提示1", "提示2"]
}"""

    def _build_user_prompt(
        self,
        destination: str,
        days: int,
        budget: Optional[float],
        preferences: list[str],
        train_info: Optional[dict],
        travel_date: Optional[str] = None,
    ) -> str:
        """构建用户提示"""
        # 获取城市攻略
        city_guide = self._get_city_guide(destination)

        prompt_parts = [
            f"帮我规划一次{destination}{days}日游旅行计划。",
        ]

        # 注入季节信息
        if travel_date:
            try:
                year, month, _ = travel_date.split("-")
                season_info = get_season_engine().get_season_info(destination, int(month))
                prompt_parts.append(f"\n📅 出行时间：{travel_date}（{season_info['season']}）")
                prompt_parts.append(f"🌤️ 天气概况：{season_info['weather']}，气温{season_info['temp']}")
                prompt_parts.append(f"👔 穿衣建议：{season_info['clothes']}")
                prompt_parts.append(f"💡 注意事项：{season_info['tips']}")

                # 节假日提醒
                from datetime import datetime
                date_obj = datetime.strptime(travel_date, "%Y-%m-%d").date()
                holiday_info = get_holiday_alert(date_obj)
                if holiday_info.get("alert"):
                    prompt_parts.append(f"\n{holiday_info['alert']}")
                    if holiday_info.get("tips"):
                        prompt_parts.append(f"建议：{'；'.join(holiday_info['tips'])}")

                # 季节性推荐
                seasonal_rec = get_season_engine().get_seasonal_recommendation(destination, int(month))
                prompt_parts.append(f"\n{seasonal_rec}")
            except Exception as e:
                logger.warning(f"获取季节信息失败: {e}")

        # 目的地介绍
        if city_guide:
            prompt_parts.append(f"\n{destination}城市信息：")
            prompt_parts.append(f"- 著名景点：{', '.join(city_guide.get('highlights', []))}")
            prompt_parts.append(f"- 推荐美食：{', '.join(city_guide.get('food', []))}")
            prompt_parts.append(f"- 最佳季节：{city_guide.get('best_season', '')}")
            prompt_parts.append(f"- 交通提示：{city_guide.get('transport', '')}")
            prompt_parts.append(f"- 实用贴士：{', '.join(city_guide.get('tips', []))}")

        # 火车路线
        if train_info:
            prompt_parts.append(f"\n火车路线信息：")
            prompt_parts.append(f"- 车次：{train_info.get('train_no', '')}")
            prompt_parts.append(f"- {train_info.get('from_station', '')} → {train_info.get('to_station', '')}")
            prompt_parts.append(f"- 发车：{train_info.get('depart_time', '')}，到达：{train_info.get('arrive_time', '')}")
            prompt_parts.append(f"- 历时：{train_info.get('duration', '')}")
            prompt_parts.append(f"- 票价参考：{train_info.get('price_range', '')}")
            if train_info.get('tips'):
                prompt_parts.append(f"- 提示：{train_info.get('tips', '')}")

        # 预算
        if budget:
            prompt_parts.append(f"\n预算：约{budget}元/人")
        else:
            prompt_parts.append(f"\n预算：可根据目的地正常消费水平估算")

        # 偏好
        if preferences:
            pref_text = "、".join(preferences)
            prompt_parts.append(f"\n用户偏好：{pref_text}，请在行程中体现这些偏好。")

        # 格式要求
        prompt_parts.append("\n\n请输出完整的旅行计划JSON。")

        return "\n".join(prompt_parts)

    def _parse_llm_response(
        self,
        response: str,
        destination: str,
        days: int,
        train_info: Optional[dict],
    ) -> TripPlan:
        """
        解析LLM响应

        Args:
            response: LLM响应字符串
            destination: 目的地
            days: 天数
            train_info: 火车路线信息

        Returns:
            TripPlan对象
        """
        # 尝试提取JSON
        json_str = self._extract_json(response)

        if json_str:
            try:
                data = json.loads(json_str)
                return TripPlan.from_dict(data)
            except json.JSONDecodeError as e:
                logger.warning(f"JSON解析失败，尝试修复: {e}")

        # 尝试修复常见的JSON问题
        fixed_json = self._fix_json(response)
        if fixed_json:
            try:
                data = json.loads(fixed_json)
                return TripPlan.from_dict(data)
            except json.JSONDecodeError:
                pass

        # 解析失败，返回降级方案
        logger.error("无法解析LLM响应，返回降级方案")
        return self._fallback_plan(destination, days, None, None, train_info)

    def _extract_json(self, text: str) -> Optional[str]:
        """
        从文本中提取JSON

        Args:
            text: 原始文本

        Returns:
            JSON字符串，未找到返回None
        """
        # 尝试提取 ```json ... ``` 块
        match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
        if match:
            return match.group(1).strip()

        # 尝试提取 { ... }
        match = re.search(r"(\{[\s\S]*\})", text)
        if match:
            return match.group(1).strip()

        return None

    def _fix_json(self, text: str) -> Optional[str]:
        """
        修复常见的JSON问题

        Args:
            text: 原始文本

        Returns:
            修复后的JSON字符串
        """
        json_str = self._extract_json(text)
        if not json_str:
            return None

        # 移除尾部多余的逗号
        json_str = re.sub(r",(\s*[}\]])", r"\1", json_str)

        # 移除单引号
        json_str = json_str.replace("'", '"')

        return json_str

    def _fallback_plan(
        self,
        destination: str,
        days: int,
        budget: Optional[float],
        preferences: Optional[list[str]],
        train_info: Optional[dict],
    ) -> TripPlan:
        """
        降级方案：基于静态数据生成计划（LLM不可用时使用）

        Args:
            destination: 目的地
            days: 天数
            budget: 预算
            preferences: 偏好
            train_info: 火车信息

        Returns:
            基于本地数据的TripPlan
        """
        city_guide = self._get_city_guide(destination)

        # 构建基础计划
        title = f"{destination}{days}日游"
        summary = f"探索{destination}之美，体验当地风土人情。"

        if city_guide:
            highlights = city_guide.get("highlights", [])
            food = city_guide.get("food", [])
            summary = f"游览{city_guide.get('province', '')}{destination}，探访{', '.join(highlights[:3])}等景点，品尝{', '.join(food[:3])}等美食。"

        # 生成每日行程
        days_plans = []
        for i in range(1, days + 1):
            day_plan = DayPlan(
                day_number=i,
                theme=f"第{i}天",
                activities=[
                    Activity(
                        time="09:00-12:00",
                        name="自由活动",
                        desc="根据个人兴趣安排活动",
                        tip="注意安全，保持联系"
                    )
                ],
                food=city_guide.get("food", [])[:3] if city_guide else [],
                accommodation="建议提前预订住宿",
            )
            days_plans.append(day_plan)

        # 火车路线
        train_route = None
        if train_info:
            train_route = TrainRouteInfo(
                train_no=train_info.get("train_no", ""),
                from_station=train_info.get("from_station", ""),
                to_station=train_info.get("to_station", ""),
                depart_time=train_info.get("depart_time", ""),
                arrive_time=train_info.get("arrive_time", ""),
                duration=train_info.get("duration", ""),
                train_type=train_info.get("train_type", ""),
                transfers=train_info.get("transfers", 0),
                price_range=train_info.get("price_range", ""),
                tips=train_info.get("tips", ""),
            )

        # 费用估算
        if budget:
            total = budget
        else:
            # 基于目的地估算
            daily = 300 if not city_guide else 400
            total = daily * days

        budget_breakdown = BudgetBreakdown(
            transport=train_info.get("price_low", 0) * 2 if train_info else 0,
            accommodation=total * 0.3,
            food=total * 0.25,
            tickets=total * 0.25,
            total=total,
        )

        # 装备清单
        packing_list = [
            "身份证",
            "手机、充电宝",
            "换洗衣物",
            "洗漱用品",
            "常用药品",
        ]

        if city_guide:
            if "拉萨" in destination or "西藏" in str(city_guide.get("province", "")):
                packing_list.extend(["红景天", "防晒霜", "墨镜", "厚外套"])
            if "哈尔滨" in destination or "冰雪" in city_guide.get("best_season", ""):
                packing_list.extend(["羽绒服", "保暖内衣", "暖宝宝", "手套"])

        # Tips
        tips = []
        if city_guide:
            tips = city_guide.get("tips", [])[:5]
        tips.extend([
            "提前规划行程",
            "预订住宿和交通",
            "注意人身财物安全",
        ])

        return TripPlan(
            title=title,
            summary=summary,
            destination=destination,
            days_count=days,
            days=days_plans,
            train_route=train_route,
            budget_breakdown=budget_breakdown,
            packing_list=packing_list,
            tips=tips,
        )
