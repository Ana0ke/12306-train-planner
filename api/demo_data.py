"""
12306模拟数据 - Demo模式
预置常见路线的模拟数据，用于演示和测试
支持模糊匹配：输入"东安东→深圳"可匹配"东安东-永州"+"永州-深圳北"
"""

DEMO_DATA = {
    "东安东-永州": [
        {
            "train_no": "K580",
            "from_station": "东安东",
            "to_station": "永州",
            "depart_time": "08:15",
            "arrive_time": "08:45",
            "duration": "00:30",
            "train_type": "普速",
            "price_yz": 12.5,
            "price_rw": 54.5,
            "price_yw": 78.5,
        },
        {
            "train_no": "K9212",
            "from_station": "东安东",
            "to_station": "永州",
            "depart_time": "14:20",
            "arrive_time": "14:50",
            "duration": "00:30",
            "train_type": "普速",
            "price_yz": 12.5,
            "price_rw": 54.5,
            "price_yw": 78.5,
        },
    ],

    "永州-广州南": [
        {
            "train_no": "G6120",
            "from_station": "永州",
            "to_station": "广州南",
            "depart_time": "09:30",
            "arrive_time": "12:35",
            "duration": "03:05",
            "train_type": "高铁",
            "price_edz": 265.0,
            "price_ydz": 424.0,
            "price_swb": 843.0,
        },
        {
            "train_no": "G6128",
            "from_station": "永州",
            "to_station": "广州南",
            "depart_time": "14:10",
            "arrive_time": "17:15",
            "duration": "03:05",
            "train_type": "高铁",
            "price_edz": 265.0,
            "price_ydz": 424.0,
            "price_swb": 843.0,
        },
        {
            "train_no": "G548",
            "from_station": "永州",
            "to_station": "广州南",
            "depart_time": "16:45",
            "arrive_time": "20:00",
            "duration": "03:15",
            "train_type": "高铁",
            "price_edz": 265.0,
            "price_ydz": 424.0,
            "price_swb": 843.0,
        },
    ],

    "永州-深圳北": [
        {
            "train_no": "G6075",
            "from_station": "永州",
            "to_station": "深圳北",
            "depart_time": "10:20",
            "arrive_time": "13:45",
            "duration": "03:25",
            "train_type": "高铁",
            "price_edz": 285.0,
            "price_ydz": 455.0,
            "price_swb": 908.0,
        },
        {
            "train_no": "G6031",
            "from_station": "永州",
            "to_station": "深圳北",
            "depart_time": "15:30",
            "arrive_time": "19:00",
            "duration": "03:30",
            "train_type": "高铁",
            "price_edz": 285.0,
            "price_ydz": 455.0,
            "price_swb": 908.0,
        },
    ],

    "长沙南-广州南": [
        {
            "train_no": "6116",
            "from_station": "长沙南",
            "to_station": "广州南",
            "depart_time": "07:30",
            "arrive_time": "09:50",
            "duration": "02:20",
            "train_type": "高铁",
            "price_edz": 164.5,
            "price_ydz": 264.5,
            "price_swb": 527.0,
        },
        {
            "train_no": "G6102",
            "from_station": "长沙南",
            "to_station": "广州南",
            "depart_time": "08:15",
            "arrive_time": "10:35",
            "duration": "02:20",
            "train_type": "高铁",
            "price_edz": 164.5,
            "price_ydz": 264.5,
            "price_swb": 527.0,
        },
        {
            "train_no": "G6182",
            "from_station": "长沙南",
            "to_station": "广州南",
            "depart_time": "09:10",
            "arrive_time": "11:30",
            "duration": "02:20",
            "train_type": "高铁",
            "price_edz": 164.5,
            "price_ydz": 264.5,
            "price_swb": 527.0,
        },
        {
            "train_no": "G6142",
            "from_station": "长沙南",
            "to_station": "广州南",
            "depart_time": "14:40",
            "arrive_time": "17:00",
            "duration": "02:20",
            "train_type": "高铁",
            "price_edz": 164.5,
            "price_ydz": 264.5,
            "price_swb": 527.0,
        },
    ],

    "北京西-上海虹桥": [
        {
            "train_no": "G1",
            "from_station": "北京西",
            "to_station": "上海虹桥",
            "depart_time": "09:00",
            "arrive_time": "13:28",
            "duration": "04:28",
            "train_type": "高铁",
            "price_edz": 553.0,
            "price_ydz": 933.0,
            "price_swb": 1748.0,
        },
        {
            "train_no": "G3",
            "from_station": "北京西",
            "to_station": "上海虹桥",
            "depart_time": "10:00",
            "arrive_time": "14:29",
            "duration": "04:29",
            "train_type": "高铁",
            "price_edz": 553.0,
            "price_ydz": 933.0,
            "price_swb": 1748.0,
        },
        {
            "train_no": "G5",
            "from_station": "北京西",
            "to_station": "上海虹桥",
            "depart_time": "13:00",
            "arrive_time": "17:30",
            "duration": "04:30",
            "train_type": "高铁",
            "price_edz": 553.0,
            "price_ydz": 933.0,
            "price_swb": 1748.0,
        },
    ],

    "广州南-深圳北": [
        {
            "train_no": "G6201",
            "from_station": "广州南",
            "to_station": "深圳北",
            "depart_time": "07:30",
            "arrive_time": "08:00",
            "duration": "00:30",
            "train_type": "高铁",
            "price_edz": 74.5,
            "price_ydz": 119.5,
            "price_swb": 238.5,
        },
        {
            "train_no": "G6255",
            "from_station": "广州南",
            "to_station": "深圳北",
            "depart_time": "09:15",
            "arrive_time": "09:45",
            "duration": "00:30",
            "train_type": "高铁",
            "price_edz": 74.5,
            "price_ydz": 119.5,
            "price_swb": 238.5,
        },
        {
            "train_no": "G6541",
            "from_station": "广州南",
            "to_station": "深圳北",
            "depart_time": "18:40",
            "arrive_time": "19:10",
            "duration": "00:30",
            "train_type": "高铁",
            "price_edz": 74.5,
            "price_ydz": 119.5,
            "price_swb": 238.5,
        },
    ],

    "成都东-重庆北": [
        {
            "train_no": "G8502",
            "from_station": "成都东",
            "to_station": "重庆北",
            "depart_time": "07:00",
            "arrive_time": "08:10",
            "duration": "01:10",
            "train_type": "高铁",
            "price_edz": 154.0,
            "price_ydz": 246.5,
            "price_swb": 492.5,
        },
        {
            "train_no": "G8516",
            "from_station": "成都东",
            "to_station": "重庆北",
            "depart_time": "09:30",
            "arrive_time": "10:40",
            "duration": "01:10",
            "train_type": "高铁",
            "price_edz": 154.0,
            "price_ydz": 246.5,
            "price_swb": 492.5,
        },
        {
            "train_no": "G8540",
            "from_station": "成都东",
            "to_station": "重庆北",
            "depart_time": "16:00",
            "arrive_time": "17:10",
            "duration": "01:10",
            "train_type": "高铁",
            "price_edz": 154.0,
            "price_ydz": 246.5,
            "price_swb": 492.5,
        },
    ],

    "西安北-兰州西": [
        {
            "train_no": "G851",
            "from_station": "西安北",
            "to_station": "兰州西",
            "depart_time": "08:00",
            "arrive_time": "10:45",
            "duration": "02:45",
            "train_type": "高铁",
            "price_edz": 169.5,
            "price_ydz": 274.5,
            "price_swb": 549.0,
        },
        {
            "train_no": "G429",
            "from_station": "西安北",
            "to_station": "兰州西",
            "depart_time": "11:30",
            "arrive_time": "14:15",
            "duration": "02:45",
            "train_type": "高铁",
            "price_edz": 169.5,
            "price_ydz": 274.5,
            "price_swb": 549.0,
        },
        {
            "train_no": "G1713",
            "from_station": "西安北",
            "to_station": "兰州西",
            "depart_time": "16:20",
            "arrive_time": "19:05",
            "duration": "02:45",
            "train_type": "高铁",
            "price_edz": 169.5,
            "price_ydz": 274.5,
            "price_swb": 549.0,
        },
    ],

    "西宁-拉萨": [
        {
            "train_no": "Z265",
            "from_station": "西宁",
            "to_station": "拉萨",
            "depart_time": "12:40",
            "arrive_time": "09:55",
            "duration": "21:15",
            "train_type": "普速",
            "price_yz": 302.5,
            "price_rw": 537.5,
            "price_yw": 832.5,
        },
        {
            "train_no": "Z917",
            "from_station": "西宁",
            "to_station": "拉萨",
            "depart_time": "19:40",
            "arrive_time": "16:30",
            "duration": "20:50",
            "train_type": "普速",
            "price_yz": 302.5,
            "price_rw": 537.5,
            "price_yw": 832.5,
        },
    ],

    "北京西-西安北": [
        {
            "train_no": "G651",
            "from_station": "北京西",
            "to_station": "西安北",
            "depart_time": "10:30",
            "arrive_time": "15:10",
            "duration": "04:40",
            "train_type": "高铁",
            "price_edz": 515.5,
            "price_ydz": 824.5,
            "price_swb": 1630.5,
        },
        {
            "train_no": "G563",
            "from_station": "北京西",
            "to_station": "西安北",
            "depart_time": "14:20",
            "arrive_time": "18:55",
            "duration": "04:35",
            "train_type": "高铁",
            "price_edz": 515.5,
            "price_ydz": 824.5,
            "price_swb": 1630.5,
        },
    ],

    "上海虹桥-杭州东": [
        {
            "train_no": "7503",
            "from_station": "上海虹桥",
            "to_station": "杭州东",
            "depart_time": "08:00",
            "arrive_time": "08:50",
            "duration": "00:50",
            "train_type": "高铁",
            "price_edz": 73.0,
            "price_ydz": 117.0,
            "price_swb": 234.0,
        },
        {
            "train_no": "G7301",
            "from_station": "上海虹桥",
            "to_station": "杭州东",
            "depart_time": "10:15",
            "arrive_time": "11:05",
            "duration": "00:50",
            "train_type": "高铁",
            "price_edz": 73.0,
            "price_ydz": 117.0,
            "price_swb": 234.0,
        },
    ],

    "成都-重庆": [
        {
            "train_no": "C5765",
            "from_station": "成都",
            "to_station": "重庆",
            "depart_time": "07:30",
            "arrive_time": "10:45",
            "duration": "03:15",
            "train_type": "动车",
            "price_edz": 112.0,
            "price_ydz": 179.5,
            "price_swb": 339.5,
        },
        {
            "train_no": "C6001",
            "from_station": "成都",
            "to_station": "重庆",
            "depart_time": "13:00",
            "arrive_time": "16:15",
            "duration": "03:15",
            "train_type": "动车",
            "price_edz": 112.0,
            "price_ydz": 179.5,
            "price_swb": 339.5,
        },
    ],
}


