"""
12306模拟数据 - Demo模式
预置常见路线的模拟数据，用于演示和测试
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

    # 添加更多热门路线
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


def get_demo_routes(from_station: str, to_station: str) -> list[dict]:
    """
    获取模拟路线数据
    
    Args:
        from_station: 出发站
        to_station: 到达站
        
    Returns:
        车次信息列表，如果没有匹配的路线返回空列表
    """
    key = f"{from_station}-{to_station}"
    return DEMO_DATA.get(key, []).copy()


def has_demo_data(from_station: str, to_station: str) -> bool:
    """
    检查是否有模拟数据
    
    Args:
        from_station: 出发站
        to_station: 到达站
        
    Returns:
        是否有该路线的模拟数据
    """
    key = f"{from_station}-{to_station}"
    return key in DEMO_DATA