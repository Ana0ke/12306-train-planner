"""
季节信息引擎 - 根据出行日期提供季节、天气、穿衣建议
支持节假日提醒和季节性推荐
"""

from datetime import datetime, date
from typing import Optional
from loguru import logger


class SeasonEngine:
    """季节信息引擎"""

    def __init__(self):
        # 城市月度数据：{城市: {月份: {"season": 季节, "weather": 天气, "temp": 温度范围, "clothes": 穿衣建议, "tips": 注意事项}}}
        self._city_season_data = self._init_city_data()

    def _init_city_data(self) -> dict:
        """初始化城市季节数据（覆盖20+城市×12个月）"""
        return {
            # ===== 西藏 ===== 
            "拉萨": {
                1: {"season": "冬季", "weather": "晴朗干燥", "temp": "-10~10°C", "clothes": "羽绒服、厚毛衣、保暖内衣、帽子手套", "tips": "气候干燥，多喝水，注意防晒"},
                2: {"season": "冬季", "weather": "晴朗干燥", "temp": "-8~12°C", "clothes": "羽绒服、厚毛衣、保暖内衣", "tips": "冬季人少，门票优惠"},
                3: {"season": "春季", "weather": "晴间多云", "temp": "0~16°C", "clothes": "棉衣、厚外套、薄毛衣", "tips": "三月桃花开，川藏线开始热闹"},
                4: {"season": "春季", "weather": "晴朗", "temp": "3~18°C", "clothes": "厚外套、薄毛衣、长袖", "tips": "林芝桃花节期间，人流量大"},
                5: {"season": "春季", "weather": "晴朗", "temp": "6~22°C", "clothes": "外套、长袖、早晚需加衣", "tips": "最佳旅游月份之一"},
                6: {"season": "夏季", "weather": "多阵雨", "temp": "9~24°C", "clothes": "薄外套、长袖、防晒帽", "tips": "雨季来临，但仍是旺季"},
                7: {"season": "夏季", "weather": "阵雨为主", "temp": "10~24°C", "clothes": "薄外套、长袖、短袖", "tips": "旺季，酒店需提前预订"},
                8: {"season": "夏季", "weather": "阵雨", "temp": "9~23°C", "clothes": "薄外套、长袖", "tips": "那达慕节，气氛热烈"},
                9: {"season": "秋季", "weather": "晴朗干燥", "temp": "5~20°C", "clothes": "外套、薄毛衣、长袖", "tips": "最佳旅游季，风景最美"},
                10: {"season": "秋季", "weather": "晴朗", "temp": "0~16°C", "clothes": "厚外套、毛衣", "tips": "秋季景色宜人"},
                11: {"season": "冬季", "weather": "晴朗", "temp": "-5~12°C", "clothes": "羽绒服、厚毛衣", "tips": "人少清净，适合摄影"},
                12: {"season": "冬季", "weather": "晴朗寒冷", "temp": "-10~8°C", "clothes": "羽绒服、厚毛衣、保暖内衣", "tips": "冬季优惠多，布达拉宫免费"},
            },

            # ===== 四川 =====
            "成都": {
                1: {"season": "冬季", "weather": "阴冷", "temp": "3~10°C", "clothes": "羽绒服、厚毛衣、秋裤", "tips": "湿冷，取暖靠抖"},
                2: {"season": "冬季", "weather": "阴天为主", "temp": "5~12°C", "clothes": "棉衣、厚外套", "tips": "春节期间，氛围浓厚"},
                3: {"season": "春季", "weather": "多阴雨", "temp": "10~18°C", "clothes": "外套、毛衣、长袖", "tips": "春暖花开，龙泉驿桃花"},
                4: {"season": "春季", "weather": "晴雨相间", "temp": "14~24°C", "clothes": "长袖、外套", "tips": "清明踏青好时节"},
                5: {"season": "春季", "weather": "温和", "temp": "18~26°C", "clothes": "长袖、薄外套", "tips": "初夏，舒适宜人"},
                6: {"season": "夏季", "weather": "闷热多雨", "temp": "22~28°C", "clothes": "短袖、雨伞", "tips": "雨季，出行带伞"},
                7: {"season": "夏季", "weather": "闷热", "temp": "24~32°C", "clothes": "短袖、防晒", "tips": "最热月份，注意防暑"},
                8: {"season": "夏季", "weather": "闷热多雨", "temp": "23~30°C", "clothes": "短袖、雨具", "tips": "暑期旺季，熊猫基地人多"},
                9: {"season": "秋季", "weather": "秋高气爽", "temp": "18~26°C", "clothes": "长袖、薄外套", "tips": "舒适，适合出行"},
                10: {"season": "秋季", "weather": "晴朗", "temp": "14~20°C", "clothes": "外套、毛衣", "tips": "秋季景色宜人"},
                11: {"season": "秋季", "weather": "阴天", "temp": "10~16°C", "clothes": "厚外套、毛衣", "tips": "深秋，略有寒意"},
                12: {"season": "冬季", "weather": "阴冷", "temp": "5~12°C", "clothes": "羽绒服、厚毛衣", "tips": "元旦氛围好，但较冷"},
            },

            # ===== 陕西 =====
            "西安": {
                1: {"season": "冬季", "weather": "寒冷干燥", "temp": "-4~6°C", "clothes": "羽绒服、厚毛衣、保暖内衣", "tips": "室内有暖气"},
                2: {"season": "冬季", "weather": "寒冷", "temp": "-2~8°C", "clothes": "羽绒服、厚外套", "tips": "春节期间年味浓"},
                3: {"season": "春季", "weather": "多风", "temp": "4~16°C", "clothes": "外套、毛衣、围巾", "tips": "三月开始变暖，春风大"},
                4: {"season": "春季", "weather": "温暖", "temp": "10~22°C", "clothes": "长袖、外套", "tips": "赏花好时节"},
                5: {"season": "春季", "weather": "舒适", "temp": "15~28°C", "clothes": "长袖、薄外套", "tips": "最佳旅游月份之一"},
                6: {"season": "夏季", "weather": "炎热", "temp": "20~34°C", "clothes": "短袖、防晒", "tips": "开始炎热，室内有空调"},
                7: {"season": "夏季", "weather": "闷热", "temp": "23~35°C", "clothes": "短袖、防晒、及时补水", "tips": "最热月份，注意防暑"},
                8: {"season": "夏季", "weather": "闷热多雨", "temp": "22~32°C", "clothes": "短袖、雨具", "tips": "雨季，出行带伞"},
                9: {"season": "秋季", "weather": "秋高气爽", "temp": "16~26°C", "clothes": "长袖、薄外套", "tips": "舒适宜人，最佳季节"},
                10: {"season": "秋季", "weather": "凉爽", "temp": "10~20°C", "clothes": "外套、毛衣", "tips": "秋高气爽，景色宜人"},
                11: {"season": "秋季", "weather": "渐冷", "temp": "3~14°C", "clothes": "厚外套、毛衣", "tips": "初冬，注意保暖"},
                12: {"season": "冬季", "weather": "寒冷", "temp": "-3~8°C", "clothes": "羽绒服、厚毛衣", "tips": "室内有暖气"},
            },

            # ===== 福建 =====
            "厦门": {
                1: {"season": "冬季", "weather": "温暖", "temp": "10~18°C", "clothes": "外套、长袖、早晚需加衣", "tips": "避寒好去处，人少清净"},
                2: {"season": "冬季", "weather": "温暖", "temp": "12~20°C", "clothes": "外套、长袖", "tips": "春节期间游客多，酒店涨价"},
                3: {"season": "春季", "weather": "温暖多雨", "temp": "14~22°C", "clothes": "外套、长袖、雨具", "tips": "春雨绵绵，但气温舒适"},
                4: {"season": "春季", "weather": "温暖", "temp": "18~26°C", "clothes": "长袖、薄外套", "tips": "最佳旅游月份之一"},
                5: {"season": "春季", "weather": "舒适", "temp": "22~28°C", "clothes": "短袖、薄外套", "tips": "初夏，舒适宜人"},
                6: {"season": "夏季", "weather": "炎热", "temp": "25~32°C", "clothes": "短袖、防晒、遮阳帽", "tips": "进入旅游旺季"},
                7: {"season": "夏季", "weather": "炎热", "temp": "26~34°C", "clothes": "短袖、防晒、遮阳伞", "tips": "最热月份，台风季开始"},
                8: {"season": "夏季", "weather": "闷热", "temp": "26~33°C", "clothes": "短袖、防晒", "tips": "暑期旺季，需防台风"},
                9: {"season": "秋季", "weather": "舒适", "temp": "24~30°C", "clothes": "短袖、薄外套", "tips": "台风季末，仍较热"},
                10: {"season": "秋季", "weather": "宜人", "temp": "20~28°C", "clothes": "长袖、薄外套", "tips": "最佳旅游月份之一"},
                11: {"season": "秋季", "weather": "温暖", "temp": "15~24°C", "clothes": "外套、长袖", "tips": "秋高气爽，人少清净"},
                12: {"season": "冬季", "weather": "温暖", "temp": "10~20°C", "clothes": "外套、长袖", "tips": "避寒好去处"},
            },

            # ===== 云南 =====
            "丽江": {
                1: {"season": "冬季", "weather": "干燥晴朗", "temp": "3~17°C", "clothes": "厚外套、毛衣、早晚需羽绒服", "tips": "干燥，注意补水"},
                2: {"season": "冬季", "weather": "干燥", "temp": "5~19°C", "clothes": "外套、毛衣", "tips": "春节期间氛围好"},
                3: {"season": "春季", "weather": "干燥", "temp": "7~22°C", "clothes": "外套、长袖", "tips": "油菜花开，景色美"},
                4: {"season": "春季", "weather": "干燥", "temp": "10~24°C", "clothes": "长袖、薄外套", "tips": "最佳旅游季，鲜花盛开"},
                5: {"season": "春季", "weather": "多雨", "temp": "13~25°C", "clothes": "外套、雨具", "tips": "雨季开始，但人不多"},
                6: {"season": "夏季", "weather": "多雨", "temp": "15~24°C", "clothes": "薄外套、雨具", "tips": "雨季，云多，难见雪山"},
                7: {"season": "夏季", "weather": "多雨", "temp": "15~23°C", "clothes": "薄外套、雨衣", "tips": "暑期旺季，游客多"},
                8: {"season": "夏季", "weather": "多雨", "temp": "15~24°C", "clothes": "薄外套、雨具", "tips": "菌子季，美食丰富"},
                9: {"season": "秋季", "weather": "晴朗", "temp": "13~23°C", "clothes": "外套、长袖", "tips": "秋高气爽，最佳季节"},
                10: {"season": "秋季", "weather": "晴朗", "temp": "9~21°C", "clothes": "厚外套、毛衣", "tips": "泸沽湖秋色很美"},
                11: {"season": "秋季", "weather": "凉爽", "temp": "5~18°C", "clothes": "羽绒服、厚外套", "tips": "深秋，略有寒意"},
                12: {"season": "冬季", "weather": "干燥寒冷", "temp": "2~16°C", "clothes": "羽绒服、厚毛衣", "tips": "晴天多，能见度好"},
            },
            "昆明": {
                1: {"season": "冬季", "weather": "晴朗", "temp": "4~17°C", "clothes": "外套、毛衣、早晚需加衣", "tips": "春城，四季如春"},
                2: {"season": "冬季", "weather": "晴朗", "temp": "6~20°C", "clothes": "外套、长袖", "tips": "春节期间温暖"},
                3: {"season": "春季", "weather": "晴朗", "temp": "9~24°C", "clothes": "长袖、薄外套", "tips": "樱花盛开"},
                4: {"season": "春季", "weather": "晴朗", "temp": "12~26°C", "clothes": "长袖、外套", "tips": "最佳旅游月份之一"},
                5: {"season": "春季", "weather": "晴朗", "temp": "15~28°C", "clothes": "短袖、薄外套", "tips": "初夏，舒适宜人"},
                6: {"season": "夏季", "weather": "多雨", "temp": "17~25°C", "clothes": "薄外套、雨具", "tips": "雨季，但气温舒适"},
                7: {"season": "夏季", "weather": "多雨", "temp": "17~24°C", "clothes": "薄外套、雨具", "tips": "菌子季节，美食丰富"},
                8: {"season": "夏季", "weather": "多雨", "temp": "17~25°C", "clothes": "薄外套、雨具", "tips": "暑期旺季"},
                9: {"season": "秋季", "weather": "晴雨相间", "temp": "15~24°C", "clothes": "外套、长袖", "tips": "舒适宜人"},
                10: {"season": "秋季", "weather": "晴朗", "temp": "12~22°C", "clothes": "外套、毛衣", "tips": "秋高气爽"},
                11: {"season": "秋季", "weather": "晴朗", "temp": "8~20°C", "clothes": "厚外套、毛衣", "tips": "深秋，需加衣"},
                12: {"season": "冬季", "weather": "晴朗", "temp": "5~17°C", "clothes": "外套、毛衣", "tips": "暖冬，避寒好去处"},
            },

            # ===== 青海 =====
            "西宁": {
                1: {"season": "冬季", "weather": "寒冷干燥", "temp": "-14~2°C", "clothes": "羽绒服、厚毛衣、保暖内衣", "tips": "干燥，注意补水"},
                2: {"season": "冬季", "weather": "寒冷", "temp": "-10~4°C", "clothes": "羽绒服、厚毛衣", "tips": "春节期间人少清净"},
                3: {"season": "春季", "weather": "多风", "temp": "-2~10°C", "clothes": "厚外套、围巾、手套", "tips": "三月仍冷，风大"},
                4: {"season": "春季", "weather": "渐暖", "temp": "3~16°C", "clothes": "外套、毛衣", "tips": "青海湖开始解冻"},
                5: {"season": "春季", "weather": "温和", "temp": "8~22°C", "clothes": "外套、长袖", "tips": "最佳季节，风景美"},
                6: {"season": "夏季", "weather": "凉爽", "temp": "10~25°C", "clothes": "外套、长袖、防晒", "tips": "油菜花开，景色绝美"},
                7: {"season": "夏季", "weather": "凉爽", "temp": "12~26°C", "clothes": "外套、长袖", "tips": "最佳旅游月份"},
                8: {"season": "夏季", "weather": "多雨", "temp": "11~24°C", "clothes": "外套、雨具", "tips": "雨季，但气温舒适"},
                9: {"season": "秋季", "weather": "晴朗", "temp": "6~20°C", "clothes": "厚外套、毛衣", "tips": "秋高气爽"},
                10: {"season": "秋季", "weather": "渐冷", "temp": "0~14°C", "clothes": "羽绒服、厚外套", "tips": "青海湖秋色"},
                11: {"season": "冬季", "weather": "寒冷", "temp": "-8~4°C", "clothes": "羽绒服、厚毛衣", "tips": "开始降雪"},
                12: {"season": "冬季", "weather": "寒冷", "temp": "-12~2°C", "clothes": "羽绒服、厚毛衣、保暖内衣", "tips": "人少清净"},
            },

            # ===== 甘肃 =====
            "敦煌": {
                1: {"season": "冬季", "weather": "寒冷干燥", "temp": "-15~2°C", "clothes": "羽绒服、厚毛衣、保暖内衣", "tips": "淡季，门票优惠"},
                2: {"season": "冬季", "weather": "寒冷", "temp": "-12~4°C", "clothes": "羽绒服、厚外套", "tips": "春节期间游客较少"},
                3: {"season": "春季", "weather": "多风沙", "temp": "0~16°C", "clothes": "厚外套、围巾、口罩", "tips": "风沙大，注意防护"},
                4: {"season": "春季", "weather": "温和", "temp": "6~24°C", "clothes": "外套、长袖", "tips": "最佳季节，人少景美"},
                5: {"season": "春季", "weather": "温暖", "temp": "12~30°C", "clothes": "长袖、短袖、外套", "tips": "舒适宜人"},
                6: {"season": "夏季", "weather": "炎热干燥", "temp": "18~36°C", "clothes": "短袖、防晒、遮阳帽", "tips": "最热，需防暑"},
                7: {"season": "夏季", "weather": "炎热", "temp": "20~38°C", "clothes": "短袖、防晒", "tips": "旺季，人多需提前订票"},
                8: {"season": "夏季", "weather": "炎热", "temp": "19~35°C", "clothes": "短袖、防晒", "tips": "暑期旺季"},
                9: {"season": "秋季", "weather": "舒适", "temp": "10~28°C", "clothes": "外套、长袖", "tips": "最佳季节，风景美"},
                10: {"season": "秋季", "weather": "渐凉", "temp": "3~20°C", "clothes": "厚外套、毛衣", "tips": "秋高气爽"},
                11: {"season": "秋季", "weather": "寒冷", "temp": "-4~10°C", "clothes": "羽绒服、厚外套", "tips": "淡季开始"},
                12: {"season": "冬季", "weather": "寒冷", "temp": "-14~2°C", "clothes": "羽绒服、厚毛衣", "tips": "淡季，参观人数少"},
            },

            # ===== 新疆 =====
            "乌鲁木齐": {
                1: {"season": "冬季", "weather": "寒冷", "temp": "-18~-8°C", "clothes": "羽绒服、厚毛衣、保暖内衣、皮帽", "tips": "极寒，室内有暖气"},
                2: {"season": "冬季", "weather": "寒冷", "temp": "-15~-5°C", "clothes": "羽绒服、厚毛衣", "tips": "春节期间有冰雪节"},
                3: {"season": "春季", "weather": "多风", "temp": "-2~8°C", "clothes": "厚外套、毛衣", "tips": "三月仍冷，春装上市晚"},
                4: {"season": "春季", "weather": "渐暖", "temp": "4~16°C", "clothes": "外套、毛衣", "tips": "杏花开放"},
                5: {"season": "春季", "weather": "温和", "temp": "11~24°C", "clothes": "外套、长袖", "tips": "伊犁薰衣草开始绽放"},
                6: {"season": "夏季", "weather": "舒适", "temp": "17~29°C", "clothes": "短袖、外套", "tips": "草原最美季节"},
                7: {"season": "夏季", "weather": "炎热", "temp": "19~32°C", "clothes": "短袖、防晒", "tips": "最热月份，但比南方舒适"},
                8: {"season": "夏季", "weather": "舒适", "temp": "17~30°C", "clothes": "短袖、外套", "tips": "瓜果飘香"},
                9: {"season": "秋季", "weather": "凉爽", "temp": "10~22°C", "clothes": "外套、毛衣", "tips": "金秋胡杨林"},
                10: {"season": "秋季", "weather": "渐冷", "temp": "3~14°C", "clothes": "厚外套、毛衣", "tips": "开始降雪"},
                11: {"season": "冬季", "weather": "寒冷", "temp": "-10~-1°C", "clothes": "羽绒服、厚毛衣", "tips": "冰雪旅游季"},
                12: {"season": "冬季", "weather": "寒冷", "temp": "-16~-6°C", "clothes": "羽绒服、厚毛衣、保暖内衣", "tips": "滑雪季开始"},
            },

            # ===== 东北 =====
            "哈尔滨": {
                1: {"season": "冬季", "weather": "极寒", "temp": "-24~-12°C", "clothes": "羽绒服、厚毛衣、保暖内衣、围巾手套", "tips": "极寒，手机会自动关机"},
                2: {"season": "冬季", "weather": "极寒", "temp": "-20~-8°C", "clothes": "羽绒服、厚毛衣", "tips": "春节期间冰雪大世界"},
                3: {"season": "冬季", "weather": "寒冷", "temp": "-10~0°C", "clothes": "羽绒服、厚外套", "tips": "三月仍冷，冰雪融化"},
                4: {"season": "春季", "weather": "渐暖", "temp": "1~13°C", "clothes": "外套、毛衣", "tips": "冰雪消融，春风起"},
                5: {"season": "春季", "weather": "温和", "temp": "10~22°C", "clothes": "外套、长袖", "tips": "舒适宜人"},
                6: {"season": "夏季", "weather": "凉爽", "temp": "17~28°C", "clothes": "短袖、外套", "tips": "夏季避暑好去处"},
                7: {"season": "夏季", "weather": "温热", "temp": "20~30°C", "clothes": "短袖", "tips": "夏季最热月份"},
                8: {"season": "夏季", "weather": "温热", "temp": "18~27°C", "clothes": "短袖、外套", "tips": "暑期旺季"},
                9: {"season": "秋季", "weather": "凉爽", "temp": "10~20°C", "clothes": "外套、毛衣", "tips": "秋高气爽"},
                10: {"season": "秋季", "weather": "寒冷", "temp": "1~11°C", "clothes": "厚外套、毛衣", "tips": "开始供暖"},
                11: {"season": "冬季", "weather": "寒冷", "temp": "-12~-2°C", "clothes": "羽绒服、厚毛衣", "tips": "冰雪旅游开始"},
                12: {"season": "冬季", "weather": "极寒", "temp": "-20~-10°C", "clothes": "羽绒服、厚毛衣、保暖内衣", "tips": "冰雪大世界开放"},
            },

            # ===== 北京 =====
            "北京": {
                1: {"season": "冬季", "weather": "寒冷干燥", "temp": "-6~4°C", "clothes": "羽绒服、厚毛衣、保暖内衣", "tips": "室内有暖气"},
                2: {"season": "冬季", "weather": "寒冷", "temp": "-4~6°C", "clothes": "羽绒服、厚外套", "tips": "春节期间氛围好"},
                3: {"season": "春季", "weather": "多风", "temp": "2~14°C", "clothes": "外套、毛衣、围巾", "tips": "三月仍冷，春风大"},
                4: {"season": "春季", "weather": "温暖", "temp": "9~22°C", "clothes": "外套、长袖", "tips": "玉兰花开放"},
                5: {"season": "春季", "weather": "舒适", "temp": "15~28°C", "clothes": "长袖、薄外套", "tips": "最佳季节之一"},
                6: {"season": "夏季", "weather": "炎热", "temp": "20~34°C", "clothes": "短袖、防晒", "tips": "开始炎热"},
                7: {"season": "夏季", "weather": "闷热", "temp": "23~35°C", "clothes": "短袖、防晒", "tips": "最热月份，注意防暑"},
                8: {"season": "夏季", "weather": "闷热多雨", "temp": "22~32°C", "clothes": "短袖、雨具", "tips": "雨季，需防暑防雨"},
                9: {"season": "秋季", "weather": "秋高气爽", "temp": "16~26°C", "clothes": "长袖、薄外套", "tips": "最佳季节，红叶渐起"},
                10: {"season": "秋季", "weather": "凉爽", "temp": "8~20°C", "clothes": "外套、毛衣", "tips": "秋高气爽，红叶最美"},
                11: {"season": "秋季", "weather": "渐冷", "temp": "0~12°C", "clothes": "厚外套、毛衣", "tips": "开始供暖"},
                12: {"season": "冬季", "weather": "寒冷", "temp": "-5~5°C", "clothes": "羽绒服、厚毛衣", "tips": "冬季滑雪"},
            },

            # ===== 上海 =====
            "上海": {
                1: {"season": "冬季", "weather": "阴冷", "temp": "2~8°C", "clothes": "羽绒服、厚毛衣、秋裤", "tips": "湿冷，取暖靠抖"},
                2: {"season": "冬季", "weather": "阴冷", "temp": "3~10°C", "clothes": "羽绒服、厚外套", "tips": "春节期间氛围浓"},
                3: {"season": "春季", "weather": "多雨", "temp": "7~15°C", "clothes": "外套、毛衣、雨具", "tips": "春雨绵绵"},
                4: {"season": "春季", "weather": "晴雨相间", "temp": "12~20°C", "clothes": "外套、长袖", "tips": "樱花盛开"},
                5: {"season": "春季", "weather": "舒适", "temp": "17~25°C", "clothes": "长袖、薄外套", "tips": "最佳季节之一"},
                6: {"season": "夏季", "weather": "闷热", "temp": "22~28°C", "clothes": "短袖、防晒", "tips": "梅雨季，雨具必备"},
                7: {"season": "夏季", "weather": "闷热", "temp": "26~34°C", "clothes": "短袖、防晒", "tips": "最热月份，台风季"},
                8: {"season": "夏季", "weather": "闷热", "temp": "26~33°C", "clothes": "短袖、防晒", "tips": "高温预警常见"},
                9: {"season": "秋季", "weather": "舒适", "temp": "22~28°C", "clothes": "长袖、薄外套", "tips": "舒适宜人"},
                10: {"season": "秋季", "weather": "宜人", "temp": "15~22°C", "clothes": "外套、长袖", "tips": "最佳季节之一"},
                11: {"season": "秋季", "weather": "渐凉", "temp": "8~16°C", "clothes": "厚外套、毛衣", "tips": "深秋，有点凉"},
                12: {"season": "冬季", "weather": "阴冷", "temp": "3~10°C", "clothes": "羽绒服、厚毛衣", "tips": "湿冷，注意保暖"},
            },

            # ===== 杭州 =====
            "杭州": {
                1: {"season": "冬季", "weather": "阴冷", "temp": "3~10°C", "clothes": "羽绒服、厚毛衣、秋裤", "tips": "湿冷，注意保暖"},
                2: {"season": "冬季", "weather": "阴冷", "temp": "5~12°C", "clothes": "羽绒服、厚外套", "tips": "春节期间氛围好"},
                3: {"season": "春季", "weather": "多雨", "temp": "8~16°C", "clothes": "外套、毛衣、雨具", "tips": "春雨绵绵"},
                4: {"season": "春季", "weather": "晴雨相间", "temp": "13~22°C", "clothes": "外套、长袖", "tips": "西湖美景"},
                5: {"season": "春季", "weather": "舒适", "temp": "18~26°C", "clothes": "长袖、薄外套", "tips": "最佳季节之一"},
                6: {"season": "夏季", "weather": "闷热", "temp": "23~30°C", "clothes": "短袖、防晒", "tips": "梅雨季"},
                7: {"season": "夏季", "weather": "闷热", "temp": "26~36°C", "clothes": "短袖、防晒", "tips": "最热月份，台风季"},
                8: {"season": "夏季", "weather": "闷热", "temp": "26~35°C", "clothes": "短袖、防晒", "tips": "高温预警常见"},
                9: {"season": "秋季", "weather": "舒适", "temp": "22~28°C", "clothes": "长袖、薄外套", "tips": "舒适宜人"},
                10: {"season": "秋季", "weather": "宜人", "temp": "15~23°C", "clothes": "外套、长袖", "tips": "桂花飘香"},
                11: {"season": "秋季", "weather": "渐凉", "temp": "8~16°C", "clothes": "厚外套、毛衣", "tips": "深秋西湖"},
                12: {"season": "冬季", "weather": "阴冷", "temp": "4~12°C", "clothes": "羽绒服、厚毛衣", "tips": "湿冷注意保暖"},
            },

            # ===== 广州 =====
            "广州": {
                1: {"season": "冬季", "weather": "温暖", "temp": "10~18°C", "clothes": "外套、长袖、早晚需加衣", "tips": "避寒好去处"},
                2: {"season": "冬季", "weather": "温暖", "temp": "12~20°C", "clothes": "外套、长袖", "tips": "春节期间温暖"},
                3: {"season": "春季", "weather": "潮湿", "temp": "15~22°C", "clothes": "外套、长袖", "tips": "回南天，较潮湿"},
                4: {"season": "春季", "weather": "多雨", "temp": "19~26°C", "clothes": "薄外套、雨具", "tips": "雨季开始"},
                5: {"season": "春季", "weather": "炎热", "temp": "23~30°C", "clothes": "短袖、空调衣", "tips": "初夏，有点热"},
                6: {"season": "夏季", "weather": "闷热", "temp": "26~32°C", "clothes": "短袖、防晒", "tips": "雨季+高温"},
                7: {"season": "夏季", "weather": "炎热", "temp": "27~34°C", "clothes": "短袖、防晒", "tips": "最热月份，台风季"},
                8: {"season": "夏季", "weather": "炎热", "temp": "27~33°C", "clothes": "短袖、防晒", "tips": "暑期旺季"},
                9: {"season": "秋季", "weather": "舒适", "temp": "25~31°C", "clothes": "短袖、薄外套", "tips": "舒适宜人"},
                10: {"season": "秋季", "weather": "宜人", "temp": "20~28°C", "clothes": "长袖、薄外套", "tips": "最佳季节之一"},
                11: {"season": "秋季", "weather": "温暖", "temp": "15~23°C", "clothes": "外套、长袖", "tips": "秋高气爽"},
                12: {"season": "冬季", "weather": "温暖", "temp": "10~19°C", "clothes": "外套、长袖", "tips": "避寒好去处"},
            },

            # ===== 长沙 =====
            "长沙": {
                1: {"season": "冬季", "weather": "阴冷", "temp": "3~8°C", "clothes": "羽绒服、厚毛衣、秋裤", "tips": "湿冷，魔法攻击"},
                2: {"season": "冬季", "weather": "阴冷", "temp": "4~10°C", "clothes": "羽绒服、厚外套", "tips": "春节期间氛围好"},
                3: {"season": "春季", "weather": "多雨", "temp": "8~16°C", "clothes": "外套、毛衣、雨具", "tips": "春雨绵绵"},
                4: {"season": "春季", "weather": "晴雨相间", "temp": "14~22°C", "clothes": "外套、长袖", "tips": "春暖花开"},
                5: {"season": "春季", "weather": "舒适", "temp": "19~28°C", "clothes": "长袖、薄外套", "tips": "初夏，舒适"},
                6: {"season": "夏季", "weather": "闷热", "temp": "24~32°C", "clothes": "短袖、防晒", "tips": "梅雨季"},
                7: {"season": "夏季", "weather": "闷热", "temp": "27~38°C", "clothes": "短袖、防晒", "tips": "最热月份，火炉城市"},
                8: {"season": "夏季", "weather": "闷热", "temp": "26~36°C", "clothes": "短袖、防晒", "tips": "暑期旺季"},
                9: {"season": "秋季", "weather": "舒适", "temp": "22~30°C", "clothes": "长袖、薄外套", "tips": "舒适宜人"},
                10: {"season": "秋季", "weather": "宜人", "temp": "15~24°C", "clothes": "外套、长袖", "tips": "最佳季节之一"},
                11: {"season": "秋季", "weather": "渐凉", "temp": "8~16°C", "clothes": "厚外套、毛衣", "tips": "深秋有点凉"},
                12: {"season": "冬季", "weather": "阴冷", "temp": "3~10°C", "clothes": "羽绒服、厚毛衣", "tips": "湿冷，注意保暖"},
            },

            # ===== 武汉 =====
            "武汉": {
                1: {"season": "冬季", "weather": "阴冷", "temp": "1~8°C", "clothes": "羽绒服、厚毛衣、秋裤", "tips": "湿冷，魔法攻击"},
                2: {"season": "冬季", "weather": "阴冷", "temp": "3~10°C", "clothes": "羽绒服、厚外套", "tips": "春节期间氛围好"},
                3: {"season": "春季", "weather": "多雨", "temp": "7~15°C", "clothes": "外套、毛衣、雨具", "tips": "春雨绵绵"},
                4: {"season": "春季", "weather": "晴雨相间", "temp": "13~22°C", "clothes": "外套、长袖", "tips": "樱花季"},
                5: {"season": "春季", "weather": "舒适", "temp": "18~28°C", "clothes": "长袖、薄外套", "tips": "初夏，舒适"},
                6: {"season": "夏季", "weather": "闷热", "temp": "24~32°C", "clothes": "短袖、防晒", "tips": "梅雨季"},
                7: {"season": "夏季", "weather": "闷热", "temp": "27~38°C", "clothes": "短袖、防晒", "tips": "最热月份，火炉城市"},
                8: {"season": "夏季", "weather": "闷热", "temp": "26~36°C", "clothes": "短袖、防晒", "tips": "暑期旺季"},
                9: {"season": "秋季", "weather": "舒适", "temp": "22~30°C", "clothes": "长袖、薄外套", "tips": "舒适宜人"},
                10: {"season": "秋季", "weather": "宜人", "temp": "14~24°C", "clothes": "外套、长袖", "tips": "最佳季节之一"},
                11: {"season": "秋季", "weather": "渐凉", "temp": "7~16°C", "clothes": "厚外套、毛衣", "tips": "深秋有点凉"},
                12: {"season": "冬季", "weather": "阴冷", "temp": "1~9°C", "clothes": "羽绒服、厚毛衣", "tips": "湿冷，注意保暖"},
            },

            # ===== 重庆 =====
            "重庆": {
                1: {"season": "冬季", "weather": "阴冷", "temp": "6~12°C", "clothes": "羽绒服、厚毛衣", "tips": "湿冷，但比湖南暖和"},
                2: {"season": "冬季", "weather": "阴冷", "temp": "7~14°C", "clothes": "羽绒服、厚外套", "tips": "春节期间氛围好"},
                3: {"season": "春季", "weather": "多雨", "temp": "10~18°C", "clothes": "外套、毛衣、雨具", "tips": "春雨绵绵"},
                4: {"season": "春季", "weather": "晴雨相间", "temp": "15~24°C", "clothes": "外套、长袖", "tips": "春暖花开"},
                5: {"season": "春季", "weather": "舒适", "temp": "19~28°C", "clothes": "长袖、薄外套", "tips": "初夏，舒适"},
                6: {"season": "夏季", "weather": "闷热", "temp": "23~32°C", "clothes": "短袖、防晒", "tips": "火炉城市开始"},
                7: {"season": "夏季", "weather": "闷热", "temp": "26~38°C", "clothes": "短袖、防晒", "tips": "最热月份，火锅很配"},
                8: {"season": "夏季", "weather": "闷热", "temp": "26~36°C", "clothes": "短袖、防晒", "tips": "暑期旺季"},
                9: {"season": "秋季", "weather": "舒适", "temp": "22~30°C", "clothes": "长袖、薄外套", "tips": "舒适宜人"},
                10: {"season": "秋季", "weather": "宜人", "temp": "16~24°C", "clothes": "外套、长袖", "tips": "最佳季节之一"},
                11: {"season": "秋季", "weather": "渐凉", "temp": "10~18°C", "clothes": "厚外套、毛衣", "tips": "深秋有点凉"},
                12: {"season": "冬季", "weather": "阴冷", "temp": "6~13°C", "clothes": "羽绒服、厚毛衣", "tips": "湿冷，但比北方暖和"},
            },

            # ===== 桂林 =====
            "桂林": {
                1: {"season": "冬季", "weather": "阴冷", "temp": "5~12°C", "clothes": "羽绒服、厚毛衣", "tips": "淡季，游客少"},
                2: {"season": "冬季", "weather": "阴冷", "temp": "7~14°C", "clothes": "羽绒服、厚外套", "tips": "春节期间氛围好"},
                3: {"season": "春季", "weather": "多雨", "temp": "10~18°C", "clothes": "外套、毛衣、雨具", "tips": "烟雨漓江"},
                4: {"season": "春季", "weather": "晴雨相间", "temp": "15~24°C", "clothes": "外套、长袖", "tips": "春暖花开"},
                5: {"season": "春季", "weather": "舒适", "temp": "20~28°C", "clothes": "长袖、薄外套", "tips": "初夏，舒适"},
                6: {"season": "夏季", "weather": "闷热", "temp": "24~32°C", "clothes": "短袖、防晒", "tips": "雨季，漓江水位高"},
                7: {"season": "夏季", "weather": "闷热", "temp": "25~34°C", "clothes": "短袖、防晒", "tips": "暑期旺季"},
                8: {"season": "夏季", "weather": "闷热", "temp": "25~33°C", "clothes": "短袖、防晒", "tips": "暑期旺季"},
                9: {"season": "秋季", "weather": "舒适", "temp": "22~30°C", "clothes": "长袖、薄外套", "tips": "舒适宜人"},
                10: {"season": "秋季", "weather": "宜人", "temp": "16~25°C", "clothes": "外套、长袖", "tips": "最佳季节之一"},
                11: {"season": "秋季", "weather": "渐凉", "temp": "10~18°C", "clothes": "厚外套、毛衣", "tips": "深秋有点凉"},
                12: {"season": "冬季", "weather": "阴冷", "temp": "5~13°C", "clothes": "羽绒服、厚毛衣", "tips": "淡季，游客少"},
            },

            # ===== 南京 =====
            "南京": {
                1: {"season": "冬季", "weather": "阴冷", "temp": "1~8°C", "clothes": "羽绒服、厚毛衣、秋裤", "tips": "湿冷，注意保暖"},
                2: {"season": "冬季", "weather": "阴冷", "temp": "2~10°C", "clothes": "羽绒服、厚外套", "tips": "春节期间氛围好"},
                3: {"season": "春季", "weather": "多雨", "temp": "6~14°C", "clothes": "外套、毛衣、雨具", "tips": "春雨绵绵"},
                4: {"season": "春季", "weather": "晴雨相间", "temp": "12~22°C", "clothes": "外套、长袖", "tips": "春暖花开"},
                5: {"season": "春季", "weather": "舒适", "temp": "17~27°C", "clothes": "长袖、薄外套", "tips": "初夏，舒适"},
                6: {"season": "夏季", "weather": "闷热", "temp": "23~30°C", "clothes": "短袖、防晒", "tips": "梅雨季"},
                7: {"season": "夏季", "weather": "闷热", "temp": "26~36°C", "clothes": "短袖、防晒", "tips": "最热月份"},
                8: {"season": "夏季", "weather": "闷热", "temp": "26~35°C", "clothes": "短袖、防晒", "tips": "暑期旺季"},
                9: {"season": "秋季", "weather": "舒适", "temp": "21~28°C", "clothes": "长袖、薄外套", "tips": "舒适宜人"},
                10: {"season": "秋季", "weather": "宜人", "temp": "14~23°C", "clothes": "外套、长袖", "tips": "最佳季节之一"},
                11: {"season": "秋季", "weather": "渐凉", "temp": "6~16°C", "clothes": "厚外套、毛衣", "tips": "深秋有点凉"},
                12: {"season": "冬季", "weather": "阴冷", "temp": "1~9°C", "clothes": "羽绒服、厚毛衣", "tips": "湿冷注意保暖"},
            },

            # ===== 贵阳 =====
            "贵阳": {
                1: {"season": "冬季", "weather": "阴冷", "temp": "3~10°C", "clothes": "羽绒服、厚毛衣", "tips": "湿冷，但比湖南暖和"},
                2: {"season": "冬季", "weather": "阴冷", "temp": "4~12°C", "clothes": "羽绒服、厚外套", "tips": "春节期间氛围好"},
                3: {"season": "春季", "weather": "多雨", "temp": "7~16°C", "clothes": "外套、毛衣、雨具", "tips": "春雨绵绵"},
                4: {"season": "春季", "weather": "晴雨相间", "temp": "12~22°C", "clothes": "外套、长袖", "tips": "春暖花开"},
                5: {"season": "春季", "weather": "舒适", "temp": "16~25°C", "clothes": "长袖、薄外套", "tips": "初夏，舒适"},
                6: {"season": "夏季", "weather": "凉爽", "temp": "19~26°C", "clothes": "短袖、外套", "tips": "避暑好去处"},
                7: {"season": "夏季", "weather": "温热", "temp": "21~28°C", "clothes": "短袖、防晒", "tips": "夏季最热月份"},
                8: {"season": "夏季", "weather": "温热", "temp": "20~28°C", "clothes": "短袖、防晒", "tips": "暑期旺季"},
                9: {"season": "秋季", "weather": "舒适", "temp": "16~24°C", "clothes": "外套、长袖", "tips": "舒适宜人"},
                10: {"season": "秋季", "weather": "宜人", "temp": "12~20°C", "clothes": "外套、毛衣", "tips": "最佳季节之一"},
                11: {"season": "秋季", "weather": "渐凉", "temp": "6~14°C", "clothes": "厚外套、毛衣", "tips": "深秋有点凉"},
                12: {"season": "冬季", "weather": "阴冷", "temp": "3~11°C", "clothes": "羽绒服、厚毛衣", "tips": "湿冷注意保暖"},
            },

            # ===== 北海 =====
            "北海": {
                1: {"season": "冬季", "weather": "温暖", "temp": "12~20°C", "clothes": "外套、长袖", "tips": "避寒好去处"},
                2: {"season": "冬季", "weather": "温暖", "temp": "14~22°C", "clothes": "外套、长袖", "tips": "春节期间温暖"},
                3: {"season": "春季", "weather": "温暖", "temp": "16~24°C", "clothes": "外套、长袖", "tips": "舒适宜人"},
                4: {"season": "春季", "weather": "舒适", "temp": "20~28°C", "clothes": "长袖、薄外套", "tips": "初夏，舒适"},
                5: {"season": "春季", "weather": "炎热", "temp": "24~30°C", "clothes": "短袖、防晒", "tips": "初夏开始热"},
                6: {"season": "夏季", "weather": "炎热", "temp": "27~33°C", "clothes": "短袖、防晒", "tips": "海边度假好时机"},
                7: {"season": "夏季", "weather": "炎热", "temp": "28~34°C", "clothes": "短袖、防晒", "tips": "最热月份，台风季"},
                8: {"season": "夏季", "weather": "炎热", "temp": "27~33°C", "clothes": "短袖、防晒", "tips": "暑期旺季"},
                9: {"season": "秋季", "weather": "舒适", "temp": "25~31°C", "clothes": "短袖、薄外套", "tips": "舒适宜人"},
                10: {"season": "秋季", "weather": "宜人", "temp": "20~28°C", "clothes": "外套、长袖", "tips": "最佳季节之一"},
                11: {"season": "秋季", "weather": "温暖", "temp": "15~23°C", "clothes": "外套、长袖", "tips": "秋高气爽"},
                12: {"season": "冬季", "weather": "温暖", "temp": "12~20°C", "clothes": "外套、长袖", "tips": "避寒好去处"},
            },
        }

    def get_season_info(self, city: str, month: int) -> dict:
        """
        获取城市某月份的季节信息

        Args:
            city: 城市名称
            month: 月份（1-12）

        Returns:
            季节信息字典，包含season、weather、temp、clothes、tips
        """
        # 默认数据（未收录城市）
        default_info = {
            "season": "未知",
            "weather": "请查询当地天气预报",
            "temp": "请查询当地气温",
            "clothes": "根据当地气候准备衣物",
            "tips": "出行前请查看天气预报",
        }

        # 获取城市数据
        city_data = self._city_season_data.get(city, {})

        # 获取月份数据
        month_data = city_data.get(month)

        if month_data:
            return month_data.copy()
        else:
            # 尝试模糊匹配
            for city_name, data in self._city_season_data.items():
                if city in city_name or city_name in city:
                    month_data = data.get(month)
                    if month_data:
                        return month_data.copy()

            return default_info

    def get_holiday_alert(self, travel_date: date) -> dict:
        """
        获取节假日提醒

        Args:
            travel_date: 出行日期

        Returns:
            节假日提醒字典，包含is_holiday、holiday_name、alert、tips
        """
        year = travel_date.year
        month = travel_date.month
        day = travel_date.day

        result = {
            "is_holiday": False,
            "holiday_name": "",
            "alert": "",
            "tips": [],
        }

        # ===== 法定节假日 =====
        # 元旦
        if month == 1 and 1 <= day <= 3:
            result["is_holiday"] = True
            result["holiday_name"] = "元旦"
            result["alert"] = "⚠️ 元旦假期，景区人流量较大"
            result["tips"] = ["提前订房", "热门景区可能限流"]

        # 春节（农历正月初一，通常在1月下旬到2月中旬）
        elif self._is_spring_festival(travel_date):
            result["is_holiday"] = True
            result["holiday_name"] = "春节"
            result["alert"] = "⚠️ 春节期间，各地将迎来出行高峰"
            result["tips"] = [
                "提前一个月订票",
                "酒店价格翻倍",
                "景区可能关闭部分区域",
                "很多餐厅关门，请提前确认",
            ]

        # 清明节（4月4日-6日）
        elif month == 4 and 4 <= day <= 6:
            result["is_holiday"] = True
            result["holiday_name"] = "清明节"
            result["alert"] = "⚠️ 清明假期，踏青赏花好时节"
            result["tips"] = ["热门景区人多", "祭祀场所附近交通管制"]

        # 劳动节（5月1日-5日）
        elif month == 5 and 1 <= day <= 5:
            result["is_holiday"] = True
            result["holiday_name"] = "劳动节"
            result["alert"] = "⚠️ 五一假期，是出游高峰期"
            result["tips"] = [
                "热门景区人满为患",
                "酒店价格大涨",
                "建议提前2-3周订房",
            ]

        # 端午节（农历五月初五，通常在6月）
        elif month == 6 and self._is_dragon_boat(travel_date):
            result["is_holiday"] = True
            result["holiday_name"] = "端午节"
            result["alert"] = "⚠️ 端午假期，粽子飘香"
            result["tips"] = ["赛龙舟活动多", "南方多雨，注意防滑"]

        # 中秋节（农历八月十五，通常在9月或10月）
        elif (month == 9 or month == 10) and self._is_mid_autumn(travel_date):
            result["is_holiday"] = True
            result["holiday_name"] = "中秋节"
            result["alert"] = "⚠️ 中秋假期，赏月团圆"
            result["tips"] = ["部分地区赏月活动", "可能与国庆假期连休"]

        # 国庆节（10月1日-7日）
        elif month == 10 and 1 <= day <= 7:
            result["is_holiday"] = True
            result["holiday_name"] = "国庆节"
            result["alert"] = "⚠️ 国庆黄金周，年度最大出行高峰！"
            result["tips"] = [
                "必须提前订房订票！",
                "景区人山人海",
                "酒店价格是平时的3-5倍",
                "建议错峰出行",
            ]

        # ===== 旺季提醒（非节假日但人多）=====
        # 暑假（7月-8月）
        elif month == 7 or month == 8:
            result["is_holiday"] = True
            result["holiday_name"] = "暑假"
            result["alert"] = "📚 暑假期间，亲子游、学生游较多"
            result["tips"] = ["热门景区人多", "建议提前规划"]

        # 寒假（1月-2月，非春节）
        elif month == 1 or (month == 2 and not self._is_spring_festival(travel_date)):
            result["is_holiday"] = True
            result["holiday_name"] = "寒假"
            result["alert"] = "📚 寒假期间，北方游客南下避寒多"
            result["tips"] = ["海南、云南等避寒目的地人多", "提前订房"]

        # ===== 小长假前后的周末调休 =====
        # 节假日前一天
        elif self._is_before_holiday(travel_date):
            result["alert"] = "📢 明天开始放假，今天可能已经开始拥堵"
            result["tips"] = ["提前出发，避开高峰"]

        # 节假日最后一天
        elif self._is_after_holiday(travel_date):
            result["alert"] = "📢 假期最后一天，返程高峰"
            result["tips"] = ["提前返程，避开晚高峰"]

        return result

    def _is_spring_festival(self, travel_date: date) -> bool:
        """判断是否为春节假期（农历正月初一到初七）"""
        from datetime import timedelta
        # 简化判断：1月21日-2月5日的范围内
        jan21 = date(travel_date.year, 1, 21)
        feb5 = date(travel_date.year, 2, 5)
        # 春节通常是1月21日到2月20日之间
        jan_start = date(travel_date.year, 1, 21)
        feb_end = date(travel_date.year, 2, 20)
        if jan_start <= travel_date <= feb_end:
            # 粗略判断：1月21日到2月20日之间
            # 实际春节日期需要农历计算，这里用简单范围
            if travel_date >= jan21:
                return True
        return False

    def _is_dragon_boat(self, travel_date: date) -> bool:
        """判断是否为端午节附近（6月第三周周末前后）"""
        # 简化判断：6月第三周
        from datetime import timedelta
        # 找6月第三个周六
        base = date(travel_date.year, 6, 1)
        # 找到第一个周六
        days_to_first_sat = (5 - base.weekday()) % 7
        first_sat = base + timedelta(days=days_to_first_sat)
        third_sat = first_sat + timedelta(days=14)
        # 端午节在第三个周六附近
        return abs((travel_date - third_sat).days) <= 2

    def _is_mid_autumn(self, travel_date: date) -> bool:
        """判断是否为中秋节附近"""
        # 简化判断：9月15-21日
        month = travel_date.month
        day = travel_date.day
        return month == 9 and 15 <= day <= 21

    def _is_before_holiday(self, travel_date: date) -> bool:
        """判断是否为节假日前一天"""
        from datetime import timedelta
        # 元旦前一天
        if travel_date == date(travel_date.year, 1, 1) - timedelta(days=1):
            return True
        # 五一前一天
        if travel_date == date(travel_date.year, 5, 1) - timedelta(days=1):
            return True
        # 国庆前一天
        if travel_date == date(travel_date.year, 10, 1) - timedelta(days=1):
            return True
        return False

    def _is_after_holiday(self, travel_date: date) -> bool:
        """判断是否为节假日最后一天"""
        from datetime import timedelta
        # 元旦最后一天
        if travel_date == date(travel_date.year, 1, 3):
            return True
        # 五一最后一天
        if travel_date == date(travel_date.year, 5, 5):
            return True
        # 国庆最后一天
        if travel_date == date(travel_date.year, 10, 7):
            return True
        return False

    def get_seasonal_recommendation(self, city: str, month: int) -> str:
        """
        获取季节性推荐

        Args:
            city: 城市名称
            month: 月份（1-12）

        Returns:
            季节性推荐字符串
        """
        recommendations = {
            # 拉萨
            ("拉萨", 3): "🌸 林芝桃花节，雪山下的粉色花海",
            ("拉萨", 4): "🌸 林芝桃花节最后观赏期，错过等一年",
            ("拉萨", 6): "💐 青海湖油菜花开，金色的海洋",
            ("拉萨", 7): "🌿 那曲草原绿草如茵，野花遍地",
            ("拉萨", 9): "🍂 秋季最佳，晴空万里，风景绝美",
            ("拉萨", 10): "🍁 九寨沟彩林，层林尽染",
            ("拉萨", 11): "❄️ 拉萨暖阳，避开寒冷地区的好选择",
            ("拉萨", 12): "❄️ 布达拉宫免费参观，人少清净",

            # 成都
            ("成都", 3): "🌸 龙泉驿桃花，粉色的海洋",
            ("成都", 4): "🌼 清明踏青，青城山都江堰",
            ("成都", 7): "🐼 暑期带娃看熊猫",
            ("成都", 9): "🍂 秋高气爽，最宜出行",

            # 西安
            ("西安", 3): "🌸 青龙寺樱花，历史与花海的邂逅",
            ("西安", 4): "🌼 春季好时光，城墙骑行",
            ("西安", 9): "🍂 秋季最佳，兵马俑人少景美",
            ("西安", 10): "🏛️ 国庆后错峰，人少体验好",
            ("西安", 11): "🍁 古观音禅寺千年银杏",
            ("西安", 12): "❄️ 室内暖气足，室外赏雪景",

            # 厦门
            ("厦门", 1): "🌊 避寒圣地，温暖如春",
            ("厦门", 2): "🏮 春节期间，花团锦簇",
            ("厦门", 4): "🌸 鼓浪屿春暖花开",
            ("厦门", 10): "🌴 最佳季节，避开台风季",
            ("厦门", 11): "🌤️ 秋高气爽，舒适宜人",

            # 丽江
            ("丽江", 2): "🏮 春节期间，古城年味浓",
            ("丽江", 3): "🌸 油菜花盛开，玉龙雪山清晰",
            ("丽江", 6): "🌿 菌子季节，美食之旅",
            ("丽江", 7): "🌧️ 雨季，云多难见雪山",
            ("丽江", 10): "🌾 泸沽湖秋色，水性杨花",
            ("丽江", 12): "☀️ 冬季阳光充足，避开人流",

            # 西宁/青海
            ("西宁", 6): "🌼 青海湖油菜花，年度最美的季节",
            ("西宁", 7): "🌿 环湖自行车赛，草原最美",
            ("西宁", 8): "🌸 祁连山花海，卓尔山丹霞",
            ("西宁", 10): "🍂 胡杨林金黄，摄影最佳季",

            # 哈尔滨
            ("哈尔滨", 1): "❄️ 冰雪大世界，冰雕王国",
            ("哈尔滨", 2): "🏮 冰灯节，春节氛围浓",
            ("哈尔滨", 7): "🌿 夏季避暑，平均气温25°C",
            ("哈尔滨", 12): "❄️ 冰雪大世界开放",

            # 桂林
            ("桂林", 4): "🌿 烟雨漓江，如诗如画",
            ("桂林", 6): "🏞️ 漓江水位高，游船最稳",
            ("桂林", 10): "🍂 秋高气爽，骑行最好季节",

            # 北京
            ("北京", 3): "🌸 玉兰花开放，颐和园最美",
            ("北京", 4): "🌼 樱花季，北海公园泛舟",
            ("北京", 10): "🍁 香山红叶，最佳观赏期",
            ("北京", 11): "🍂 故宫银杏，金色海洋",

            # 杭州
            ("杭州", 3): "🌸 西湖边太子湾樱花盛开",
            ("杭州", 4): "🌼 太子湾郁金香，春季最美",
            ("杭州", 10): "�丹桂飘香，满觉陇赏桂",

            # 广州
            ("广州", 1): "🌺 冬季避寒，花市迎春",
            ("广州", 2): "🏮 春节花市，行花街",
            ("广州", 10): "🌤️ 秋季舒适，避开回南天",

            # 长沙
            ("长沙", 3): "🌸 橘子洲梅花开放",
            ("长沙", 7): "🍉 暑期摘西瓜，漂流好时节",
            ("长沙", 10): "🍂 秋季舒适，岳麓山红叶",
        }

        key = (city, month)
        if key in recommendations:
            return recommendations[key]

        # 通用推荐
        if month in [4, 5, 9, 10]:
            return "🍃 春秋季气候宜人，是出行的黄金季节"
        elif month in [6, 7, 8]:
            return "☀️ 夏季炎热，注意防暑防晒"
        elif month in [1, 2, 12]:
            return "❄️ 冬季寒冷，可考虑避寒目的地"
        else:
            return "🌤️ 根据当地气候合理安排行程"


# 全局实例
_season_engine: SeasonEngine | None = None


def get_season_engine() -> SeasonEngine:
    """获取全局季节引擎实例"""
    global _season_engine
    if _season_engine is None:
        _season_engine = SeasonEngine()
    return _season_engine


def get_season_info(city: str, month: int) -> dict:
    """获取季节信息（便捷函数）"""
    return get_season_engine().get_season_info(city, month)


def get_holiday_alert(travel_date: date) -> dict:
    """获取节假日提醒（便捷函数）"""
    return get_season_engine().get_holiday_alert(travel_date)


def get_seasonal_recommendation(city: str, month: int) -> str:
    """获取季节性推荐（便捷函数）"""
    return get_season_engine().get_seasonal_recommendation(city, month)
