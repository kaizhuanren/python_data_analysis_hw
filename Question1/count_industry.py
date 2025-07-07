import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv('hurun_baifu_list_2024_processed.csv', encoding='utf-8')

# 初始化一个空列表用于存储所有行业
all_industries = []

# 遍历每一行，分割行业并添加到列表中
for industries in df['所在行业_中文'].dropna():
    all_industries.extend(industries.split('、'))

# 使用 Counter 统计每个行业的出现次数
industry_count = dict(Counter(all_industries))
print(len(industry_count))
#print(industry_count)

# 按照出现次数从大到小排序，并选出前20个
top_20_industries = dict(sorted(industry_count.items(), key=lambda item: item[1], reverse=True)[:20])
print(top_20_industries)

# 绘制柱状图
plt.figure(figsize=(14, 8)) # 调整图表大小以便更好地展示文字
plt.barh(list(top_20_industries.keys()), top_20_industries.values(), color='skyblue')
plt.xlabel('出现次数')
plt.ylabel('行业')
plt.title('出现次数最多的20个行业')
plt.gca().invert_yaxis() # 从上至下按次数从高到低排列
plt.tight_layout() # 自动调整子图参数,使之填充整个图像区域
plt.show()