def _stations_match(input_station: str, demo_station: str) -> bool:
    """
    判断两个站名是否匹配（支持模糊匹配）
    
    匹配规则：
    1. 精确匹配
    2. 包含匹配：输入的站名被Demo站名包含，或Demo站名被输入站名包含
    3. 部分字符匹配
    
    Args:
        input_station: 用户输入的站名
        demo_station: Demo数据中的站名
        
    Returns:
        是否匹配
    """
    if not input_station or not demo_station:
        return False
    
    # 去除空格
    input_station = input_station.strip()
    demo_station = demo_station.strip()
    
    # 1. 精确匹配
    if input_station == demo_station:
        return True
    
    # 2. 大小写无关精确匹配
    if input_station.lower() == demo_station.lower():
        return True
    
    # 3. 包含匹配：demo_station 包含 input_station
    # 例如："深圳" 匹配 "深圳北"
    if demo_station in input_station or input_station.lower() in demo_station.lower():
        return True
    
    # 4. 反向包含：input_station 包含 demo_station
    # 例如："深圳北" 匹配 "深圳"
    if input_station in demo_station:
        return True
    
    # 5. 部分字符匹配（至少2个字符）
    if len(input_station) >= 2 and len(demo_station) >= 2:
        # 取前2个字符匹配
        if input_station[:2] == demo_station[:2]:
            return True
    
    return False


