import requests
import pandas as pd
from time import sleep
import random
from bs4 import BeautifulSoup

weather_history = []
for year in range(2, 5):
    for month in range(1, 13):
        sleep_seconds = random.uniform(1, 2)
        #print('开始等待{}秒'.format(sleep_seconds))
        sleep(sleep_seconds)
        print('开始爬取202{}年{}月天气信息'.format(year, month))
        YEAR = '202' + str(year)
        MONTH = str(month)
        if len(MONTH) == 1 :
            MONTH = '0'+MONTH
        url = 'https://www.tianqihoubao.com/lishi/dalian/month/{}{}.html'.format(YEAR, MONTH)
        # 构造请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Mobile Safari/537.36',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'accept-encoding': 'gzip, deflate, br',
            'content-type': 'application/json',
            'referer': 'https://www.tianqihoubao.com/lishi/dalian/month/'
        }
        # 发送请求
        response = requests.get(url, headers=headers)
        response.encoding = "utf-8"  # 根据实际页面编码调整

        # 解析HTML
        soup = BeautifulSoup(response.text, "html.parser")

        table = soup.find('table', {'class': 'weather-table'})

        jump = 0
        for row in table.find('tbody').find_all('tr'):
            jump += 1
            columns = row.find_all('td')
            if jump == 11 or jump == 22:    #跳过空行
                continue

            #获取日期
            date = columns[0].get_text(strip=True)
            # 提取天气状况
            weather_conditions = columns[1].get_text(strip=True).split('/')
            daytime_weather = weather_conditions[0].strip()
            nighttime_weather = weather_conditions[1].strip()

            # 提取最高/最低气温
            temperatures = columns[2].find_all('span')
            high_temp = temperatures[0].get_text(strip=True).strip()[:-1]
            low_temp = temperatures[1].get_text(strip=True).strip()[:-1]

            # 提取风力风向
            wind_conditions = columns[3].get_text(strip=True).split('/')
            daytime_wind = wind_conditions[0].strip()[-4:-1]
            nighttime_wind = wind_conditions[1].strip()[-4:-1]

            # 将提取的信息存入字典
            data_dict = {
                '日期': date,
                '白天天气': daytime_weather,
                '夜间天气': nighttime_weather,
                '最高气温(℃)': high_temp,
                '最低气温(℃)': low_temp,
                '白天风力(级)': daytime_wind,
                '夜间风力(级)': nighttime_wind,
            }
            # 添加到列表
            weather_history.append(data_dict)

df = pd.DataFrame(weather_history)
df.to_csv("weather_history_2022_to_2024.csv", index=False, encoding='utf_8_sig')

#爬取2025年1-6月最高气温
temperature_2025_real = []
for month in range(1, 7):
    sleep_seconds = random.uniform(1, 2)
    # print('开始等待{}秒'.format(sleep_seconds))
    sleep(sleep_seconds)
    print('开始爬取202{}年{}月天气信息'.format(5, month))
    #YEAR = '202' + str(year)
    MONTH = str(month)
    if len(MONTH) == 1:
        MONTH = '0' + MONTH
    url = 'https://www.tianqihoubao.com/lishi/dalian/month/{}{}.html'.format(2025, MONTH)
    # 构造请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Mobile Safari/537.36',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'accept-encoding': 'gzip, deflate, br',
        'content-type': 'application/json',
        'referer': 'https://www.tianqihoubao.com/lishi/dalian/month/'
    }
    # 发送请求
    response = requests.get(url, headers=headers)
    response.encoding = "utf-8"  # 根据实际页面编码调整

    # 解析HTML
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find('table', {'class': 'weather-table'})

    jump = 0
    for row in table.find('tbody').find_all('tr'):
        jump += 1
        columns = row.find_all('td')
        if jump == 11 or jump == 22:  # 跳过空行
            continue

        # 获取日期
        date = columns[0].get_text(strip=True)
        # 提取天气状况
        # weather_conditions = columns[1].get_text(strip=True).split('/')
        # daytime_weather = weather_conditions[0].strip()
        # nighttime_weather = weather_conditions[1].strip()

        # 提取最高/最低气温
        temperatures = columns[2].find_all('span')
        high_temp = temperatures[0].get_text(strip=True).strip()[:-1]
        #low_temp = temperatures[1].get_text(strip=True).strip()[:-1]

        # # 提取风力风向
        # wind_conditions = columns[3].get_text(strip=True).split('/')
        # daytime_wind = wind_conditions[0].strip()[-4:-1]
        # nighttime_wind = wind_conditions[1].strip()[-4:-1]

        # 将提取的信息存入字典
        data_dict = {
            '日期': date,
            # '白天天气': daytime_weather,
            # '夜间天气': nighttime_weather,
            '最高气温(℃)': high_temp,
            #'最低气温(℃)': low_temp,
            # '白天风力(级)': daytime_wind,
            # '夜间风力(级)': nighttime_wind,
        }
        # 添加到列表
        temperature_2025_real.append(data_dict)

