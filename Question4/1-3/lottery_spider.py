import requests
import pandas as pd
from datetime import datetime
import random
from time import sleep


# 用户代理列表
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
]

def fetch_dlt_history():

    api_url = "https://webapi.sporttery.cn/gateway/lottery/getHistoryPageListV1.qry"
    all_data = []
    for i in range(1,3):
        params = {
            "gameNo": "85",
            "provinceId": "0",
            "pageSize": "100",
            "isVerify": "1",
            "pageNo": "{}".format(i)
        }

        headers = {
            'User-Agent': random.choice(USER_AGENTS),
            'Referer': 'https://www.lottery.gov.cn/'
        }

        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        if data['success']:
            for item in data['value']['list']:
                period = item['lotteryDrawNum']
                date = datetime.strptime(item['lotteryDrawTime'], '%Y-%m-%d')
                numbers = item['lotteryDrawResult'].split()
                red_balls = numbers[:5]
                blue_balls = numbers[5:7]

                # 处理销售额字符串（去除逗号）
                sales_str = item['totalSaleAmount'].replace(',', '')
                sales = int(sales_str) *10000 # 转换为元

                all_data.append({
                    '期号': period,
                    '开奖日期': date,
                    '前区': red_balls,
                    '后区': blue_balls,
                    '销售额': sales
                })

    return pd.DataFrame(all_data)


if __name__ == "__main__":
    df = fetch_dlt_history()
    df = df.iloc[3:104]
    df['销售额'] = df['销售额']/10000
    df.to_csv('dlt_data_last100.csv', index=False, encoding='utf_8_sig')
