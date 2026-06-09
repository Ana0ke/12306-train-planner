"""
Demo旅行方案 - 预生成的热门目的地旅行计划
用于无API Key时的体验模式
"""

from core.itinerary import (
    TripPlan, DayPlan, Activity, BudgetBreakdown, TrainRouteInfo
)


def get_demo_plans() -> dict[str, TripPlan]:
    """
    获取所有Demo旅行方案

    Returns:
        字典，key为目的地拼音，value为TripPlan对象
    """
    return {
        "lhasa": _create_lhasa_5day_plan(),
        "chengdu": _create_chengdu_4day_plan(),
        "xian": _create_xian_3day_plan(),
        "xiamen": _create_xiamen_3day_plan(),
        "lijiang": _create_lijiang_5day_plan(),
    }


def get_demo_plan_by_destination(destination: str) -> TripPlan | None:
    """
    根据目的地名称获取Demo方案

    Args:
        destination: 目的地名称（支持中文、拼音、拼音首字母）

    Returns:
        TripPlan对象，未找到返回None
    """
    plans = get_demo_plans()

    # 中文匹配
    chinese_map = {
        "拉萨": "lhasa",
        "拉萨市": "lhasa",
        "成都": "chengdu",
        "成都市": "chengdu",
        "西安": "xian",
        "西安市": "xian",
        "厦门": "xiamen",
        "厦门市": "xiamen",
        "丽江": "lijiang",
        "丽江市": "lijiang",
    }

    if destination in chinese_map:
        return plans.get(chinese_map[destination])

    # 拼音匹配
    if destination.lower() in plans:
        return plans.get(destination.lower())

    # 模糊匹配
    for key, plan in plans.items():
        if destination.lower() in key or key in destination.lower():
            return plan
        if destination in plan.destination or plan.destination in destination:
            return plan

    return None


