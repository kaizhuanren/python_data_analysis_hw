import pandas as pd

df = pd.read_csv('hurun_baifu_list_2024_categorized.csv')

rich_cnt_1 = df.groupby('一级类别')['掌权人'].count()
rich_cnt_2 = df.groupby('二级类别')['掌权人'].count()
wealth_sum_1 = df.groupby('一级类别')['财富值_人民币_亿'].sum()
wealth_sum_2 = df.groupby('二级类别')['财富值_人民币_亿'].sum()
wealth_mean_1 = df.groupby('一级类别')['财富值_人民币_亿'].mean()
wealth_mean_2 = df.groupby('二级类别')['财富值_人民币_亿'].mean()

df.loc[df['财富值变化'] == 'NEW', '财富值变化'] = '0%'
df['财富值_去年'] = df['财富值_人民币_亿'] / (1 - df['财富值变化'].str.strip('%').astype(float)/100)
df['财富增量'] = df['财富值_人民币_亿'] * ((1/(1 - df['财富值变化'].str.strip('%').astype(float)/100))-1) #去年财富值-今年财富值

wealth_change_1 = df.groupby('一级类别').agg(
    增量_sum=('财富增量', 'sum'),
    财富值_sum=('财富值_去年', 'sum')
)

wealth_change_2 = df.groupby('二级类别').agg(
    增量_sum=('财富增量', 'sum'),
    财富值_sum=('财富值_去年', 'sum')
)

wealth_change_1['增长百分比'] = wealth_change_1['增量_sum'] / wealth_change_1['财富值_sum']
wealth_change_2['增长百分比'] = wealth_change_2['增量_sum'] / wealth_change_2['财富值_sum']


#可视化
import matplotlib.pyplot as plt
import matplotlib as mpl

# 设置中文字体支持
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

# # 1. 掌权人数量分布
# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))
# rich_cnt_1.sort_values(ascending=False).plot.bar(ax=ax1, color='skyblue')
# ax1.set_title('一级类别掌权人数量分布', fontsize=14)
# ax1.set_ylabel('人数')
#
# rich_cnt_2.sort_values(ascending=False).head(10).plot.bar(ax=ax2, color='salmon')
# ax2.set_title('二级类别掌权人数量TOP10', fontsize=14)
# plt.tight_layout()
# plt.savefig('掌权人数量分布.png', dpi=300)
#
# # 2. 财富总值分布
# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))
# wealth_sum_1.sort_values(ascending=False).plot.bar(ax=ax1, color='skyblue')
# ax1.set_title('一级类别财富总值分布', fontsize=14)
# ax1.set_ylabel('财富总值（亿人民币）')
#
# wealth_sum_2.sort_values(ascending=False).head(10).plot.bar(ax=ax2, color='salmon')
# ax2.set_title('二级类别财富总值TOP10', fontsize=14)
# plt.tight_layout()
# plt.savefig('财富总值分布.png', dpi=300)
#
# # 3. 人均财富分布
# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))
# wealth_mean_1.sort_values(ascending=False).plot.bar(ax=ax1, color='skyblue')
# ax1.set_title('一级类别人均财富', fontsize=14)
# ax1.set_ylabel('平均财富（亿人民币）')
#
# wealth_mean_2.sort_values(ascending=False).head(10).plot.bar(ax=ax2, color='salmon')
# ax2.set_title('二级类别人均财富TOP10', fontsize=14)
# plt.tight_layout()
# plt.savefig('人均财富分布.png', dpi=300)
#
# # 4. 财富增长率分布
# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))
# wealth_change_1['增长百分比'].sort_values(ascending=False).plot.bar(ax=ax1, color='skyblue')
# ax1.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)
# ax1.set_title('一级类别财富增长率', fontsize=14)
# ax1.set_ylabel('增长率')
#
# wealth_change_2['增长百分比'].sort_values(ascending=False).head(10).plot.bar(ax=ax2, color='salmon')
# ax2.set_title('二级类别财富增长率TOP10', fontsize=14)
# plt.tight_layout()
# plt.savefig('财富增长率分布.png', dpi=300)

plt.rcParams.update({'font.size': 14, 'axes.titlesize': 16})
# 7. 一级类别财富增长率
plt.figure(figsize=(12, 8))
wealth_change_1['增长百分比'].sort_values(ascending=False).plot.bar(color='skyblue')
plt.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)
plt.title('一级类别财富增长率', pad=20)
plt.ylabel('增长率')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('一级类别财富增长率.png', dpi=300)
plt.close()

# 8. 二级类别财富增长率TOP10
plt.figure(figsize=(12, 8))
wealth_change_2['增长百分比'].sort_values(ascending=False).head(10).plot.bar(color='salmon')
plt.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)
plt.title('二级类别财富增长率TOP10', pad=20)
plt.ylabel('增长率')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('二级类别财富增长率TOP10.png', dpi=300)
plt.close()

# 9. 二级类别财富增长率LAST10
plt.figure(figsize=(12, 8))
wealth_change_2['增长百分比'].sort_values(ascending=False).tail(10).plot.bar(color='salmon')
plt.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)
plt.title('二级类别财富增长率LAST10', pad=20)
plt.ylabel('增长率')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('二级类别财富增长率LAST10.png', dpi=300)
plt.close()