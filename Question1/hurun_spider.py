import requests
import pandas as pd
from time import sleep
import random

all_data = []
# 循环请求1-6页
for page in range(1,7):
	# 胡润百富榜地址
	sleep_seconds = random.uniform(1, 2)
	#print('开始等待{}秒'.format(sleep_seconds))
	sleep(sleep_seconds)
	print('开始爬取第{}页'.format(page))
	offset = (page - 1) * 200
	url = ('https://www.hurun.net/zh-CN/Rank/HsRankDetailsList?num=ODBYW2BI&search=&offset={}&limit=200'
		   .format(offset))
	# 构造请求头
	headers = {
		'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Mobile Safari/537.36',
		'accept': 'application/json, text/javascript, */*; q=0.01',
		'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
		'accept-encoding': 'gzip, deflate, br',
		'content-type': 'application/json',
		'referer': 'https://www.hurun.net/zh-CN/Rank/HsRankDetails?pagetype=rich'
	}
	# 发送请求
	response = requests.get(url, headers=headers)

	json_data = response.json()
	rows = json_data.get('rows', [])
	# 解析每条记录
	for row in rows:
		basic_info = {
			"掌权人": row.get("hs_Rank_Rich_ChaName_Cn"),
			"排名": row.get("hs_Rank_Rich_Ranking"),
			"排名变化": row.get("hs_Rank_Rich_Ranking_Change"),
			"财富值_人民币_亿": row.get("hs_Rank_Rich_Wealth"),
			"财富值_美元": row.get("hs_Rank_Rich_Wealth_USD"),
			"财富值变化": row.get("hs_Rank_Rich_Wealth_Change"),
			"人物关系": row.get("hs_Rank_Rich_Relations"),
			"公司名称_中文": row.get("hs_Rank_Rich_ComName_Cn"),
			"公司名称_英文": row.get("hs_Rank_Rich_ComName_En"),
			"公司总部地_中文": row.get("hs_Rank_Rich_ComHeadquarters_Cn"),
			"公司总部地_英文": row.get("hs_Rank_Rich_ComHeadquarters_En"),
			"所在行业_中文": row.get("hs_Rank_Rich_Industry_Cn"),
			"所在行业_英文": row.get("hs_Rank_Rich_Industry_En")
		}
	# 提取基本信息
		char_data = row["hs_Character"][0]  # 取第一个元素，省略其他人物信息（如果有）
		character_info = {
			"性别": char_data.get("hs_Character_Gender"),
			"年龄": char_data.get("hs_Character_Age"),
			"出生地_中文": char_data.get("hs_Character_BirthPlace_Cn"),
			"籍贯_中文": char_data.get("hs_Character_NativePlace_Cn"),
			"常住地_中文": char_data.get("hs_Character_Permanent_Cn"),
			"学历_中文": char_data.get("hs_Character_Education_Cn"),
			"毕业院校_中文": char_data.get("hs_Character_School_Cn"),
			"毕业院校_英文": char_data.get("hs_Character_School_En"),
			"专业_中文": char_data.get("hs_Character_Major_Cn"),
			"专业_英文": char_data.get("hs_Character_Major_En")
			}

		# 合并基础信息和人物信息
		combined_data = {**basic_info, **character_info}

		# 添加到总数据列表
		all_data.append(combined_data)

df = pd.DataFrame(all_data)
df.to_csv("hurun_baifu_list_2024.csv", index=False, encoding='utf_8_sig')