def get_demo_routes(from_station: str, to_station: str) -> list[dict]:
    """
    获取模拟路线数据，支持模糊匹配站名
    
    匹配策略：
    1. 精确匹配 key（如 "东安东-永州"）
    2. 遍历所有 key，对出发站和到达站分别做包含匹配
    3. 站名 "深圳" 可匹配 "深圳北"、"深圳东" 等
    
    Args:
        from_station: 出发站
        to_station: 到达站
        
    Returns:
        车次信息列表，如果没有匹配的路线返回空列表
    """
    if not from_station or not to_station:
        return []
    
    from_station = from_station.strip()
    to_station = to_station.strip()
    
    # 1. 精确匹配 key
    key = f"{from_station}-{to_station}"
    if key in DEMO_DATA:
        return DEMO_DATA[key].copy()
    
    # 2. 遍历所有 key，进行站名模糊匹配
    for route_key, routes in DEMO_DATA.items():
        parts = route_key.split("-", 1)
        if len(parts) == 2:
            demo_from, demo_to = parts
            
            # 出发站和到达站都满足匹配关系
            from_match = _stations_match(from_station, demo_from)
            to_match = _stations_match(to_station, demo_to)
            
            if from_match and to_match:
                return routes.copy()
    
    return []


def get_demo_transfer_routes(from_station: str, to_station: str) -> tuple[list[dict], list[dict]]:
    """
    获取换乘路线数据（用于Demo模式）
    
    当直达路线不存在时，尝试查找两段式换乘方案
    
    Args:
        from_station: 出发站
        to_station: 到达站
        
    Returns:
        (第一程列表, 第二程列表)，如果找不到换乘方案则返回空列表
    """
    if not from_station or not to_station:
        return [], []
    
    from_station = from_station.strip()
    to_station = to_station.strip()
    
    # 定义可中转的枢纽站（这些站之间的数据我们有）
    transfer_hubs = ["永州", "长沙南", "广州南", "深圳北"]
    
    for hub in transfer_hubs:
        # 检查：出发站→中转站，中转站→终点站 是否都有数据
        leg1 = get_demo_routes(from_station, hub)
        leg2 = get_demo_routes(hub, to_station)
        
        if leg1 and leg2:
            return leg1, leg2
    
    return [], []


def has_demo_data(from_station: str, to_station: str) -> bool:
    """
    检查是否有模拟数据（支持模糊匹配）
    
    Args:
        from_station: 出发站
        to_station: 到达站
        
    Returns:
        是否有该路线的模拟数据
    """
    return len(get_demo_routes(from_station, to_station)) > 0


def get_all_demo_routes() -> dict:
    """获取所有Demo路线数据"""
    return DEMO_DATA.copy()