def _create_lhasa_5day_plan() -> TripPlan:
    """拉萨5日深度游"""
    return TripPlan(
        title="拉萨5日深度游",
        summary="乘坐Z264次列车穿越青藏高原，感受世界屋脊的壮美与神秘。布达拉宫虔诚祈福，纳木错湖畔看日出，这是一次洗涤心灵的旅程。",
        destination="拉萨",
        days_count=5,
        days=[
            DayPlan(
                day_number=1,
                theme="启程 · 天路之旅",
                activities=[
                    Activity(
                        time="08:00-09:00",
                        name="东安东站出发",
                        desc="提前1小时到站，取票安检，准备登车。携带身份证原件和学生证（景区可能有优惠）。",
                        tip="记得带身份证，刷身份证进站"
                    ),
                    Activity(
                        time="09:00-09:30",
                        name="火车上的上午",
                        desc="欣赏沿途风景，从湖南的山水逐渐过渡到云贵高原。",
                        tip="可以开始服用红景天，预防高原反应"
                    ),
                    Activity(
                        time="09:30-18:00",
                        name="穿越云贵高原",
                        desc="火车穿越云贵高原，沿途欣赏壮丽的喀斯特地貌。",
                        tip="多喝水，保持充足睡眠"
                    ),
                ],
                food=["火车餐", "自带零食", "巧克力"],
                accommodation="Z264次列车硬卧",
            ),
            DayPlan(
                day_number=2,
                theme="穿越可可西里",
                activities=[
                    Activity(
                        time="全天",
                        name="青藏铁路精华段",
                        desc="翻越唐古拉山（海拔5072米），穿越可可西里无人区。运气好的话可以看到藏羚羊、藏野驴等野生动物。",
                        tip="海拔最高处超过5000米，多喝水少走动，有不适及时告诉列车员"
                    ),
                    Activity(
                        time="傍晚",
                        name="抵达拉萨",
                        desc="列车抵达拉萨站，出站后乘坐出租车或公交车前往市区酒店。",
                        tip="不要剧烈运动，慢慢行走"
                    ),
                ],
                food=["火车餐", "葡萄糖水", "巧克力"],
                accommodation="拉萨市区酒店（建议提前预订）",
            ),
            DayPlan(
                day_number=3,
                theme="虔诚 · 布达拉宫",
                activities=[
                    Activity(
                        time="08:00-10:00",
                        name="布达拉宫",
                        desc="世界上海拔最高的宫殿，布达拉宫需要提前1天预约门票。建议请导游讲解，否则看不懂壁画和历史。门票200元，优惠票100元。",
                        tip="请导游约150元，建议拼团。参观时间约2小时，禁止拍照。"
                    ),
                    Activity(
                        time="11:00-13:00",
                        name="宗角禄康公园",
                        desc="布达拉宫背后的公园，可以拍摄布达拉宫倒影，藏民在这里跳锅庄舞。",
                        tip="早上来可以看到晨练的藏民"
                    ),
                    Activity(
                        time="14:00-16:00",
                        name="大昭寺",
                        desc="藏传佛教圣地，有1300多年历史，供奉着文成公主带来的释迦牟尼12岁等身像。门票85元。",
                        tip="八廓街顺时针行走，尊重当地信仰"
                    ),
                    Activity(
                        time="16:00-18:00",
                        name="八廓街",
                        desc="拉萨最古老的街道，围绕大昭寺的转经道。街道两旁是藏式建筑，有很多藏族手工艺品和纪念品店。",
                        tip="购物记得砍价，至少砍一半"
                    ),
                ],
                food=["光明港琼甜茶馆（藏面+甜茶）", "玛吉阿米（藏餐）", "安多诺增藏餐"],
                accommodation="拉萨市区酒店",
            ),
            DayPlan(
                day_number=4,
                theme="圣湖 · 纳木错",
                activities=[
                    Activity(
                        time="06:00-08:00",
                        name="前往纳木错",
                        desc="从拉萨出发，沿青藏公路前往纳木错，全程约220公里，车程约4小时。沿途经过那根拉山口（海拔5190米）。",
                        tip="早起出发，纳木错日出非常美"
                    ),
                    Activity(
                        time="09:00-14:00",
                        name="纳木错湖畔",
                        desc="西藏三大圣湖之一，湖面海拔4718米，湖水清澈，雪山倒映。可骑马或徒步环湖，门票120元。",
                        tip="湖边风大，带好外套和防晒"
                    ),
                    Activity(
                        time="14:00-18:00",
                        name="返回拉萨",
                        desc="下午返回拉萨，路上可以休息。",
                        tip="今天会比较累，晚上好好休息"
                    ),
                ],
                food=["纳木错周边藏餐", "自带干粮", "拉萨晚餐"],
                accommodation="拉萨市区酒店",
            ),
            DayPlan(
                day_number=5,
                theme="悠闲 · 拉萨时光",
                activities=[
                    Activity(
                        time="09:00-11:00",
                        name="色拉寺",
                        desc="拉萨三大寺之一，以辨经著称。每天下午3点开始辨经，非常有特色。门票50元。",
                        tip="辨经是藏传佛教独特的修行方式，值得一看"
                    ),
                    Activity(
                        time="12:00-14:00",
                        name="布达拉宫广场",
                        desc="在广场拍照留念，然后去旁边的天上人间或神偷巧克力吃午餐。",
                        tip="广场上可以拍布达拉宫全景倒影"
                    ),
                    Activity(
                        time="15:00-17:00",
                        name="购买特产",
                        desc="在八廓街或超市购买牦牛肉干、藏红花、唐卡等特产。",
                        tip="藏红花建议去正规药店购买"
                    ),
                    Activity(
                        time="晚上",
                        name="返程",
                        desc="根据返程车次前往拉萨站。",
                        tip="提前2小时到站"
                    ),
                ],
                food=["光明港琼甜茶馆", "牦牛酸奶", "返程火车餐"],
                accommodation="Z264次列车",
            ),
        ],
        train_route=TrainRouteInfo(
            train_no="Z264",
            from_station="东安东",
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
            transport=1400,
            accommodation=600,
            food=400,
            tickets=500,
            total=2900,
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
            "葡萄糖粉或糖果",
            "围巾或披肩（防晒+拍照）",
        ],
        tips=[
            "第一天到拉萨多休息，不要洗澡洗头",
            "布达拉宫需提前1天预约门票",
            "尊重当地宗教习俗，顺时针参观寺庙",
            "高原紫外线强，全年都需要防晒",
            "纳木错建议跟团或包车，路况复杂",
        ],
        travel_date=None,
        season_info=None,
    )


