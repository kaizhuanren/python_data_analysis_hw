import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv('hurun_baifu_list_2024_processed.csv')

# 创建画布
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# 1. 性别分布饼图 - 过滤掉未知性别
# 统计性别分布
df_sex = df.groupby('性别')['掌权人'].count()

# 过滤掉"未知"性别
if '未知' in df_sex.index:
    df_sex = df_sex.drop('未知')

# 设置颜色 - 只保留男性和女性颜色
sex_colors = ['#FF9999', '#66B2FF']  # 女-粉, 男-蓝

# 绘制饼图
wedges, texts, autotexts = ax1.pie(
    df_sex,
    labels=df_sex.index,
    autopct=lambda p: f'{p:.1f}%' if p > 0 else '',
    startangle=90,
    colors=sex_colors[:len(df_sex)],  # 根据类别数量选择颜色
    wedgeprops={'edgecolor': 'white', 'linewidth': 1},
    textprops={'fontsize': 12}
)

# 设置饼图中心空白区域
centre_circle = plt.Circle((0, 0), 0.70, fc='white')
ax1.add_artist(centre_circle)

# 添加标题
ax1.set_title('富豪性别分布', fontsize=15, pad=20)

# 2. 年龄段分布柱状图（保持不变）
# 统计年龄段分布
age_data = {
    '30-39': 0, '40-49': 0, '50-59': 0, '60-69': 0, '70-79': 0, '>=80': 0
}

for index, row in df.iterrows():
    age_str = row['年龄']
    if age_str == '未知':
        continue
    age = int(age_str)
    if 30 <= age < 40:
        age_data['30-39'] += 1
    elif 40 <= age < 50:
        age_data['40-49'] += 1
    elif 50 <= age < 60:
        age_data['50-59'] += 1
    elif 60 <= age < 70:
        age_data['60-69'] += 1
    elif 70 <= age < 80:
        age_data['70-79'] += 1
    elif age >= 80:
        age_data['>=80'] += 1

s_age = pd.Series(age_data)

# 设置年龄段颜色（按年龄渐变）
age_colors = plt.cm.Blues(np.linspace(0.4, 1, len(s_age)))

# 绘制柱状图
bars = ax2.bar(
    s_age.index,
    s_age.values,
    color=age_colors,
    edgecolor='white',
    linewidth=1.2
)

# 添加数据标签
for bar in bars:
    height = bar.get_height()
    ax2.annotate(f'{height}',
                 xy=(bar.get_x() + bar.get_width() / 2, height),
                 xytext=(0, 3),  # 3 points vertical offset
                 textcoords="offset points",
                 ha='center', va='bottom',
                 fontsize=11)

# 设置Y轴范围
max_value = s_age.max()
ax2.set_ylim(0, max_value * 1.15)

# 添加网格线
ax2.grid(axis='y', linestyle='--', alpha=0.7)

# 设置标题和标签
ax2.set_title('富豪年龄段分布', fontsize=15, pad=15)
ax2.set_xlabel('年龄段', fontsize=12)
ax2.set_ylabel('人数', fontsize=12)

# 优化X轴标签
ax2.set_xticklabels(s_age.index, rotation=15, ha='right')

fig.text(0.5, 0.93,
         f'2024胡润富豪榜分析',
         ha='center', fontsize=16, fontweight='bold')

# 调整布局
plt.tight_layout(rect=[0, 0, 1, 0.92])  # 为顶部标题留空间

# 保存图表
plt.savefig('富豪性别与年龄分布.png', dpi=300, bbox_inches='tight')
plt.show()