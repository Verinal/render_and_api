"""api_key = "db317c10943b56933ed1d14a47a72b52"""

import requests
import jwt
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 允许跨域（前端调用时需要）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境请替换为具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class WeatherAPI:
    """天气API类"""

    def __init__(self,city_name):
        
        self.api_key = "db317c10943b56933ed1d14a47a72b52"
        self.headers = {
            'Authorization': f'Bearer {self.get_jwt()}'
        }
        self.city_name = city_name
    def get_jwt(self):
        try:
            print("正在获取JWT...")
            private_key = """-----BEGIN PRIVATE KEY-----
MC4CAQAwBQYDK2VwBCIEIDSvHxsMSAgBhSqjWxd05teMYqvX0WcKS2z8YbIvC11S
-----END PRIVATE KEY-----"""

            payload = {
                'iat': int(time.time()) - 30,
                'exp': int(time.time()) + 900,
                'sub': '24KXE2DQET' # project_id
            }
            headers = {
                'kid': 'K95D3KK2U4' # prvate_key_id
            }
            encoded_jwt = jwt.encode(payload, private_key, algorithm='EdDSA', headers = headers)
            return encoded_jwt
        except Exception as e:
            print(f'获取JWT时失败：{e}')
            return ''

    def get_area_id(self)->str:
        try:
            print("正在获取城市ID...")
            url = f"https://n65n8mj7jx.re.qweatherapi.com/geo/v2/city/lookup?location={self.city_name}"
            response = requests.get(url,headers=self.headers)
            data_json = response.json()
            city_id = data_json['location'][0]['id']
            return city_id
        except Exception as e:
            print(f'获取城市ID时失败：{e}')
            return ''
        
    def get_weather_forecasts(self, city_id:str)->str:
        try:
            print("正在获取实时天气预报...")
            url = f"https://n65n8mj7jx.re.qweatherapi.com/v7/weather/now?location={city_id}"
            response = requests.get(url,headers=self.headers)
            data = response.json()
            return data
        except Exception as e:
            print(f'获取实时天气预报时失败：{e}')
            return ''
    def run(self):
        # 获取城市ID
        city_id = self.get_area_id()
        # 获取天气预报
        data = self.get_weather_forecasts(city_id)
        print(data)

@app.post("/getWeather",city_name = str)
async def getWeather(city_name: str):
    """获取天气信息"""
    weather_api = WeatherAPI(city_name)
    json_data = weather_api.run()
    return json_data

if __name__ == "__main__":
    city_name = input("请输入城市名称：")
    weather_api = WeatherAPI(city_name).run()
    # city_name = "北京" # 测试

    