def _create_chengdu_4day_plan() -> TripPlan:
    """成都4日休闲游"""
    return TripPlan(
        title="成都4日休闲游",
        summary="熊猫基地看萌主、宽窄巷子品美食、锦里古街赏夜景、都江堰叹古人智慧。这是一座来了就不想走的城市。",
        destination="成都",
        days_count=4,
        days=[
            DayPlan(
                day_number=1,
                theme="萌主 · 大熊猫基地",
                activities=[
                    Activity(
                        time="07:00-08:00",
                        name="前往熊猫基地",
                        desc="早起出发，建议8点前到达熊猫基地，这时熊猫最活跃。乘坐地铁3号线到熊猫大道站，出站后有景区直通车。",
                        tip="早点去！熊猫9-10点就开始睡觉了"
                    ),
                    Activity(
                        time="08:00-11:30",
                        name="成都大熊猫繁育研究基地",
                        desc="世界著名的大熊猫迁地保护基地，有大熊猫、小熊猫等。门票55元，建议游览2-3小时。",
                        tip="月亮产房值得一看，运气好能看到熊猫宝宝"
                    ),
                    Activity(
                        time="12:00-14:00",
                        name="午饭",
                        desc="熊猫基地附近有很多川菜馆，推荐“老蜀人”或“巴蜀大宅门”。",
                        tip="吃完饭可以休息一下再继续游玩"
                    ),
                    Activity(
                        time="14:30-17:00",
                        name="宽窄巷子",
                        desc="成都最具代表性的历史文化街区，由宽巷子、窄巷子、井巷子组成。免费开放。",
                        tip="宽巷子偏商业化，窄巷子更有老成都味道"
                    ),
                    Activity(
                        time="18:00-20:00",
                        name="晚饭",
                        desc="在宽窄巷子附近品尝成都小吃，推荐“龙抄手”或“蜀大侠”。",
                        tip="火锅店排队严重，建议提前预约或错峰"
                    ),
                ],
                food=["龙抄手", "担担面", "钟水饺", "串串香"],
                accommodation="成都春熙路/太古里附近酒店",
            ),
            DayPlan(
                day_number=2,
                theme="古韵 · 都江堰",
                activities=[
                    Activity(
                        time="07:30-09:30",
                        name="前往都江堰",
                        desc="从成都乘坐城际列车到都江堰，车程约40分钟。或在茶店子客运站乘大巴。",
                        tip="建议早点出发，避开周末人流"
                    ),
                    Activity(
                        time="10:00-13:00",
                        name="都江堰景区",
                        desc="世界文化遗产，两千多年前李冰父子修建的水利工程，至今仍在使用。门票90元，建议请导游讲解。",
                        tip="南桥夜景很美，如果时间允许可以等到晚上"
                    ),
                    Activity(
                        time="13:00-14:00",
                        name="午饭",
                        desc="都江堰景区附近有“青城山庄”或当地农家乐。",
                        tip="青城山猕猴桃很甜，可以尝尝"
                    ),
                    Activity(
                        time="14:30-17:00",
                        name="青城山",
                        desc="道教名山，分为前山和后山。前山以道观古迹为主，后山以自然风光著称。",
                        tip="体力有限的话只爬前山即可"
                    ),
                    Activity(
                        time="18:00-20:00",
                        name="返回成都+锦里",
                        desc="返回成都后前往锦里古街，夜景很美，有很多小吃。",
                        tip="锦里的小吃不便宜，建议尝鲜为主"
                    ),
                ],
                food=["青城泡菜", "白果炖鸡", "火锅", "三大炮"],
                accommodation="成都春熙路/太古里附近酒店",
            ),
            DayPlan(
                day_number=3,
                theme="慢生活 · 成都citywalk",
                activities=[
                    Activity(
                        time="09:00-11:00",
                        name="武侯祠",
                        desc="纪念诸葛亮的三国博物馆，门票50元。红墙竹影非常适合拍照。",
                        tip="锦里和武侯祠在一起，可以一起游览"
                    ),
                    Activity(
                        time="11:00-13:00",
                        name="锦里古街",
                        desc="武侯祠旁边的古街，有很多成都特色小吃和手工艺品。",
                        tip="张飞牛肉、兔头、糖油果子必尝"
                    ),
                    Activity(
                        time="13:00-15:00",
                        name="午饭+休息",
                        desc="在锦里附近的“皇城坝”吃午饭，推荐豆花和肥肠粉。",
                        tip='成都人喜欢吃苍蝇馆子，环境一般但味道好'

                    ),
                    Activity(
                        time="15:30-18:00",
                        name="春熙路+太古里",
                        desc="成都最繁华的商业区，有IFS爬墙熊猫、方所书店等网红打卡点。",
                        tip="IFS熊猫在7楼天台，排队拍照的人很多"
                    ),
                    Activity(
                        time="18:30-21:00",
                        name="九眼桥夜景",
                        desc="成都夜生活的代表，安顺廊桥夜景很美。附近有很多酒吧。",
                        tip="339电视塔可以看成都夜景"
                    ),
                ],
                food=["豆花", "肥肠粉", "冰粉", "蛋烘糕", "玉林串串"],
                accommodation="成都春熙路/太古里附近酒店",
            ),
            DayPlan(
                day_number=4,
                theme="舌尖 · 美食之旅",
                activities=[
                    Activity(
                        time="08:00-10:00",
                        name="人民公园鹤鸣茶社",
                        desc="成都最老的茶馆，本地人喝茶聊天的地方。可以体验掏耳朵、看川剧变脸。",
                        tip="茶社消费约30-50元，掏耳朵另收费"
                    ),
                    Activity(
                        time="10:00-12:00",
                        name="文殊院",
                        desc="成都最著名的佛教寺院，香火很旺。周围有很多素斋店。免费开放。",
                        tip="文殊院门口的宫廷桃酥很好吃"
                    ),
                    Activity(
                        time="12:00-14:00",
                        name="午饭",
                        desc="在文殊院附近吃午饭，推荐“洞子口张凉粉”或“龙抄手总店”。",
                        tip="成都的凉粉、甜水面很有特色"
                    ),
                    Activity(
                        time="14:00-16:00",
                        name="东郊记忆",
                        desc="成都的“798”，由以前的工厂改造而成，有很多文创店和咖啡馆。",
                        tip="适合拍照，很文艺"
                    ),
                    Activity(
                        time="16:30-18:00",
                        name="建设路小吃街",
                        desc="成都最火的小吃街，烤脑花、降龙爪爪、糍粑冰粉等网红小吃都在这里。",
                        tip="傍晚去最好，人多热闹"
                    ),
                    Activity(
                        time="晚上",
                        name="返程",
                        desc="根据返程时间前往机场或火车站。",
                        tip="成都双流机场离市区很近，打车约30分钟"
                    ),
                ],
                food=["降龙爪爪", "烤脑花", "糍粑冰粉", "绵绵冰", "兔头"],
                accommodation="无（返程日）",
            ),
        ],
        train_route=TrainRouteInfo(
            train_no="Z334",
            from_station="东安东",
            to_station="成都",
            depart_time="09:48",
            arrive_time="08:24+1",
            duration="22:36",
            train_type="直达特快",
            transfers=0,
            price_range="硬座¥148.5/硬卧¥280.5/软卧¥448.5",
            tips="建议购买硬卧，睡一晚就到成都了"
        ),
        budget_breakdown=BudgetBreakdown(
            transport=600,
            accommodation=400,
            food=500,
            tickets=200,
            total=1700,
        ),
        packing_list=[
            "身份证",
            "雨伞（成都多雨）",
            "舒适的步行鞋",
            "肠胃药（成都美食偏辣）",
            "充电宝",
            "相机（拍熊猫必备）",
        ],
        tips=[
            "成都火锅要配油碟，不要配麻酱",
            "大熊猫基地早上8点前到达最好",
            "成都地铁很方便，可以到达大部分景点",
            "川菜偏辣，点菜时记得说微微辣或不辣",
            "成都人说话带儿话音，是本地特色",
        ],
        travel_date=None,
        season_info=None,
    )


