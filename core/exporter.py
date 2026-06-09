"""
行程导出功能
支持导出为纯文本、Markdown和微信分享格式
"""

from typing import Optional
from core.itinerary import TripPlan


def export_to_text(trip_plan: TripPlan) -> str:
    """
    导出为纯文本格式行程单
    
    Args:
        trip_plan: 旅行计划对象
        
    Returns:
        纯文本格式的行程单
    """
    lines = []
    
    # 标题
    lines.append("=" * 50)
    lines.append(f"🚂 {trip_plan.title}")
    lines.append("=" * 50)
    lines.append("")
    
    # 基本信息
    lines.append(f"📍 目的地: {trip_plan.destination}")
    lines.append(f"📅 旅行天数: {trip_plan.days_count}天")
    lines.append(f"💰 预算: ¥{trip_plan.budget_breakdown.total:.0f}")
    
    if trip_plan.travel_date:
        lines.append(f"🗓️ 出发日期: {trip_plan.travel_date}")
    
    lines.append("")
    lines.append("-" * 50)
    
    # 火车路线
    if trip_plan.train_route:
        tr = trip_plan.train_route
        lines.append("🚂 推荐火车路线")
        lines.append(f"   {tr.train_no} {tr.from_station} → {tr.to_station}")
        lines.append(f"   {tr.depart_time} 出发 → {tr.arrive_time} 到达")
        lines.append(f"   历时: {tr.duration} | {tr.train_type}")
        lines.append(f"   票价: {tr.price_range}")
        if tr.tips:
            lines.append(f"   提示: {tr.tips}")
        lines.append("")
    
    # 每日行程
    lines.append("📅 每日行程")
    lines.append("-" * 50)
    
    for day in trip_plan.days:
        lines.append(f"\n【Day {day.day_number}】{day.theme}")
        
        if day.activities:
            for act in day.activities:
                time_range = act.time if act.time else "全天"
                lines.append(f"  ⏰ {time_range} {act.name}")
                if act.desc:
                    # 截取前100字符
                    desc = act.desc[:100] + "..." if len(act.desc) > 100 else act.desc
                    lines.append(f"     {desc}")
                if act.tip:
                    lines.append(f"     💡 {act.tip}")
        
        if day.food:
            lines.append("  🍜 今日美食:")
            for food in day.food:
                lines.append(f"     - {food}")
        
        if day.accommodation:
            lines.append(f"  🏨 住宿: {day.accommodation}")
    
    # 费用明细
    lines.append("")
    lines.append("=" * 50)
    lines.append("💰 费用预算")
    lines.append("-" * 50)
    lines.append(f"   交通费: ¥{trip_plan.budget_breakdown.transport:.0f}")
    lines.append(f"   住宿费: ¥{trip_plan.budget_breakdown.accommodation:.0f}")
    lines.append(f"   餐饮费: ¥{trip_plan.budget_breakdown.food:.0f}")
    lines.append(f"   门票费: ¥{trip_plan.budget_breakdown.tickets:.0f}")
    lines.append(f"   ------------------------")
    lines.append(f"   总计: ¥{trip_plan.budget_breakdown.total:.0f}")
    
    # 装备清单
    if trip_plan.packing_list:
        lines.append("")
        lines.append("🎒 装备清单")
        lines.append("-" * 50)
        for i, item in enumerate(trip_plan.packing_list, 1):
            lines.append(f"   {i}. {item}")
    
    # 实用Tips
    if trip_plan.tips:
        lines.append("")
        lines.append("💡 实用Tips")
        lines.append("-" * 50)
        for tip in trip_plan.tips:
            lines.append(f"   • {tip}")
    
    lines.append("")
    lines.append("=" * 50)
    lines.append("由 12306省心小助手 生成")
    lines.append("=" * 50)
    
    return "\n".join(lines)


