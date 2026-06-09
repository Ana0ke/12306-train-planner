"""
12306模拟数据 - Demo模式
预置热门路线的模拟数据，用于演示和测试
支持模糊匹配站名和换乘路线自动拼接

扩充至40+条热门路线，覆盖全国主要省会城市互达
"""

# 所有可用中转枢纽站（保持与planner.py、transfer.py一致）
TRANSFER_HUBS = [
    "北京", "北京西", "北京南",
    "上海", "上海虹桥",
    "广州", "广州南",
    "深圳", "深圳北",
    "武汉", "汉口", "武昌",
    "长沙", "长沙南",
    "成都", "成都东",
    "重庆", "重庆北", "重庆西",
    "西安", "西安北",
    "郑州", "郑州东",
    "南京", "南京南",
    "杭州", "杭州东",
    "合肥",
    "贵阳", "贵阳北",
    "昆明", "昆明南",
    "南昌", "南昌西",
    "济南", "济南西",
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

DEMO_DATA = {
    # ===== 华北区域 =====
    "北京-上海虹桥": [
        {"train_no": "G1", "from_station": "北京南", "to_station": "上海虹桥", "depart_time": "09:00", "arrive_time": "13:28", "duration": "04:28", "train_type": "高铁", "price_edz": 553.0, "price_ydz": 933.0, "price_swb": 1748.0},
        {"train_no": "G3", "from_station": "北京南", "to_station": "上海虹桥", "depart_time": "10:00", "arrive_time": "14:29", "duration": "04:29", "train_type": "高铁", "price_edz": 553.0, "price_ydz": 933.0, "price_swb": 1748.0},
        {"train_no": "G5", "from_station": "北京南", "to_station": "上海虹桥", "depart_time": "14:00", "arrive_time": "18:29", "duration": "04:29", "train_type": "高铁", "price_edz": 553.0, "price_ydz": 933.0, "price_swb": 1748.0},
    ],
    "北京南-上海虹桥": [
        {"train_no": "G1", "from_station": "北京南", "to_station": "上海虹桥", "depart_time": "09:00", "arrive_time": "13:28", "duration": "04:28", "train_type": "高铁", "price_edz": 553.0, "price_ydz": 933.0, "price_swb": 1748.0},
        {"train_no": "G3", "from_station": "北京南", "to_station": "上海虹桥", "depart_time": "10:00", "arrive_time": "14:29", "duration": "04:29", "train_type": "高铁", "price_edz": 553.0, "price_ydz": 933.0, "price_swb": 1748.0},
        {"train_no": "G7", "from_station": "北京南", "to_station": "上海虹桥", "depart_time": "19:00", "arrive_time": "23:29", "duration": "04:29", "train_type": "高铁", "price_edz": 553.0, "price_ydz": 933.0, "price_swb": 1748.0},
    ],
    "北京西-西安北": [
        {"train_no": "G651", "from_station": "北京西", "to_station": "西安北", "depart_time": "07:30", "arrive_time": "12:10", "duration": "04:40", "train_type": "高铁", "price_edz": 515.5, "price_ydz": 824.5, "price_swb": 1630.5},
        {"train_no": "G87", "from_station": "北京西", "to_station": "西安北", "depart_time": "14:00", "arrive_time": "18:20", "duration": "04:20", "train_type": "高铁", "price_edz": 515.5, "price_ydz": 824.5, "price_swb": 1630.5},
        {"train_no": "G59", "from_station": "北京西", "to_station": "西安北", "depart_time": "18:00", "arrive_time": "22:30", "duration": "04:30", "train_type": "高铁", "price_edz": 515.5, "price_ydz": 824.5, "price_swb": 1630.5},
    ],
    "北京-石家庄": [
        {"train_no": "G71", "from_station": "北京西", "to_station": "石家庄", "depart_time": "07:00", "arrive_time": "08:08", "duration": "01:08", "train_type": "高铁", "price_edz": 128.5, "price_ydz": 209.5, "price_swb": 400.5},
        {"train_no": "G89", "from_station": "北京西", "to_station": "石家庄", "depart_time": "09:00", "arrive_time": "10:08", "duration": "01:08", "train_type": "高铁", "price_edz": 128.5, "price_ydz": 209.5, "price_swb": 400.5},
        {"train_no": "G6733", "from_station": "北京西", "to_station": "石家庄", "depart_time": "19:30", "arrive_time": "20:38", "duration": "01:08", "train_type": "高铁", "price_edz": 128.5, "price_ydz": 209.5, "price_swb": 400.5},
    ],
    "石家庄-太原": [
        {"train_no": "G609", "from_station": "石家庄", "to_station": "太原", "depart_time": "08:00", "arrive_time": "09:50", "duration": "01:50", "train_type": "高铁", "price_edz": 68.0, "price_ydz": 113.0, "price_swb": 206.0},
        {"train_no": "G615", "from_station": "石家庄", "to_station": "太原", "depart_time": "14:00", "arrive_time": "15:50", "duration": "01:50", "train_type": "高铁", "price_edz": 68.0, "price_ydz": 113.0, "price_swb": 206.0},
    ],
    "北京-太原": [
        {"train_no": "G601", "from_station": "北京西", "to_station": "太原", "depart_time": "08:00", "arrive_time": "11:30", "duration": "03:30", "train_type": "高铁", "price_edz": 232.5, "price_ydz": 384.5, "price_swb": 727.5},
        {"train_no": "G605", "from_station": "北京西", "to_station": "太原", "depart_time": "16:00", "arrive_time": "19:30", "duration": "03:30", "train_type": "高铁", "price_edz": 232.5, "price_ydz": 384.5, "price_swb": 727.5},
    ],

    # ===== 华东区域 =====
    "上海虹桥-杭州东": [
        {"train_no": "G7503", "from_station": "上海虹桥", "to_station": "杭州东", "depart_time": "08:00", "arrive_time": "08:50", "duration": "00:50", "train_type": "高铁", "price_edz": 73.0, "price_ydz": 117.0, "price_swb": 234.0},
        {"train_no": "G7535", "from_station": "上海虹桥", "to_station": "杭州东", "depart_time": "10:00", "arrive_time": "10:50", "duration": "00:50", "train_type": "高铁", "price_edz": 73.0, "price_ydz": 117.0, "price_swb": 234.0},
        {"train_no": "G7557", "from_station": "上海虹桥", "to_station": "杭州东", "depart_time": "14:00", "arrive_time": "14:50", "duration": "00:50", "train_type": "高铁", "price_edz": 73.0, "price_ydz": 117.0, "price_swb": 234.0},
        {"train_no": "G7337", "from_station": "上海虹桥", "to_station": "杭州东", "depart_time": "18:30", "arrive_time": "19:20", "duration": "00:50", "train_type": "高铁", "price_edz": 73.0, "price_ydz": 117.0, "price_swb": 234.0},
    ],
    "杭州东-南京南": [
        {"train_no": "G7562", "from_station": "杭州东", "to_station": "南京南", "depart_time": "07:15", "arrive_time": "08:35", "duration": "01:20", "train_type": "高铁", "price_edz": 117.5, "price_ydz": 197.5, "price_swb": 366.5},
        {"train_no": "G7566", "from_station": "杭州东", "to_station": "南京南", "depart_time": "10:00", "arrive_time": "11:20", "duration": "01:20", "train_type": "高铁", "price_edz": 117.5, "price_ydz": 197.5, "price_swb": 366.5},
        {"train_no": "G7572", "from_station": "杭州东", "to_station": "南京南", "depart_time": "16:30", "arrive_time": "17:50", "duration": "01:20", "train_type": "高铁", "price_edz": 117.5, "price_ydz": 197.5, "price_swb": 366.5},
    ],
    "南京-合肥": [
        {"train_no": "G7275", "from_station": "南京", "to_station": "合肥", "depart_time": "08:00", "arrive_time": "09:20", "duration": "01:20", "train_type": "高铁", "price_edz": 79.5, "price_ydz": 129.5, "price_swb": 249.5},
        {"train_no": "G7281", "from_station": "南京", "to_station": "合肥", "depart_time": "12:00", "arrive_time": "13:20", "duration": "01:20", "train_type": "高铁", "price_edz": 79.5, "price_ydz": 129.5, "price_swb": 249.5},
        {"train_no": "G7293", "from_station": "南京", "to_station": "合肥", "depart_time": "18:30", "arrive_time": "19:50", "duration": "01:20", "train_type": "高铁", "price_edz": 79.5, "price_ydz": 129.5, "price_swb": 249.5},
    ],
    "上海-南京": [
        {"train_no": "G7002", "from_station": "上海", "to_station": "南京", "depart_time": "07:00", "arrive_time": "09:00", "duration": "02:00", "train_type": "高铁", "price_edz": 134.5, "price_ydz": 224.5, "price_swb": 429.5},
        {"train_no": "G7006", "from_station": "上海", "to_station": "南京", "depart_time": "10:00", "arrive_time": "12:00", "duration": "02:00", "train_type": "高铁", "price_edz": 134.5, "price_ydz": 224.5, "price_swb": 429.5},
        {"train_no": "G7010", "from_station": "上海", "to_station": "南京", "depart_time": "16:00", "arrive_time": "18:00", "duration": "02:00", "train_type": "高铁", "price_edz": 134.5, "price_ydz": 224.5, "price_swb": 429.5},
    ],
    "济南-青岛": [
        {"train_no": "G6901", "from_station": "济南", "to_station": "青岛", "depart_time": "07:00", "arrive_time": "09:00", "duration": "02:00", "train_type": "高铁", "price_edz": 119.5, "price_ydz": 194.5, "price_swb": 374.5},
        {"train_no": "G6911", "from_station": "济南", "to_station": "青岛", "depart_time": "11:00", "arrive_time": "13:00", "duration": "02:00", "train_type": "高铁", "price_edz": 119.5, "price_ydz": 194.5, "price_swb": 374.5},
        {"train_no": "G6903", "from_station": "济南", "to_station": "青岛", "depart_time": "18:00", "arrive_time": "20:00", "duration": "02:00", "train_type": "高铁", "price_edz": 119.5, "price_ydz": 194.5, "price_swb": 374.5},
    ],
    "福州-厦门": [
        {"train_no": "D6201", "from_station": "福州", "to_station": "厦门", "depart_time": "07:00", "arrive_time": "09:00", "duration": "02:00", "train_type": "动车", "price_edz": 84.5, "price_ydz": 135.5, "price_swb": 259.5},
        {"train_no": "D6213", "from_station": "福州", "to_station": "厦门", "depart_time": "11:00", "arrive_time": "13:00", "duration": "02:00", "train_type": "动车", "price_edz": 84.5, "price_ydz": 135.5, "price_swb": 259.5},
        {"train_no": "D6219", "from_station": "福州", "to_station": "厦门", "depart_time": "17:30", "arrive_time": "19:30", "duration": "02:00", "train_type": "动车", "price_edz": 84.5, "price_ydz": 135.5, "price_swb": 259.5},
    ],

    # ===== 华中区域 =====
    "武汉-长沙南": [
        {"train_no": "G1001", "from_station": "武汉", "to_station": "长沙南", "depart_time": "08:00", "arrive_time": "09:20", "duration": "01:20", "train_type": "高铁", "price_edz": 164.5, "price_ydz": 264.5, "price_swb": 527.0},
        {"train_no": "G1003", "from_station": "武汉", "to_station": "长沙南", "depart_time": "10:00", "arrive_time": "11:20", "duration": "01:20", "train_type": "高铁", "price_edz": 164.5, "price_ydz": 264.5, "price_swb": 527.0},
        {"train_no": "G1005", "from_station": "武汉", "to_station": "长沙南", "depart_time": "14:00", "arrive_time": "15:20", "duration": "01:20", "train_type": "高铁", "price_edz": 164.5, "price_ydz": 264.5, "price_swb": 527.0},
        {"train_no": "G1007", "from_station": "武汉", "to_station": "长沙南", "depart_time": "18:30", "arrive_time": "19:50", "duration": "01:20", "train_type": "高铁", "price_edz": 164.5, "price_ydz": 264.5, "price_swb": 527.0},
    ],
    "武汉-广州南": [
        {"train_no": "G1001", "from_station": "武汉", "to_station": "广州南", "depart_time": "07:30", "arrive_time": "11:00", "duration": "03:30", "train_type": "高铁", "price_edz": 463.5, "price_ydz": 738.5, "price_swb": 1388.5},
        {"train_no": "G1003", "from_station": "武汉", "to_station": "广州南", "depart_time": "09:00", "arrive_time": "12:25", "duration": "03:25", "train_type": "高铁", "price_edz": 463.5, "price_ydz": 738.5, "price_swb": 1388.5},
        {"train_no": "G1007", "from_station": "武汉", "to_station": "广州南", "depart_time": "14:30", "arrive_time": "17:55", "duration": "03:25", "train_type": "高铁", "price_edz": 463.5, "price_ydz": 738.5, "price_swb": 1388.5},
    ],
    "武汉-郑州": [
        {"train_no": "G850", "from_station": "武汉", "to_station": "郑州东", "depart_time": "08:00", "arrive_time": "10:00", "duration": "02:00", "train_type": "高铁", "price_edz": 244.5, "price_ydz": 389.5, "price_swb": 749.5},
        {"train_no": "G856", "from_station": "武汉", "to_station": "郑州东", "depart_time": "12:00", "arrive_time": "14:00", "duration": "02:00", "train_type": "高铁", "price_edz": 244.5, "price_ydz": 389.5, "price_swb": 749.5},
        {"train_no": "G862", "from_station": "武汉", "to_station": "郑州东", "depart_time": "17:00", "arrive_time": "19:00", "duration": "02:00", "train_type": "高铁", "price_edz": 244.5, "price_ydz": 389.5, "price_swb": 749.5},
    ],
    "武汉-南昌": [
        {"train_no": "G647", "from_station": "武汉", "to_station": "南昌西", "depart_time": "08:30", "arrive_time": "11:30", "duration": "03:00", "train_type": "高铁", "price_edz": 204.5, "price_ydz": 329.5, "price_swb": 634.5},
        {"train_no": "G649", "from_station": "武汉", "to_station": "南昌西", "depart_time": "14:00", "arrive_time": "17:00", "duration": "03:00", "train_type": "高铁", "price_edz": 204.5, "price_ydz": 329.5, "price_swb": 634.5},
    ],
    "西安-郑州": [
        {"train_no": "G2001", "from_station": "西安北", "to_station": "郑州东", "depart_time": "08:00", "arrive_time": "10:30", "duration": "02:30", "train_type": "高铁", "price_edz": 229.5, "price_ydz": 369.5, "price_swb": 714.5},
        {"train_no": "G2003", "from_station": "西安北", "to_station": "郑州东", "depart_time": "11:00", "arrive_time": "13:30", "duration": "02:30", "train_type": "高铁", "price_edz": 229.5, "price_ydz": 369.5, "price_swb": 714.5},
        {"train_no": "G2005", "from_station": "西安北", "to_station": "郑州东", "depart_time": "16:00", "arrive_time": "18:30", "duration": "02:30", "train_type": "高铁", "price_edz": 229.5, "price_ydz": 369.5, "price_swb": 714.5},
    ],

    # ===== 华南区域 =====
    "广州南-长沙南": [
        {"train_no": "G6101", "from_station": "广州南", "to_station": "长沙南", "depart_time": "07:00", "arrive_time": "09:20", "duration": "02:20", "train_type": "高铁", "price_edz": 164.5, "price_ydz": 264.5, "price_swb": 527.0},
        {"train_no": "G6105", "from_station": "广州南", "to_station": "长沙南", "depart_time": "10:30", "arrive_time": "12:50", "duration": "02:20", "train_type": "高铁", "price_edz": 164.5, "price_ydz": 264.5, "price_swb": 527.0},
        {"train_no": "G6145", "from_station": "广州南", "to_station": "长沙南", "depart_time": "16:00", "arrive_time": "18:20", "duration": "02:20", "train_type": "高铁", "price_edz": 164.5, "price_ydz": 264.5, "price_swb": 527.0},
        {"train_no": "G6165", "from_station": "广州南", "to_station": "长沙南", "depart_time": "20:00", "arrive_time": "22:20", "duration": "02:20", "train_type": "高铁", "price_edz": 164.5, "price_ydz": 264.5, "price_swb": 527.0},
    ],
    "广州南-深圳北": [
        {"train_no": "G6201", "from_station": "广州南", "to_station": "深圳北", "depart_time": "07:30", "arrive_time": "08:00", "duration": "00:30", "train_type": "高铁", "price_edz": 74.5, "price_ydz": 119.5, "price_swb": 238.5},
        {"train_no": "G6255", "from_station": "广州南", "to_station": "深圳北", "depart_time": "09:15", "arrive_time": "09:45", "duration": "00:30", "train_type": "高铁", "price_edz": 74.5, "price_ydz": 119.5, "price_swb": 238.5},
        {"train_no": "G6541", "from_station": "广州南", "to_station": "深圳北", "depart_time": "18:40", "arrive_time": "19:10", "duration": "00:30", "train_type": "高铁", "price_edz": 74.5, "price_ydz": 119.5, "price_swb": 238.5},
        {"train_no": "G6545", "from_station": "广州南", "to_station": "深圳北", "depart_time": "21:00", "arrive_time": "21:30", "duration": "00:30", "train_type": "高铁", "price_edz": 74.5, "price_ydz": 119.5, "price_swb": 238.5},
    ],
    "广州南-贵阳北": [
        {"train_no": "D2803", "from_station": "广州南", "to_station": "贵阳北", "depart_time": "07:00", "arrive_time": "11:00", "duration": "04:00", "train_type": "动车", "price_edz": 323.5, "price_ydz": 515.5, "price_swb": 991.5},
        {"train_no": "D2814", "from_station": "广州南", "to_station": "贵阳北", "depart_time": "10:00", "arrive_time": "14:00", "duration": "04:00", "train_type": "动车", "price_edz": 323.5, "price_ydz": 515.5, "price_swb": 991.5},
        {"train_no": "D2820", "from_station": "广州南", "to_station": "贵阳北", "depart_time": "14:00", "arrive_time": "18:00", "duration": "04:00", "train_type": "动车", "price_edz": 323.5, "price_ydz": 515.5, "price_swb": 991.5},
    ],
    "深圳北-厦门北": [
        {"train_no": "D2318", "from_station": "深圳北", "to_station": "厦门北", "depart_time": "07:45", "arrive_time": "10:22", "duration": "02:37", "train_type": "动车", "price_edz": 150.0, "price_ydz": 240.0, "price_swb": 450.0},
        {"train_no": "D2322", "from_station": "深圳北", "to_station": "厦门北", "depart_time": "11:00", "arrive_time": "13:37", "duration": "02:37", "train_type": "动车", "price_edz": 150.0, "price_ydz": 240.0, "price_swb": 450.0},
        {"train_no": "D2326", "from_station": "深圳北", "to_station": "厦门北", "depart_time": "16:00", "arrive_time": "18:37", "duration": "02:37", "train_type": "动车", "price_edz": 150.0, "price_ydz": 240.0, "price_swb": 450.0},
    ],
    "长沙南-广州南": [
        {"train_no": "G6102", "from_station": "长沙南", "to_station": "广州南", "depart_time": "07:30", "arrive_time": "09:50", "duration": "02:20", "train_type": "高铁", "price_edz": 164.5, "price_ydz": 264.5, "price_swb": 527.0},
        {"train_no": "G6118", "from_station": "长沙南", "to_station": "广州南", "depart_time": "08:15", "arrive_time": "10:35", "duration": "02:20", "train_type": "高铁", "price_edz": 164.5, "price_ydz": 264.5, "price_swb": 527.0},
        {"train_no": "G6142", "from_station": "长沙南", "to_station": "广州南", "depart_time": "14:40", "arrive_time": "17:00", "duration": "02:20", "train_type": "高铁", "price_edz": 164.5, "price_ydz": 264.5, "price_swb": 527.0},
        {"train_no": "G6186", "from_station": "长沙南", "to_station": "广州南", "depart_time": "19:00", "arrive_time": "21:20", "duration": "02:20", "train_type": "高铁", "price_edz": 164.5, "price_ydz": 264.5, "price_swb": 527.0},
    ],
    "长沙-南昌": [
        {"train_no": "G1433", "from_station": "长沙南", "to_station": "南昌西", "depart_time": "08:30", "arrive_time": "11:00", "duration": "02:30", "train_type": "高铁", "price_edz": 157.0, "price_ydz": 252.0, "price_swb": 489.0},
        {"train_no": "G1435", "from_station": "长沙南", "to_station": "南昌西", "depart_time": "14:00", "arrive_time": "16:30", "duration": "02:30", "train_type": "高铁", "price_edz": 157.0, "price_ydz": 252.0, "price_swb": 489.0},
    ],
    "南宁-海口": [
        {"train_no": "D3601", "from_station": "南宁东", "to_station": "海口", "depart_time": "08:00", "arrive_time": "12:30", "duration": "04:30", "train_type": "动车", "price_edz": 242.0, "price_ydz": 389.0, "price_swb": 731.0},
        {"train_no": "D3611", "from_station": "南宁东", "to_station": "海口", "depart_time": "13:00", "arrive_time": "17:30", "duration": "04:30", "train_type": "动车", "price_edz": 242.0, "price_ydz": 389.0, "price_swb": 731.0},
    ],

    # ===== 西南区域 =====
    "成都东-重庆北": [
        {"train_no": "G8502", "from_station": "成都东", "to_station": "重庆北", "depart_time": "07:00", "arrive_time": "08:10", "duration": "01:10", "train_type": "高铁", "price_edz": 154.0, "price_ydz": 246.5, "price_swb": 492.5},
        {"train_no": "G8516", "from_station": "成都东", "to_station": "重庆北", "depart_time": "09:30", "arrive_time": "10:40", "duration": "01:10", "train_type": "高铁", "price_edz": 154.0, "price_ydz": 246.5, "price_swb": 492.5},
        {"train_no": "G8540", "from_station": "成都东", "to_station": "重庆北", "depart_time": "16:00", "arrive_time": "17:10", "duration": "01:10", "train_type": "高铁", "price_edz": 154.0, "price_ydz": 246.5, "price_swb": 492.5},
        {"train_no": "G8544", "from_station": "成都东", "to_station": "重庆北", "depart_time": "20:00", "arrive_time": "21:10", "duration": "01:10", "train_type": "高铁", "price_edz": 154.0, "price_ydz": 246.5, "price_swb": 492.5},
    ],
    "成都-重庆": [
        {"train_no": "C5765", "from_station": "成都东", "to_station": "重庆北", "depart_time": "07:30", "arrive_time": "10:45", "duration": "03:15", "train_type": "动车", "price_edz": 112.0, "price_ydz": 179.5, "price_swb": 339.5},
        {"train_no": "C6001", "from_station": "成都东", "to_station": "重庆北", "depart_time": "13:00", "arrive_time": "16:15", "duration": "03:15", "train_type": "动车", "price_edz": 112.0, "price_ydz": 179.5, "price_swb": 339.5},
    ],
    "成都东-贵阳北": [
        {"train_no": "G8651", "from_station": "成都东", "to_station": "贵阳北", "depart_time": "08:00", "arrive_time": "12:30", "duration": "04:30", "train_type": "高铁", "price_edz": 304.0, "price_ydz": 487.0, "price_swb": 974.0},
        {"train_no": "G8655", "from_station": "成都东", "to_station": "贵阳北", "depart_time": "12:00", "arrive_time": "16:30", "duration": "04:30", "train_type": "高铁", "price_edz": 304.0, "price_ydz": 487.0, "price_swb": 974.0},
    ],
    "昆明南-贵阳": [
        {"train_no": "G2963", "from_station": "昆明南", "to_station": "贵阳北", "depart_time": "08:00", "arrive_time": "10:30", "duration": "02:30", "train_type": "高铁", "price_edz": 212.5, "price_ydz": 340.5, "price_swb": 681.5},
        {"train_no": "G2965", "from_station": "昆明南", "to_station": "贵阳北", "depart_time": "13:00", "arrive_time": "15:30", "duration": "02:30", "train_type": "高铁", "price_edz": 212.5, "price_ydz": 340.5, "price_swb": 681.5},
        {"train_no": "G2967", "from_station": "昆明南", "to_station": "贵阳北", "depart_time": "18:00", "arrive_time": "20:30", "duration": "02:30", "train_type": "高铁", "price_edz": 212.5, "price_ydz": 340.5, "price_swb": 681.5},
    ],
    "昆明南-大理": [
        {"train_no": "D8692", "from_station": "昆明南", "to_station": "大理", "depart_time": "07:20", "arrive_time": "09:55", "duration": "02:35", "train_type": "动车", "price_edz": 145.0, "price_ydz": 232.0, "price_swb": 435.0},
        {"train_no": "D8696", "from_station": "昆明南", "to_station": "大理", "depart_time": "10:30", "arrive_time": "13:05", "duration": "02:35", "train_type": "动车", "price_edz": 145.0, "price_ydz": 232.0, "price_swb": 435.0},
        {"train_no": "D8702", "from_station": "昆明南", "to_station": "大理", "depart_time": "15:00", "arrive_time": "17:35", "duration": "02:35", "train_type": "动车", "price_edz": 145.0, "price_ydz": 232.0, "price_swb": 435.0},
        {"train_no": "D8706", "from_station": "昆明南", "to_station": "大理", "depart_time": "19:00", "arrive_time": "21:35", "duration": "02:35", "train_type": "动车", "price_edz": 145.0, "price_ydz": 232.0, "price_swb": 435.0},
    ],

    # ===== 西北区域 =====
    "西安北-兰州西": [
        {"train_no": "G851", "from_station": "西安北", "to_station": "兰州西", "depart_time": "08:00", "arrive_time": "10:45", "duration": "02:45", "train_type": "高铁", "price_edz": 169.5, "price_ydz": 274.5, "price_swb": 549.0},
        {"train_no": "G429", "from_station": "西安北", "to_station": "兰州西", "depart_time": "11:30", "arrive_time": "14:15", "duration": "02:45", "train_type": "高铁", "price_edz": 169.5, "price_ydz": 274.5, "price_swb": 549.0},
        {"train_no": "G1713", "from_station": "西安北", "to_station": "兰州西", "depart_time": "16:20", "arrive_time": "19:05", "duration": "02:45", "train_type": "高铁", "price_edz": 169.5, "price_ydz": 274.5, "price_swb": 549.0},
    ],
    "兰州-西宁": [
        {"train_no": "D55", "from_station": "兰州西", "to_station": "西宁", "depart_time": "08:00", "arrive_time": "09:20", "duration": "01:20", "train_type": "动车", "price_edz": 58.0, "price_ydz": 93.0, "price_swb": 186.0},
        {"train_no": "D267", "from_station": "兰州西", "to_station": "西宁", "depart_time": "14:00", "arrive_time": "15:20", "duration": "01:20", "train_type": "动车", "price_edz": 58.0, "price_ydz": 93.0, "price_swb": 186.0},
        {"train_no": "D2711", "from_station": "兰州西", "to_station": "西宁", "depart_time": "19:00", "arrive_time": "20:20", "duration": "01:20", "train_type": "动车", "price_edz": 58.0, "price_ydz": 93.0, "price_swb": 186.0},
    ],
    "西宁-拉萨": [
        {"train_no": "Z265", "from_station": "西宁", "to_station": "拉萨", "depart_time": "12:40", "arrive_time": "09:55", "duration": "21:15", "train_type": "普速", "price_yz": 302.5, "price_rw": 537.5, "price_yw": 832.5},
        {"train_no": "Z917", "from_station": "西宁", "to_station": "拉萨", "depart_time": "19:40", "arrive_time": "16:30", "duration": "20:50", "train_type": "普速", "price_yz": 302.5, "price_rw": 537.5, "price_yw": 832.5},
    ],
    "西安-乌鲁木齐": [
        {"train_no": "K4629", "from_station": "西安", "to_station": "乌鲁木齐", "depart_time": "12:00", "arrive_time": "09:00", "duration": "21:00", "train_type": "普速", "price_yz": 236.5, "price_rw": 415.5, "price_yw": 648.5},
    ],

    # ===== 东北区域 =====
    "沈阳-大连": [
        {"train_no": "G8002", "from_station": "沈阳", "to_station": "大连", "depart_time": "07:00", "arrive_time": "09:00", "duration": "02:00", "train_type": "高铁", "price_edz": 175.0, "price_ydz": 280.0, "price_swb": 545.0},
        {"train_no": "G8020", "from_station": "沈阳", "to_station": "大连", "depart_time": "12:00", "arrive_time": "14:00", "duration": "02:00", "train_type": "高铁", "price_edz": 175.0, "price_ydz": 280.0, "price_swb": 545.0},
        {"train_no": "G8050", "from_station": "沈阳", "to_station": "大连", "depart_time": "18:00", "arrive_time": "20:00", "duration": "02:00", "train_type": "高铁", "price_edz": 175.0, "price_ydz": 280.0, "price_swb": 545.0},
    ],
    "哈尔滨-长春": [
        {"train_no": "G703", "from_station": "哈尔滨西", "to_station": "长春", "depart_time": "08:00", "arrive_time": "09:00", "duration": "01:00", "train_type": "高铁", "price_edz": 109.5, "price_ydz": 174.5, "price_swb": 344.5},
        {"train_no": "G719", "from_station": "哈尔滨西", "to_station": "长春", "depart_time": "12:00", "arrive_time": "13:00", "duration": "01:00", "train_type": "高铁", "price_edz": 109.5, "price_ydz": 174.5, "price_swb": 344.5},
        {"train_no": "G729", "from_station": "哈尔滨西", "to_station": "长春", "depart_time": "18:00", "arrive_time": "19:00", "duration": "01:00", "train_type": "高铁", "price_edz": 109.5, "price_ydz": 174.5, "price_swb": 344.5},
    ],
    "沈阳北-哈尔滨": [
        {"train_no": "G800", "from_station": "沈阳北", "to_station": "哈尔滨西", "depart_time": "08:00", "arrive_time": "10:30", "duration": "02:30", "train_type": "高铁", "price_edz": 217.0, "price_ydz": 347.0, "price_swb": 694.0},
        {"train_no": "G804", "from_station": "沈阳北", "to_station": "哈尔滨西", "depart_time": "14:00", "arrive_time": "16:30", "duration": "02:30", "train_type": "高铁", "price_edz": 217.0, "price_ydz": 347.0, "price_swb": 694.0},
    ],

    # ===== 跨区域重要线路 =====
    "北京-广州": [
        {"train_no": "G71", "from_station": "北京西", "to_station": "广州南", "depart_time": "08:00", "arrive_time": "17:00", "duration": "09:00", "train_type": "高铁", "price_edz": 862.0, "price_ydz": 1380.0, "price_swb": 2732.0},
        {"train_no": "G79", "from_station": "北京西", "to_station": "广州南", "depart_time": "10:00", "arrive_time": "18:50", "duration": "08:50", "train_type": "高铁", "price_edz": 862.0, "price_ydz": 1380.0, "price_swb": 2732.0},
    ],
    "上海-广州": [
        {"train_no": "G85", "from_station": "上海虹桥", "to_station": "广州南", "depart_time": "08:00", "arrive_time": "16:30", "duration": "08:30", "train_type": "高铁", "price_edz": 793.0, "price_ydz": 1269.0, "price_swb": 2518.0},
        {"train_no": "G87", "from_station": "上海虹桥", "to_station": "广州南", "depart_time": "14:00", "arrive_time": "22:30", "duration": "08:30", "train_type": "高铁", "price_edz": 793.0, "price_ydz": 1269.0, "price_swb": 2518.0},
    ],
    "广州-成都": [
        {"train_no": "D1762", "from_station": "广州南", "to_station": "成都东", "depart_time": "08:00", "arrive_time": "18:00", "duration": "10:00", "train_type": "动车", "price_edz": 643.0, "price_ydz": 1029.0, "price_swb": 2048.0},
    ],
    "北京-成都": [
        {"train_no": "G87", "from_station": "北京西", "to_station": "成都东", "depart_time": "08:00", "arrive_time": "18:00", "duration": "10:00", "train_type": "高铁", "price_edz": 809.5, "price_ydz": 1296.5, "price_swb": 2573.5},
        {"train_no": "G89", "from_station": "北京西", "to_station": "成都东", "depart_time": "14:00", "arrive_time": "23:30", "duration": "09:30", "train_type": "高铁", "price_edz": 809.5, "price_ydz": 1296.5, "price_swb": 2573.5},
    ],
    "上海-成都": [
        {"train_no": "G1974", "from_station": "上海虹桥", "to_station": "成都东", "depart_time": "06:00", "arrive_time": "18:00", "duration": "12:00", "train_type": "高铁", "price_edz": 1095.5, "price_ydz": 1753.5, "price_swb": 3487.5},
    ],
    "北京-上海": [
        {"train_no": "G1", "from_station": "北京南", "to_station": "上海虹桥", "depart_time": "09:00", "arrive_time": "13:28", "duration": "04:28", "train_type": "高铁", "price_edz": 553.0, "price_ydz": 933.0, "price_swb": 1748.0},
        {"train_no": "G3", "from_station": "北京南", "to_station": "上海虹桥", "depart_time": "14:00", "arrive_time": "18:29", "duration": "04:29", "train_type": "高铁", "price_edz": 553.0, "price_ydz": 933.0, "price_swb": 1748.0},
        {"train_no": "G5", "from_station": "北京南", "to_station": "上海虹桥", "depart_time": "19:00", "arrive_time": "23:29", "duration": "04:29", "train_type": "高铁", "price_edz": 553.0, "price_ydz": 933.0, "price_swb": 1748.0},
    ],
}


def _match_priority(input_station: str, demo_station: str) -> int:
    """
    判断匹配优先级，用于排序
    
    优先级（数字越小优先级越高）：
    0 - 完全匹配
    1 - 精确大小写匹配
    2 - 输入是站名的前缀（输入>=3字）
    3 - 站名是输入的前缀（输入>=3字）
    4 - 输入包含站名（输入>=3字）
    5 - 站名包含输入（输入>=3字）
    6 - 前2字匹配
    -1 - 不匹配
    
    Args:
        input_station: 用户输入的站名
        demo_station: Demo数据中的站名
        
    Returns:
        优先级数字，不匹配返回-1
    """
    if not input_station or not demo_station:
        return -1
    
    # 去除空格
    input_station = input_station.strip()
    demo_station = demo_station.strip()
    
    # 0. 完全匹配
    if input_station == demo_station:
        return 0
    
    # 1. 大小写无关完全匹配
    if input_station.lower() == demo_station.lower():
        return 1
    
    # 以下规则仅在输入长度>=3时启用
    if len(input_station) >= 3 and len(demo_station) >= 3:
        # 2. 输入是站名的前缀（如"北京"匹配"北京西"）
        if demo_station.startswith(input_station):
            return 2
        
        # 3. 站名是输入的前缀（如"北京西"匹配"北京"）
        if input_station.startswith(demo_station):
            return 3
        
        # 4. 输入包含站名（如"北京"在"北京西"中）
        if input_station in demo_station:
            return 4
        
        # 5. 站名包含输入（如"北京西"包含"北京"）
        if demo_station in input_station:
            return 5
    
    # 6. 前2字匹配（作为最低优先级兜底）
    if len(input_station) >= 2 and len(demo_station) >= 2:
        if input_station[:2] == demo_station[:2]:
            return 6
    
    return -1


def _stations_match(input_station: str, demo_station: str) -> bool:
    """
    判断两个站名是否匹配（支持模糊匹配）
    
    匹配规则（分级匹配）：
    1. 完全匹配（最高优先级）
    2. 输入是站名的前缀（至少3个字）
    3. 站名是输入的前缀（至少3个字）
    4. 输入包含站名（至少3个字）
    5. 站名包含输入（至少3个字）
    6. 前2字匹配（最低优先级）
    
    Args:
        input_station: 用户输入的站名
        demo_station: Demo数据中的站名
        
    Returns:
        是否匹配
    """
    return _match_priority(input_station, demo_station) >= 0


def get_demo_routes(from_station: str, to_station: str) -> list[dict]:
    """
    获取模拟路线数据，支持模糊匹配站名
    
    匹配策略：
    1. 精确匹配 key（如 "武汉-广州南"）
    2. 遍历所有 key，对出发站和到达站分别做分级匹配
    3. 结果按优先级排序
    
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
    best_match = None
    best_priority = float('inf')
    
    for route_key, routes in DEMO_DATA.items():
        parts = route_key.split("-", 1)
        if len(parts) == 2:
            demo_from, demo_to = parts
            
            # 出发站匹配优先级
            from_priority = _match_priority(from_station, demo_from)
            # 到达站匹配优先级
            to_priority = _match_priority(to_station, demo_to)
            
            # 两站都匹配
            if from_priority >= 0 and to_priority >= 0:
                total_priority = from_priority + to_priority
                if total_priority < best_priority:
                    best_priority = total_priority
                    best_match = routes.copy()
    
    return best_match if best_match else []


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
    
    # 使用统一的换乘枢纽列表
    for hub in TRANSFER_HUBS:
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