def _create_xian_3day_plan() -> TripPlan:
    """西安3日古都行"""
    return TripPlan(
        title="西安3日古都行",
        summary="一朝入长安，一眼望千年。兵马俑看历史奇迹，大雁塔听梵音袅袅，大唐不夜城梦回盛唐。这是一次穿越千年的文化之旅。",
        destination="西安",
        days_count=3,
        days=[
            DayPlan(
                day_number=1,
                theme="奇迹 · 秦始皇兵马俑",
                activities=[
                    Activity(
                        time="07:00-08:30",
                        name="前往兵马俑",
                        desc="在西安火车站东广场乘坐游5路公交车（306路），到兵马俑站下车，车程约1小时。票价7元。",
                        tip="认准正规的游5路，黑车很多"
                    ),
                    Activity(
                        time="09:00-12:00",
                        name="秦始皇兵马俑博物馆",
                        desc="世界第八大奇迹，分为一号坑、二号坑、三号坑和铜车马展厅。建议请导游或租讲解器，否则看不懂。门票120元。",
                        tip="一号坑最大最震撼，建议最后参观"
                    ),
                    Activity(
                        time="12:30-14:00",
                        name="午饭",
                        desc="兵马俑景区附近有美食街，推荐“魏家凉皮”或当地农家乐。",
                        tip="可以尝尝biangbiang面"
                    ),
                    Activity(
                        time="14:30-17:00",
                        name="华清宫",
                        desc="杨贵妃沐浴之地，也是西安事变发生地。门票120元，包含华清池和骊山。",
                        tip="华清池夜景《长恨歌》很震撼，但需要另外购票"
                    ),
                    Activity(
                        time="18:00-21:00",
                        name="大唐不夜城",
                        desc="西安最火的网红打卡地，晚上灯火辉煌，有很多表演和互动节目。",
                        tip="一定要晚上去！大雁塔北广场有音乐喷泉表演"
                    ),
                ],
                food=["biangbiang面", "肉夹馍", "凉皮", "羊肉泡馍"],
                accommodation="西安钟楼/回民街附近酒店",
            ),
            DayPlan(
                day_number=2,
                theme="古城 · 历史穿越",
                activities=[
                    Activity(
                        time="08:00-10:00",
                        name="明城墙",
                        desc="中国现存最完整的古代城墙，周长约14公里。可以骑自行车环城，也可以步行。门票54元，骑车另加45元。",
                        tip="建议骑自行车，2小时可以环城一周"
                    ),
                    Activity(
                        time="10:30-12:30",
                        name="钟楼+鼓楼",
                        desc="西安的地标建筑，钟楼位于市中心，鼓楼在回民街对面。联票50元。",
                        tip="钟楼和鼓楼相距不远，可以一起参观"
                    ),
                    Activity(
                        time="12:30-14:00",
                        name="午饭（回民街）",
                        desc="回民街是西安著名的小吃街，有各种西安特色美食。",
                        tip="回民街主街商业化较重，往里走的小巷子更地道"
                    ),
                    Activity(
                        time="14:30-17:00",
                        name="陕西历史博物馆",
                        desc="中国第一座大型现代化国家级博物馆，周恩来总理提议建设。免费开放，但需要提前预约。",
                        tip="一定要提前预约！每天限量发放免费票"
                    ),
                    Activity(
                        time="18:00-20:00",
                        name="大雁塔+大唐芙蓉园",
                        desc="大雁塔是唐僧取经归来翻译经文的地方，大唐芙蓉园是仿唐主题公园。夜景很美。",
                        tip="大唐芙蓉园门票120元，不进去也可以在外面看夜景"
                    ),
                ],
                food=["牛羊肉泡馍", "贾三灌汤包", "biangbiang面", "甑糕", "酸梅汤"],
                accommodation="西安钟楼/回民街附近酒店",
            ),
            DayPlan(
                day_number=3,
                theme="味道 · 美食探索",
                activities=[
                    Activity(
                        time="08:30-10:30",
                        name="小雁塔+西安博物院",
                        desc="小雁塔和荐福寺组成，免费开放。人少清静，比大雁塔更适合慢慢逛。",
                        tip="西安博物院可以了解西安的前世今生"
                    ),
                    Activity(
                        time="11:00-13:00",
                        name="永兴坊",
                        desc="摔碗酒的发源地，有很多网红小吃。抖音上很火的摔碗酒就是这里。",
                        tip="摔碗酒5元一碗，仪式感十足"
                    ),
                    Activity(
                        time="13:00-15:00",
                        name="午饭",
                        desc="在永兴坊或附近吃午饭，推荐面食和陕西菜。",
                        tip="陕西的面食种类繁多，可以每天换一种"
                    ),
                    Activity(
                        time="15:30-17:30",
                        name="赛格国际购物中心",
                        desc="西安最大的购物中心，有亚洲第一长的扶梯和室内瀑布。可以购物或休息。",
                        tip="长安大排档在这里有店，可以边吃边看表演"
                    ),
                    Activity(
                        time="晚上",
                        name="返程",
                        desc="根据返程时间前往机场或火车站。西安北站是高铁站，有地铁直达。",
                        tip="西安咸阳机场距市区约40公里，需提前2小时出发"
                    ),
                ],
                food=["子午路张记肉夹馍", "凉皮", "黄桂稠酒", "粉汤羊血"],
                accommodation="无（返程日）",
            ),
        ],
        train_route=TrainRouteInfo(
            train_no="Z230",
            from_station="东安东",
            to_station="西安",
            depart_time="22:22",
            arrive_time="12:48+1",
            duration="14:26",
            train_type="直达特快",
            transfers=0,
            price_range="硬座¥148.5/硬卧¥280.5/软卧¥448.5",
            tips="夕发朝至，睡一觉就到西安"
        ),
        budget_breakdown=BudgetBreakdown(
            transport=600,
            accommodation=300,
            food=400,
            tickets=350,
            total=1650,
        ),
        packing_list=[
            "身份证",
            "舒适的步行鞋",
            "充电宝",
            "防晒用品",
            "学生证（景区可能有优惠）",
        ],
        tips=[
            "兵马俑一定要请导游或租讲解器",
            "陕西历史博物馆免费但需要提前预约",
            "回民街往小巷子里走更地道",
            "西安天气干燥，多喝水多吃水果",
            "古城墙骑自行车环城约2小时",
        ],
        travel_date=None,
        season_info=None,
    )


