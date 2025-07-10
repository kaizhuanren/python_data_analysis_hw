import requests
import pandas as pd
from time import sleep
import random
from bs4 import BeautifulSoup

all_data = []
ids = ['1958734', '2379124', '2930378', '3098515', '2886139', '3122717', '2901280', '2037784', '3103268', '2437623', '2835466', '2232902', '1797236', '2998706', '758781', '2940702', '3055732', '2043028', '2336694', '2368156', '1919444']
for id in ids:
	sleep_seconds = random.uniform(1, 2)
	sleep(sleep_seconds)
	print('开始爬取id为{}的用户'.format(id))
	url = ('https://www.cmzj.net/expertItem?id={}'
		   .format(id))
	# 构造请求头
	headers = {
		'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Mobile Safari/537.36',
		'accept': 'application/json, text/javascript, */*; q=0.01',
		'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
		'accept-encoding': 'gzip, deflate, br',
		'content-type': 'application/json',
		'referer': 'https://www.cmzj.net/expertItem/'
	}
	response = requests.get(url, headers=headers)
	response.encoding = "utf-8"  # 根据实际页面编码调整

	# 解析HTML
	soup = BeautifulSoup(response.text, "html.parser")
	print(soup)
	data = {}

	# 提取姓名
	name = soup.find('p', class_='okami-name').get_text(strip=True)
	data['姓名'] = name

	# 提取彩龄
	cailing = soup.select_one('.okami-text > p:nth-of-type(1) > span').get_text(strip=True)
	data['彩龄'] = cailing

	# 提取文章数量
	article_count = soup.select_one('.okami-text > p:nth-of-type(2) > span').get_text(strip=True)
	data['文章数量'] = article_count

	# 提取专家简介
	intro = soup.find('span', class_='titleText').get_text(strip=True)
	data['专家简介'] = intro

	# 提取彩种等级
	levels = [span.get_text(strip=True) for span in soup.select('.czdj span')]
	data['彩种等级'] = levels

	# 提取大奖战绩
	battle_records = {}
	for djzj_div in soup.select('.djzjP .djzj'):
		game_name = djzj_div.find('span', class_='text-head-bg').get_text(strip=True)
		items = djzj_div.select('.item')
		record = {}
		for item in items:
			key = item.contents[0].strip()
			value = item.find('span').get_text(strip=True)
			record[key] = value
		battle_records[game_name] = record

	data['大奖战绩'] = battle_records

	all_data.append(data)

df = pd.DataFrame(all_data)
df.to_csv("expert_data.csv", index=False, encoding='utf_8_sig')