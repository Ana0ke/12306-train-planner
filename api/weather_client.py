"""
天气查询客户端
使用 wttr.in 免费API获取天气信息
无需API Key，直接可用
"""

import httpx
from typing import Optional
from loguru import logger


def get_weather(city: str, date: Optional[str] = None) -> dict:
    """
    获取城市天气信息
    
    使用 wttr.in 免费API，支持：
    - 实时天气
    - 未来3天预报
    - 指定日期天气（有限）
    
    Args:
        city: 城市名称（如"拉萨"、"拉萨市"）
        date: 可选，指定日期（格式 YYYY-MM-DD）
              如果不指定，返回当前天气
        
    Returns:
        天气信息字典，包含：
        - temp: 温度
        - weather: 天气状况
        - wind: 风力
        - humidity: 湿度
        - feels_like: 体感温度
        - uv_index: 紫外线指数
        - tips: 出行建议
        如果获取失败返回空字典
    """
    if not city:
        return {}
    
    # 清理城市名（去掉"市"、"县"等后缀）
    city = city.strip().replace("市", "").replace("县", "").replace("区", "")
    
    try:
        # wttr.in API
        url = f"https://wttr.in/{city}"
        params = {
            "format": "j1",  # JSON格式
            "lang": "zh",   # 中文
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        with httpx.Client(timeout=10) as client:
            resp = client.get(url, params=params, headers=headers)
            resp.raise_for_status()
            data = resp.json()
        
        # 解析天气数据
        weather_info = _parse_wttr_response(data, city)
        return weather_info
        
    except httpx.HTTPError as e:
        logger.warning(f"天气查询HTTP错误: {city}, {e}")
        return {}
    except Exception as e:
        logger.warning(f"天气查询失败: {city}, {e}")
        return {}


def _parse_wttr_response(data: dict, city: str) -> dict:
    """
    解析 wttr.in 返回的JSON数据
    
    Args:
        data: wttr.in返回的原始数据
        city: 查询的城市名
        
    Returns:
        解析后的天气信息字典
    """
    try:
        # 获取当前天气（nearest area）
        nearest = data.get("nearest_area", [{}])
        area_name = nearest[0].get("areaName", [{}])[0].get("value", city) if nearest else city
        country = nearest[0].get("country", [{}])[0].get("value", "") if nearest else ""
        
        # 获取当前天气
        current = data.get("current_condition", [{}])[0]
        
        temp = current.get("temp_C", "N/A")
        weather_code = current.get("weatherCode", "0")
        weather_desc = _get_weather_desc(weather_code)
        wind_speed = current.get("windspeedKmph", "0")
        wind_dir = current.get("winddir16Point", "")
        humidity = current.get("humidity", "0")
        feels_like = current.get("FeelsLikeC", temp)
        uv_index = current.get("uvIndex", "0")
        visibility = current.get("visibility", "0")
        pressure = current.get("pressure", "0")
        
        # 获取今天和未来几天
        weather_forecast = []
        for i, day_data in enumerate(data.get("weather", [])[:3]):
            date_str = day_data.get("date", "")
            max_temp = day_data.get("maxtempC", "")
            min_temp = day_data.get("mintempC", "")
            avg_humidity = day_data.get("avghumidity", "")
            
            # 获取小时详情
            hourly = day_data.get("hourly", [])
            if hourly:
                noon_hour = hourly[4] if len(hourly) > 4 else hourly[0]
                forecast_weather = noon_hour.get("weatherCode", weather_code)
            else:
                forecast_weather = weather_code
            
            weather_forecast.append({
                "date": date_str,
                "max_temp": max_temp,
                "min_temp": min_temp,
                "weather": _get_weather_desc(forecast_weather),
                "humidity": avg_humidity,
            })
        
        # 生成出行建议
        tips = _generate_tips(temp, weather_desc, wind_speed, uv_index)
        
        return {
            "city": area_name,
            "country": country,
            "temp": temp,
            "weather": weather_desc,
            "wind": f"{wind_speed}km/h {wind_dir}",
            "humidity": f"{humidity}%",
            "feels_like": feels_like,
            "uv_index": uv_index,
            "visibility": visibility,
            "pressure": pressure,
            "forecast": weather_forecast,
            "tips": tips,
        }
        
    except Exception as e:
        logger.warning(f"解析天气数据失败: {e}")
        return {}


def _get_weather_desc(code: str) -> str:
    """
    将天气代码转换为描述
    
    Args:
        code: wttr.in天气代码
        
    Returns:
        天气描述
    """
    weather_codes = {
        "0": "☀️ 晴",
        "1": "🌤️ 基本晴",
        "2": "⛅ 多云",
        "3": "☁️ 阴",
        "4": "🌫️ 雾",
        "5": "🌫️ 薄雾",
        "6": "🌫️ 冰雾",
        "7": "🌫️ 冰雾",
        "8": "🌨️ 小冰雹",
        "9": "🌧️ 小雨",
        "10": "🌧️ 中雨",
        "11": "🌧️ 大雨",
        "12": "🌧️ 暴雨",
        "13": "🌨️ 小雪",
        "14": "🌨️ 中雪",
        "15": "❄️ 大雪",
        "16": "❄️ 暴雪",
        "17": "⛈️ 雷暴",
        "18": "🌧️ 倾盆大雨",
        "19": "🌨️ 雨夹雪",
        "20": "🌨️ 冻雨",
        "21": "🌨️ 小阵雪",
        "22": "🌨️ 中阵雪",
        "23": "🌨️ 大阵雪",
        "24": "🌨️ 冻雾",
        "25": "🌨️ 雷阵雨",
        "26": "🌨️ 阵雨",
        "27": "🌨️ 大阵雨",
        "28": "🌨️ 大雷阵雨",
        "29": "⛈️ 雷阵雨",
        "30": "🌫️ 沙尘",
        "31": "🌫️ 沙尘",
        "32": "🌬️ 大风",
        "33": "🌙 晴夜",
        "34": "🌤️ 基本晴夜",
        "35": "⛅ 多云夜",
        "36": "☁️ 阴夜",
        "37": "🌫️ 雾夜",
        "38": "🌫️ 薄雾夜",
        "39": "🌧️ 小雨夜",
        "40": "🌧️ 中雨夜",
    }
    return weather_codes.get(code, "未知天气")


def _generate_tips(temp: str, weather: str, wind_speed: str, uv_index: str) -> str:
    """
    根据天气情况生成出行建议
    
    Args:
        temp: 温度
        weather: 天气描述
        wind_speed: 风速
        uv_index: 紫外线指数
        
    Returns:
        出行建议
    """
    tips = []
    
    try:
        temp_val = float(temp) if temp else 20
        wind_val = float(wind_speed) if wind_speed else 0
        uv_val = float(uv_index) if uv_index else 0
        
        # 温度建议
        if temp_val < 0:
            tips.append("❄️ 天气寒冷，注意保暖羽绒服")
        elif temp_val < 10:
            tips.append("🧥 天气较凉，建议穿厚外套")
        elif temp_val < 20:
            tips.append("🧣 天气凉爽，适合薄外套")
        elif temp_val < 30:
            tips.append("👕 天气温暖，舒适出行")
        else:
            tips.append("🥵 天气炎热，注意防暑")
        
        # 天气建议
        if "雨" in weather or "雪" in weather:
            tips.append("🌂 记得带伞/注意防滑")
        if "雾" in weather or "霾" in weather:
            tips.append("😷 能见度低，出行注意安全")
        if "晴" in weather and uv_val > 5:
            tips.append("🧴 紫外线较强，注意防晒")
        
        # 风速建议
        if wind_val > 30:
            tips.append("💨 风速较大，避免高空作业")
        elif wind_val > 15:
            tips.append("🌬️ 风力适中，注意防风")
            
    except (ValueError, TypeError):
        tips.append("👔 根据天气适当增减衣物")
    
    return " | ".join(tips) if tips else "👔 根据天气适当增减衣物"


def get_weather_brief(city: str) -> str:
    """
    获取简短天气信息（用于快速展示）
    
    Args:
        city: 城市名称
        
    Returns:
        简短天气描述，如 "25°C ☀️ 晴 微风"
    """
    weather = get_weather(city)
    if not weather:
        return "天气未知"
    
    temp = weather.get("temp", "N/A")
    desc = weather.get("weather", "未知")
    wind = weather.get("wind", "")
    
    # 简化风速描述
    wind_short = ""
    if wind:
        try:
            speed = float(wind.split("km/h")[0].strip()) if "km/h" in wind else 0
            if speed < 10:
                wind_short = "微风"
            elif speed < 20:
                wind_short = "和风"
            elif speed < 30:
                wind_short = "清风"
            else:
                wind_short = "大风"
        except (ValueError, IndexError):
            wind_short = wind
    
    return f"{temp}°C {desc} {wind_short}"


def get_weather_for_dates(city: str, dates: list[str]) -> dict[str, dict]:
    """
    获取指定日期列表的天气信息
    
    Args:
        city: 城市名称
        dates: 日期列表（格式 YYYY-MM-DD）
        
    Returns:
        日期到天气的字典
    """
    result = {}
    
    try:
        url = f"https://wttr.in/{city}"
        params = {"format": "j1", "lang": "zh"}
        
        headers = {"User-Agent": "Mozilla/5.0"}
        
        with httpx.Client(timeout=10) as client:
            resp = client.get(url, params=params, headers=headers)
            resp.raise_for_status()
            data = resp.json()
        
        forecasts = data.get("weather", [])
        
        for date_str in dates:
            # 简单匹配（只取预报天数内的）
            for forecast in forecasts[:len(dates)]:
                result[date_str] = {
                    "max_temp": forecast.get("maxtempC", ""),
                    "min_temp": forecast.get("mintempC", ""),
                    "weather": _get_weather_desc(
                        forecast.get("hourly", [{}])[4].get("weatherCode", "0") 
                        if forecast.get("hourly") else "0"
                    ),
                }
                
    except Exception as e:
        logger.warning(f"批量天气查询失败: {e}")
    
    return result