def _create_xiamen_3day_plan() -> TripPlan:
    """厦门3日海岛风情"""
    return TripPlan(
        title="厦门3日海岛风情",
        summary="漫步鼓浪屿，感受万国建筑风情；骑行环岛路，聆听海浪的声音；南普陀寺祈福，曾厝垵寻美食。这是一座文艺清新的海上花园城市。",
        destination="厦门",
        days_count=3,
        days=[
            DayPlan(
                day_number=1,
                theme="浪漫 · 鼓浪屿",
                activities=[
                    Activity(
                        time="07:30-08:00",
                        name="前往东渡码头",
                        desc="在厦门市区乘坐公交车或出租车到东渡码头，车程约20分钟。",
                        tip="提前30分钟到达码头"
                    ),
                    Activity(
                        time="08:00-09:00",
                        name="乘船前往鼓浪屿",
                        desc="在东渡码头乘坐渡轮前往鼓浪屿三丘田码头，票价35元（含返程）。需要刷身份证。",
                        tip="微信搜索“厦门轮渡有限公司”提前买票"
                    ),
                    Activity(
                        time="09:00-12:00",
                        name="鼓浪屿漫步",
                        desc="世界文化遗产，有“万国建筑博览”之称。推荐路线: 日光岩-菽庄花园-皓月园-风琴博物馆。",
                        tip="日光岩是鼓浪屿最高点，可以俯瞰全岛"
                    ),
                    Activity(
                        time="12:00-14:00",
                        name="龙头路午餐",
                        desc="鼓浪屿最热闹的商业街，有很多网红小吃店。推荐林氏鱼丸、叶氏麻糍。",
                        tip="鼓浪屿上不能骑单车，只能步行"
                    ),
                    Activity(
                        time="14:00-17:00",
                        name="深度探索",
                        desc="可以参观钢琴博物馆、百年鼓浪屿博物馆，或在海边发呆。",
                        tip="下午4-5点拍日光岩日落很美"
                    ),
                    Activity(
                        time="17:30-18:30",
                        name="返回厦门",
                        desc="乘船返回厦门，车览鹭江夜景。",
                        tip="返程末班船到晚上12点，不用担心"
                    ),
                ],
                food=["林氏鱼丸", "叶氏麻糍", "海蛎煎", "沙茶面"],
                accommodation="厦门中山路/曾厝垵附近酒店",
            ),
            DayPlan(
                day_number=2,
                theme="清新 · 环岛路",
                activities=[
                    Activity(
                        time="08:00-10:00",
                        name="厦门大学",
                        desc="中国最美大学之一，芙蓉隧道、芙蓉湖、情人谷都值得一看。免费开放，需要预约。",
                        tip="周一到周五限流，记得提前在公众号预约"
                    ),
                    Activity(
                        time="10:00-11:00",
                        name="南普陀寺",
                        desc="闽南佛教胜地，香火很旺。免费开放，可以领香拜佛。",
                        tip="素斋很有名，可以尝尝"
                    ),
                    Activity(
                        time="12:00-14:00",
                        name="沙坡尾",
                        desc="厦门最老的港口，有很多文艺小店和老建筑。避风坞很有渔村风情。",
                        tip="艺术西区有很多网红打卡点"
                    ),
                    Activity(
                        time="14:30-17:30",
                        name="环岛路骑行",
                        desc="厦门最浪漫的海滨公路，可以租单车骑行。推荐路线: 椰风寨-一国两制标语-会展中心。",
                        tip="租单车约20-30元/小时，记得砍价"
                    ),
                    Activity(
                        time="18:00-20:00",
                        name="曾厝垵",
                        desc="中国最文艺的渔村，有很多小吃和民宿。",
                        tip="阿信厚吐司和八婆婆烧仙草很火"
                    ),
                ],
                food=["沙茶面", "姜母鸭", "海蛎煎", "烧仙草", "土笋冻"],
                accommodation="厦门中山路/曾厝垵附近酒店",
            ),
            DayPlan(
                day_number=3,
                theme="闽南 · 文化探索",
                activities=[
                    Activity(
                        time="08:30-10:30",
                        name="集美学村",
                        desc="陈嘉庚先生创办的学村，有闽南建筑风格的嘉庚建筑群。乘坐地铁1号线可以到达。",
                        tip="厦门海上小火车就在地铁1号线上"
                    ),
                    Activity(
                        time="11:00-13:00",
                        name="陈嘉庚先生故居",
                        desc="了解爱国华侨陈嘉庚先生的事迹，感受他的爱国情怀。",
                        tip="学村食堂可以体验当地学生餐，便宜好吃"
                    ),
                    Activity(
                        time="13:30-15:30",
                        name="中山路步行街",
                        desc="厦门最老牌的商业街，有很多南洋骑楼建筑。",
                        tip="黄则和的花生汤和海蛎煎很有名"
                    ),
                    Activity(
                        time="16:00-17:30",
                        name="铁路文化公园",
                        desc="由废弃铁路改建的公园，很适合拍照，很文艺。",
                        tip="鸿山隧道很有历史感"
                    ),
                    Activity(
                        time="晚上",
                        name="返程",
                        desc="根据返程时间前往机场或火车站。厦门高崎国际机场距市中心约10公里。",
                        tip="厦门机场有机场快线到市区，很方便"
                    ),
                ],
                food=["黄则和花生汤", "海蛎煎", "姜母鸭", "闽南菜"],
                accommodation="无（返程日）",
            ),
        ],
        train_route=TrainRouteInfo(
            train_no="K229",
            from_station="东安东",
            to_station="厦门",
            depart_time="15:36",
            arrive_time="19:52+1",
            duration="28:16",
            train_type="快速列车",
            transfers=0,
            price_range="硬座¥189.5/硬卧¥363.5/软卧¥576.5",
            tips="建议购买硬卧，舒适度较好"
        ),
        budget_breakdown=BudgetBreakdown(
            transport=800,
            accommodation=400,
            food=500,
            tickets=150,
            total=1850,
        ),
        packing_list=[
            "身份证",
            "防晒霜（厦门阳光强烈）",
            "舒适的步行鞋",
            "遮阳帽/太阳伞",
            "相机（鼓浪屿拍照很美）",
            "薄外套（海边风大）",
        ],
        tips=[
            "鼓浪屿船票需要提前购买，节假日要提前一周",
            "厦门大学需要提前预约，周一至周五限流",
            "环岛路骑行建议租电动车，更省力",
            "曾厝垵的小吃不便宜，可以去八市菜市场更地道",
            "厦门天气暖和，衣服不用带太厚",
        ],
        travel_date=None,
        season_info=None,
    )


