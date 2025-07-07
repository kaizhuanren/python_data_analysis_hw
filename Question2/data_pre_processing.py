import pandas as pd

df = pd.read_csv('weather_history_2022_to_2024.csv')

# 转换日期格式
df['日期'] = pd.to_datetime(df['日期'], format='%Y年%m月%d日')

# 提取年份和月份
df['年份'] = df['日期'].dt.year
df['月份'] = df['日期'].dt.month

df.to_csv('weather_history_2022_to_2024_processed.csv')


df = pd.read_csv('temperature_2025_real.csv')

# 转换日期格式
df['日期'] = pd.to_datetime(df['日期'], format='%Y年%m月%d日')

# 提取年份和月份
df['年份'] = df['日期'].dt.year
df['月份'] = df['日期'].dt.month

df.to_csv('temperature_2025_real.csv')

df = pd.read_csv('temperature_2020_to_2024_real.csv')

# 转换日期格式
df['日期'] = pd.to_datetime(df['日期'], format='%Y年%m月%d日')

# 提取年份和月份
df['年份'] = df['日期'].dt.year
df['月份'] = df['日期'].dt.month

df.to_csv('temperature_2020_to_2024_real.csv')
