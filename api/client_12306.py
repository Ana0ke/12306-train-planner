"""
12306查询客户端
封装12306查询接口，支持余票和时刻查询
"""

import httpx
from loguru import logger
from typing import Optional


class Client12306:
    """12306查询客户端"""

    # 12306查询接口
    QUERY_URL = "https://kyfw.12306.cn/otn/leftTicket/query"
    STATION_URL = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js"

    # 请求头
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
        "Referer": "https://kyfw.12306.cn/otn/leftTicket/init",
    }

    def __init__(self):
        self._station_map: Optional[dict[str, str]] = None

    def query(
        self,
        from_station: str,
        to_station: str,
        date: str,
    ) -> list[dict]:
        """
        查询车次信息

        Args:
            from_station: 出发站名（如"长沙南"）
            to_station: 到达站名（如"广州南"）
            date: 日期（如"2026-06-12"）

        Returns:
            车次信息列表
        """
        try:
            # 获取站点代码
            from_code = self._get_station_code(from_station)
            to_code = self._get_station_code(to_station)

            if not from_code or not to_code:
                logger.warning(f"未找到站点代码: {from_station}({from_code}) → {to_station}({to_code})")
                return []

            # 构建查询URL
            url = f"{self.QUERY_URL}"
            params = {
                "leftTicketDTO.train_date": date,
                "leftTicketDTO.from_station": from_code,
                "leftTicketDTO.to_station": to_code,
                "purpose_codes": "ADULT",
            }

            with httpx.Client(timeout=10) as client:
                resp = client.get(url, params=params, headers=self.HEADERS, follow_redirects=True)
                resp.raise_for_status()
                data = resp.json()

            if data.get("httpstatus") != 200:
                logger.error(f"12306查询失败: {data}")
                return []

            # 解析结果
            results = data.get("data", {}).get("result", [])
            return [self._parse_train_info(r) for r in results]

        except httpx.HTTPError as e:
            logger.error(f"12306请求失败: {e}")
            return []
        except Exception as e:
            logger.error(f"12306查询异常: {e}")
            return []

    def _get_station_code(self, station_name: str) -> Optional[str]:
        """获取站点电报码"""
        if self._station_map is None:
            self._load_station_map()
        return self._station_map.get(station_name)

    def _load_station_map(self):
        """加载站点名→电报码映射"""
        self._station_map = {}
        try:
            with httpx.Client(timeout=15) as client:
                resp = client.get(self.STATION_URL, headers=self.HEADERS, follow_redirects=True)
                resp.raise_for_status()
                text = resp.text

            # 解析 station_name.js 格式
            # 格式: @bjb|北京北|VAP|beijingbei|bjb|0
            for entry in text.split("@")[1:]:
                parts = entry.split("|")
                if len(parts) >= 3:
                    name = parts[1]       # 站名
                    code = parts[2]       # 电报码
                    self._station_map[name] = code

            logger.info(f"加载站点映射: {len(self._station_map)} 个站点")

        except Exception as e:
            logger.error(f"加载站点映射失败: {e}")
            # 使用预置常用站点
            self._station_map = {
                "北京": "BJP", "北京西": "BXP", "北京南": "VNP",
                "上海": "SHH", "上海虹桥": "AOH", "上海南": "SNH",
                "广州": "GZQ", "广州南": "IZQ", "广州东": "GGQ",
                "深圳": "SZQ", "深圳北": "IOQ", "深圳东": "BJQ",
                "长沙": "CSQ", "长沙南": "CWQ",
                "武汉": "WHN", "汉口": "HKN",
                "成都东": "ICW", "重庆北": "CUW",
                "永州": "YNQ", "东安东": "DAZ",
                "衡阳东": "HVQ", "株洲西": "ZAQ",
                "南京南": "NKH", "杭州东": "HGH",
                "西安北": "EAO", "郑州东": "ZAF",
                "贵阳北": "KQW", "南宁东": "NFZ",
                "昆明南": "KOM", "拉萨": "LSO",
                "西宁": "XNO", "格尔木": "GRO",
            }

    def _parse_train_info(self, raw_str: str) -> dict:
        """
        解析12306返回的车次信息字符串
        格式: 预订|车次|出发站|到达站|出发时间|到达时间|历时|...
        """
        try:
            fields = raw_str.split("|")
            return {
                "train_no": fields[3] if len(fields) > 3 else "",
                "from_station_code": fields[6] if len(fields) > 6 else "",
                "to_station_code": fields[7] if len(fields) > 7 else "",
                "depart_time": fields[8] if len(fields) > 8 else "",
                "arrive_time": fields[9] if len(fields) > 9 else "",
                "duration": fields[10] if len(fields) > 10 else "",
            }
        except Exception as e:
            logger.warning(f"解析车次信息失败: {e}")
            return {}