def _create_lijiang_5day_plan() -> TripPlan:
    """丽江5日慢旅行"""
    return TripPlan(
        title="丽江5日慢旅行",
        summary="漫步古城青石板路，感受纳西族东巴文化；玉龙雪山仰望冰川，蓝月谷漫步碧水；束河古镇享受宁静泸沽湖泛舟。这是一场洗涤灵魂的慢旅行。",
        destination="丽江",
        days_count=5,
        days=[
            DayPlan(
                day_number=1,
                theme="抵达 · 丽江古城",
                activities=[
                    Activity(
                        time="下午",
                        name="抵达丽江",
                        desc="根据交通方式到达丽江，可乘飞机或火车。丽江站距古城约10公里。",
                        tip="丽江海拔约2400米，一般不会有高原反应"
                    ),
                    Activity(
                        time="15:00-18:00",
                        name="丽江古城闲逛",
                        desc="世界文化遗产，有800多年历史。古城的青石板路、木结构建筑、小桥流水都很有特色。",
                        tip="古城维护费50元（进黑龙潭等景点需要）"
                    ),
                    Activity(
                        time="18:00-20:00",
                        name="晚饭",
                        desc="古城里有各种餐厅，推荐纳西菜和腊排骨火锅。",
                        tip="阿婆腊排骨“是网红店，排队严重"
                    ),
                    Activity(
                        time="20:00-22:00",
                        name="古城夜景",
                        desc='晚上的古城更有魅力，四方街有纳西族广场舞打跳，大水车是标志性打卡点。',
                        tip="酒吧一条街很热闹，但消费较高"
                    ),
                ],
                food=["腊排骨火锅", "纳西烤鱼", "鸡豆凉粉", "丽江粑粑"],
                accommodation="丽江古城内客栈（建议提前预订）",
            ),
            DayPlan(
                day_number=2,
                theme="雪山 · 玉龙冰川",
                activities=[
                    Activity(
                        time="07:00-08:00",
                        name="出发前往玉龙雪山",
                        desc="在古城忠义市场乘坐101路公交车，或包车前往。包车约100元/车。",
                        tip="早上出发可以避开人流"
                    ),
                    Activity(
                        time="08:30-10:00",
                        name="冰川公园大索道",
                        desc="乘索道到达4506米观景台，可以近距离看冰川。索道+门票+观光车140元。",
                        tip="羽绒服可以现场租，约50元"
                    ),
                    Activity(
                        time="10:00-12:00",
                        name="冰川公园徒步",
                        desc="从4506米徒步到4680米最高点，约1小时。注意不要跑跳，慢慢走。",
                        tip="多喝水，高原紫外线强"
                    ),
                    Activity(
                        time="12:30-14:30",
                        name="蓝月谷",
                        desc="雪山脚下的高原湖泊，水色碧蓝，有小九寨之称。电瓶车50元，也可步行。",
                        tip="蓝月谷的水不能喝，含有矿物质"
                    ),
                    Activity(
                        time="15:00-17:00",
                        name="观看印象丽江",
                        desc="张艺谋导演的大型实景演出，在雪山背景下非常震撼。门票220元。",
                        tip="根据个人喜好决定是否观看"
                    ),
                    Activity(
                        time="18:00-20:00",
                        name="返回古城",
                        desc="回到古城，晚饭后可以去看丽水金沙演出。",
                        tip="今天会比较累，晚上好好休息"
                    ),
                ],
                food=["雪山脚下的农家乐", "腊排骨火锅", "纳西菜"],
                accommodation="丽江古城内客栈",
            ),
            DayPlan(
                day_number=3,
                theme="纳西 · 东巴文化",
                activities=[
                    Activity(
                        time="09:00-11:00",
                        name="黑龙潭",
                        desc="古城边的公园，可以拍玉龙雪山倒影。早上人少，光线好。",
                        tip="早7点前进入免古城维护费"
                    ),
                    Activity(
                        time="11:00-13:00",
                        name="木府",
                        desc="丽江土司府邸，北有故宫南有木府。门票60元，请导游约80元。",
                        tip="《木府风云木府风云》在这里拍摄"
                    ),
                    Activity(
                        time="13:00-15:00",
                        name="午饭+休息",
                        desc="在古城吃午饭，休息到下午3点左右。",
                        tip="阿妈意是老字号纳西菜"
                    ),
                    Activity(
                        time="15:00-18:00",
                        name="束河古镇",
                        desc="茶马古道上的重要小镇，比丽江古城更安静。可以骑马或闲逛。",
                        tip=" 从丽江古城打车约15元"
                    ),
                    Activity(
                        time="18:00-20:00",
                        name="返回古城",
                        desc="回丽江古城，晚饭后可以逛忠义市场夜市。",
                        tip="忠义市场是本地人的菜市场，很接地气"
                    ),
                ],
                food=["纳西三叠水", "鸡豆凉粉", "丽江粑粑", "米灌肠"],
                accommodation="丽江古城内客栈",
            ),
            DayPlan(
                day_number=4,
                theme="泸沽湖 · 女儿国",
                activities=[
                    Activity(
                        time="06:00-13:00",
                        name="前往泸沽湖",
                        desc="从丽江到泸沽湖约200公里，车程4-5小时。沿途山路蜿蜒，风景很美。",
                        tip="建议跟一日游或包车，路况复杂"
                    ),
                    Activity(
                        time="13:30-15:30",
                        name="泸沽湖观景台",
                        desc="俯瞰泸沽湖全景的最佳位置，可以看到里格半岛的全貌。",
                        tip=" 下午的光线最好"
                    ),
                    Activity(
                        time="16:00-18:00",
                        name="环湖游玩",
                        desc="可以包车环湖，或骑单车。大落水、里格半岛、女神湾都值得看。",
                        tip="草海走婚桥是网红打卡点"
                    ),
                    Activity(
                        time="18:30-20:00",
                        name="篝火晚会",
                        desc="晚上可以参加当地的篝火晚会，感受摩梭族的热情。",
                        tip=" 一般包含在旅游团费用中"
                    ),
                ],
                food=["摩梭菜", "蒸汽石锅鱼", "猪膘肉", "咣当酒"],
                accommodation="泸沽湖大落水或里格半岛客栈",
            ),
            DayPlan(
                day_number=5,
                theme="晨曦 · 返回丽江",
                activities=[
                    Activity(
                        time="06:00-08:00",
                        name="泸沽湖日出",
                        desc="在湖边看日出，感受泸沽湖的宁静与美丽。",
                        tip="大落水是看日出的好地方"
                    ),
                    Activity(
                        time="08:00-10:00",
                        name="乘猪槽船",
                        desc="摩梭人传统的交通工具，可以泛舟湖上，去王妃岛看看。",
                        tip="王妃岛需要另外购票"
                    ),
                    Activity(
                        time="10:30-15:30",
                        name="返回丽江",
                        desc="中午返回丽江，路上吃午饭。下午在古城自由活动或购物。",
                        tip=" 带点丽江特产回去"
                    ),
                    Activity(
                        time="晚上",
                        name="返程",
                        desc="根据返程时间前往机场或火车站。",
                        tip="鲜花饼是丽江特产，建议带一些"
                    ),
                ],
                food=["摩梭菜", "腊排骨", "丽江特产"],
                accommodation="无（返程日）",
            ),
        ],
        train_route=TrainRouteInfo(
            train_no="K9625",
            from_station="东安东",
            to_station="丽江",
            depart_time="18:20",
            arrive_time="22:50+2",
            duration="76:30",
            train_type="快速列车",
            transfers=1,
            price_range="硬座¥180.5/硬卧¥373.5/软卧¥596.5",
            tips="需要在昆明或大理转车，建议飞丽江更方便"
        ),
        budget_breakdown=BudgetBreakdown(
            transport=1500,
            accommodation=600,
            food=600,
            tickets=500,
            total=3200,
        ),
        packing_list=[
            "身份证",
            "防晒霜SPF50+（高原紫外线强）",
            "墨镜",
            "厚外套（玉龙雪山很冷）",
            "舒适的步行鞋",
            "红景天（预防高原反应）",
            "润唇膏",
            "常用药品",
            "充电宝",
        ],
        tips=[
            "玉龙雪山大索道有高原反应的风险，量力而行",
            "丽江古城商业化严重，但夜景很美",
            "泸沽湖建议住一晚，看日出日落",
            "丽江早晚温差大，注意保暖",
            "丽江古城维护费50元，进景点需要",
        ],
        travel_date=None,
        season_info=None,
    )