df1 = pd.DataFrame(temperature_2025_real)
df1.to_csv("temperature_2025_real.csv", index=False, encoding='utf_8_sig')

#爬取2020-2024年各月最高气温
temperature_2020_to_2024_real = []
for year in range(0, 5):
    for month in range(1, 13):
        sleep_seconds = random.uniform(1, 2)
        #print('开始等待{}秒'.format(sleep_seconds))
        sleep(sleep_seconds)
        print('开始爬取202{}年{}月天气信息'.format(year, month))
        YEAR = '202' + str(year)
        MONTH = str(month)
        if len(MONTH) == 1 :
            MONTH = '0'+MONTH
        url = 'https://www.tianqihoubao.com/lishi/dalian/month/{}{}.html'.format(YEAR, MONTH)
        # 构造请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Mobile Safari/537.36',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'accept-encoding': 'gzip, deflate, br',
            'content-type': 'application/json',
            'referer': 'https://www.tianqihoubao.com/lishi/dalian/month/'
        }
        # 发送请求
        response = requests.get(url, headers=headers)
        response.encoding = "utf-8"  # 根据实际页面编码调整

        # 解析HTML
        soup = BeautifulSoup(response.text, "html.parser")

        table = soup.find('table', {'class': 'weather-table'})

        jump = 0
        for row in table.find('tbody').find_all('tr'):
            jump += 1
            columns = row.find_all('td')
            if jump == 11 or jump == 22:    #跳过空行
                continue

            #获取日期
            date = columns[0].get_text(strip=True)
            # # 提取天气状况
            # weather_conditions = columns[1].get_text(strip=True).split('/')
            # daytime_weather = weather_conditions[0].strip()
            # nighttime_weather = weather_conditions[1].strip()

            # 提取最高/最低气温
            temperatures = columns[2].find_all('span')
            high_temp = temperatures[0].get_text(strip=True).strip()[:-1]
            # low_temp = temperatures[1].get_text(strip=True).strip()[:-1]

            # # 提取风力风向
            # wind_conditions = columns[3].get_text(strip=True).split('/')
            # daytime_wind = wind_conditions[0].strip()[-4:-1]
            # nighttime_wind = wind_conditions[1].strip()[-4:-1]

            # 将提取的信息存入字典
            data_dict = {
                '日期': date,
                # '白天天气': daytime_weather,
                # '夜间天气': nighttime_weather,
                '最高气温(℃)': high_temp,
                # '最低气温(℃)': low_temp,
                # '白天风力(级)': daytime_wind,
                # '夜间风力(级)': nighttime_wind,
            }
            # 添加到列表
            temperature_2020_to_2024_real.append(data_dict)

df = pd.DataFrame(temperature_2020_to_2024_real)
df.to_csv("temperature_2020_to_2024_real.csv", index=False, encoding='utf_8_sig')
