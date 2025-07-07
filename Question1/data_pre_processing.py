import pandas as pd

df = pd.read_csv("hurun_baifu_list_2024.csv")

df.rename(columns={"财富值_美元": "财富值_美元_百万"}, inplace=True)
df.loc[df['人物关系'] == '未知', '人物关系'] = '个人'
df.loc[df['性别'] == '先生', '性别'] = '男'
df.loc[df['性别'] == '女士', '性别'] = '女'

df.loc[df['所在行业_中文'] == '北京', '所在行业_中文'] = '智能硬件与技术'    #小米的错误信息
df.iat[166, 10] = 'Beijing'     #公司总部地_英文错误信息
df.iat[75, 15] = '中国-山东-淄博'

df.drop(columns=['学历_中文', '毕业院校_中文', '毕业院校_英文', '专业_中文', '专业_英文'], inplace=True)     #学历未知远多于已知，删除，不作分析

df.to_csv("hurun_baifu_list_2024_processed.csv", index=False)