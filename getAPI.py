import json
import os.path
from datetime import datetime
import re

import requests
import jsondeal

_cityCode = jsondeal.get_citycode()
_Key=jsondeal.get_gaodeApikey()
_weather_chahe = "weather_chahe"


# def getIp():
#     try:
#         response_ip = requests.get(f'https://restapi.amap.com/v3/ip?key={_Key}')
#         if response_ip.status_code == 200:
#             data = response_ip.json()
#             return data['ip']
#         else:
#             return None
#     except Exception as e:
#         print(e)
#         return None

weather_mapping = {
    "晴": "Clear",
    "少云": "Few clouds",
    "晴间多云": "Partly cloudy",
    "多云": "Cloudy",
    "阴": "Overcast",
    "有风": "Windy",
    "平静": "Calm",
    "微风": "Light breeze",
    "和风": "Gentle breeze",
    "清风": "Fresh breeze",
    "强风/劲风": "Strong wind",
    "疾风": "Gale",
    "大风": "High wind",
    "烈风": "Blustery",
    "风暴": "Storm",
    "狂爆风": "Violent storm",
    "飓风": "Hurricane",
    "热带风暴": "Tropical storm",
    "霾": "Haze",
    "中度霾": "Moderate haze",
    "重度霾": "Heavy haze",
    "严重霾": "Severe haze",
    "阵雨": "Showers",
    "雷阵雨": "Thunderstorms",
    "雷阵雨并伴有冰雹": "Thunderstorms with hail",
    "小雨": "Light rain",
    "中雨": "Moderate rain",
    "大雨": "Heavy rain",
    "暴雨": "Rainstorm",
    "大暴雨": "Severe rainstorm",
    "特大暴雨": "Extraordinary rainstorm",
    "强阵雨": "Heavy showers",
    "强雷阵雨": "Severe thunderstorms",
    "极端降雨": "Extreme rainfall",
    "毛毛雨/细雨": "Drizzle",
    "雨": "Rain",
    "小雨-中雨": "Light to moderate rain",
    "中雨-大雨": "Moderate to heavy rain",
    "大雨-暴雨": "Heavy rain to rainstorm",
    "暴雨-大暴雨": "Rainstorm to severe rainstorm",
    "大暴雨-特大暴雨": "Severe rainstorm to extraordinary rainstorm",
    "雨雪天气": "Rain and snow",
    "雨夹雪": "Rain mixed with snow",
    "阵雨夹雪": "Showers mixed with snow",
    "冻雨": "Freezing rain",
    "雪": "Snow",
    "阵雪": "Snow showers",
    "小雪": "Light snow",
    "中雪": "Moderate snow",
    "大雪": "Heavy snow",
    "暴雪": "Blizzard",
    "小雪-中雪": "Light to moderate snow",
    "中雪-大雪": "Moderate to heavy snow",
    "大雪-暴雪": "Heavy snow to blizzard",
    "浮尘": "Dust",
    "扬沙": "Dusty",
    "沙尘暴": "Dust storm",
    "强沙尘暴": "Severe dust storm",
    "龙卷风": "Tornado",
    "雾": "Fog",
    "浓雾": "Thick fog",
    "强浓雾": "Dense fog",
    "轻雾": "Light fog",
    "大雾": "Heavy fog",
    "特强浓雾": "Severe fog",
    "热": "Hot",
    "冷": "Cold",
    "未知": "Unknown"
}

wind_direction_map = {
    '无风向': 'Calm',
    '东北': 'Northeast',
    '东': 'East',
    '东南': 'Southeast',
    '南': 'South',
    '西南': 'Southwest',
    '西': 'West',
    '西北': 'Northwest',
    '北': 'North',
    '旋转不定': 'Variable',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'
}

def getCityCode():
    try:
        response_citycode = requests.get(f'https://restapi.amap.com/v3/ip?key={_Key}',headers=headers)

        if response_citycode.status_code == 200:
            response_citycode = response_citycode.json()
            return response_citycode['adcode']

    except Exception as e:
        print("No Intneret (aCode)",e)
        return None


def getWeather():

    try:
        cityCode = getCityCode()
        if cityCode is None or len(cityCode) == 0:
            cityCode = _cityCode


        respone_weather = requests.get(
            f'https://restapi.amap.com/v3/weather/weatherInfo?parameters&city={cityCode}&key={_Key}',headers=headers)
        weather = respone_weather.json()

        if respone_weather.status_code == 200 or (not weather['status'] == 0):

            weather = weather['lives'][0]
            weathertemp(_cityCode,weather['weather'], weather['temperature'], weather['humidity'], weather['reporttime'],weather['winddirection'],weather['windpower'])
            return weather['weather'], weather['temperature'], weather['humidity'],weather['winddirection'],weather['windpower'],weather['reporttime']
        else:
            return getWeathertemp()
            # return "Offline", "Offline", "Offline"

    except Exception as e:
        # print("getWeather",e)
        print("无法获取网络天气")
        return getWeathertemp()


def get_weather_en_description(chinese_term):
    return weather_mapping.get(chinese_term, "Unknow")

def get_english_direction(chinese_direction):
    return wind_direction_map.get(chinese_direction, 'uknow')

def extract_numbers(text):
    return ''.join(re.findall(r'\d+', text))

def weathertemp(citycode,weather,temperature,humidity,reporttime,winddirection,windpower):
    _weather_chahe_json = {
        "cityCode": citycode,
        "weather": weather,
        "temp": temperature,
        "humidity": humidity,
        "winddirection": winddirection,
        "windpower": windpower,
        "reportime":reporttime,
        "updateTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    try:
        # if not os.path.exists(_weather_chahe):
        with open(_weather_chahe,"w") as file:
            file.write(json.dumps(_weather_chahe_json,ensure_ascii=False))

        # with open(_weather_chahe,"a") as file:
        #     file.write(_weather_chahe_json)
        # else:
        #     with open(_weather_chahe,"w") as file:
        #         file.write(_weather_chahe_json)
    except Exception as e:
        # print(e)
        print("无法存储本地天气")

def getWeathertemp():
    try:
        if not os.path.exists(_weather_chahe):
            weathertemp(_cityCode,"unknow","unknow","unknow","unknow","unknow","unknow")
        with open(_weather_chahe,"r") as file:
            _weather_chahe_json = file.read()
            weather = json.loads(_weather_chahe_json)
            return weather['weather'], weather['temp'], weather['humidity'], weather['winddirection'],weather['windpower'],weather['reportime']
    except Exception as e:
        print("gettemp",e)
        return "unknow","unknow","unknow","unknow","unknow","unknow"