# 热门目的地列表（用于展示）
POPULAR_DESTINATIONS = [
    {
        "name": "拉萨",
        "emoji": "🏔️",
        "desc": "世界屋脊，洗涤心灵",
        "days": 5,
        "highlights": ["布达拉宫", "纳木错", "大昭寺"],
        "key": "lhasa",
    },
    {
        "name": "成都",
        "emoji": "🐼",
        "desc": "天府之国，美食天堂",
        "days": 4,
        "highlights": ["大熊猫", "宽窄巷子", "火锅"],
        "key": "chengdu",
    },
    {
        "name": "西安",
        "emoji": "🏯",
        "desc": "千年古都，文化之旅",
        "days": 3,
        "highlights": ["兵马俑", "大雁塔", "古城墙"],
        "key": "xian",
    },
    {
        "name": "厦门",
        "emoji": "🌊",
        "desc": "海上花园，文艺清新",
        "days": 3,
        "highlights": ["鼓浪屿", "环岛路", "曾厝垵"],
        "key": "xiamen",
    },
    {
        "name": "丽江",
        "emoji": "🌸",
        "desc": "柔软时光，慢旅行",
        "days": 5,
        "highlights": ["古城", "玉龙雪山", "泸沽湖"],
        "key": "lijiang",
    },
]