def export_to_markdown(trip_plan: TripPlan) -> str:
    """
    导出为Markdown格式
    
    Args:
        trip_plan: 旅行计划对象
        
    Returns:
        Markdown格式的行程单
    """
    md = []
    
    # 标题
    md.append(f"# 🚂 {trip_plan.title}\n")
    
    # 基本信息卡片
    md.append("## 📋 基本信息\n")
    md.append("| 项目 | 内容 |")
    md.append("| --- | --- |")
    md.append(f"| 📍 目的地 | {trip_plan.destination} |")
    md.append(f"| 📅 旅行天数 | {trip_plan.days_count}天 |")
    md.append(f"| 💰 预算 | ¥{trip_plan.budget_breakdown.total:.0f} |")
    if trip_plan.travel_date:
        md.append(f"| 🗓️ 出发日期 | {trip_plan.travel_date} |")
    if trip_plan.season_info:
        season = trip_plan.season_info.get('season', '未知')
        weather = trip_plan.season_info.get('weather', '')
        md.append(f"| 🌡️ 季节 | {season} |")
        md.append(f"| 🌤️ 天气 | {weather} |")
    md.append("")
    
    # 火车路线
    if trip_plan.train_route:
        md.append("## 🚂 推荐火车路线\n")
        tr = trip_plan.train_route
        md.append(f"**{tr.train_no}** {tr.from_station} → {tr.to_station}\n")
        md.append(f"- ⏰ {tr.depart_time} 出发 → {tr.arrive_time} 到达")
        md.append(f"- 🕐 历时: {tr.duration} | 类型: {tr.train_type}")
        md.append(f"- 💵 票价: {tr.price_range}")
        if tr.tips:
            md.append(f"- 💡 {tr.tips}")
        md.append("")
    
    # 每日行程
    md.append("## 📅 每日行程\n")
    
    for day in trip_plan.days:
        md.append(f"### Day {day.day_number}: {day.theme}\n")
        
        if day.activities:
            md.append("| 时间 | 活动 | 详情 |")
            md.append("| --- | --- | --- |")
            for act in day.activities:
                time_range = act.time if act.time else "全天"
                desc = act.desc[:50] + "..." if len(act.desc) > 50 else act.desc
                tip = f"💡 {act.tip}" if act.tip else ""
                md.append(f"| {time_range} | {act.name} | {desc} {tip} |")
            md.append("")
        
        if day.food:
            md.append("**🍜 今日美食**\n")
            for food in day.food:
                md.append(f"- {food}")
            md.append("")
        
        if day.accommodation:
            md.append(f"**🏨 住宿建议**: {day.accommodation}\n")
        
        md.append("---\n")
    
    # 费用分析
    md.append("## 💰 费用预算\n")
    md.append("| 类别 | 费用 |")
    md.append("| --- | --- |")
    md.append(f"| 🚂 交通 | ¥{trip_plan.budget_breakdown.transport:.0f} |")
    md.append(f"| 🏨 住宿 | ¥{trip_plan.budget_breakdown.accommodation:.0f} |")
    md.append(f"| 🍜 餐饮 | ¥{trip_plan.budget_breakdown.food:.0f} |")
    md.append(f"| 🎫 门票 | ¥{trip_plan.budget_breakdown.tickets:.0f} |")
    md.append(f"| **总计** | **¥{trip_plan.budget_breakdown.total:.0f}** |")
    md.append("")
    
    # 装备清单
    if trip_plan.packing_list:
        md.append("## 🎒 装备清单\n")
        for i, item in enumerate(trip_plan.packing_list, 1):
            md.append(f"{i}. {item}")
        md.append("")
    
    # 实用Tips
    if trip_plan.tips:
        md.append("## 💡 实用Tips\n")
        for tip in trip_plan.tips:
            md.append(f"- {tip}")
        md.append("")
    
    # 页脚
    md.append("---\n")
    md.append("*由 12306省心小助手 生成*\n")
    
    return "\n".join(md)


def export_to_share_text(trip_plan: TripPlan) -> str:
    """
    导出为微信分享短文案
    
    格式简洁，适合朋友圈/群聊分享
    
    Args:
        trip_plan: 旅行计划对象
        
    Returns:
        分享文案
    """
    parts = []
    
    # 标题
    parts.append(f"🚂 {trip_plan.title}")
    parts.append("")
    
    # 基本信息
    parts.append(f"📍 {trip_plan.destination} | {trip_plan.days_count}天 | 💰¥{trip_plan.budget_breakdown.total:.0f}")
    
    # 火车信息
    if trip_plan.train_route:
        tr = trip_plan.train_route
        parts.append(f"🚄 {tr.train_no} | {tr.depart_time}-{tr.arrive_time} | {tr.duration}")
    
    parts.append("")
    
    # 行程亮点（每日前3个活动）
    parts.append("📅 行程亮点:")
    for day in trip_plan.days[:3]:  # 只显示前3天
        highlights = [a.name for a in day.activities[:3]] if day.activities else []
        if highlights:
            parts.append(f"Day{day.day_number}: {'+'.join(highlights[:2])}")
    
    # 费用
    parts.append("")
    parts.append(f"💰 费用: 交通¥{trip_plan.budget_breakdown.transport:.0f} + 住宿¥{trip_plan.budget_breakdown.accommodation:.0f} + 餐饮¥{trip_plan.budget_breakdown.food:.0f}")
    
    # 特色美食
    if trip_plan.days and any(d.food for d in trip_plan.days):
        foods = []
        for d in trip_plan.days:
            if d.food:
                foods.extend(d.food[:2])
        if foods:
            parts.append("")
            parts.append(f"🍜 必吃: {', '.join(foods[:3])}")
    
    parts.append("")
    parts.append("---")
    parts.append("✨ 由12306省心小助手生成")
    
    return "\n".join(parts)
