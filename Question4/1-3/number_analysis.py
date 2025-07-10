import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# 设置matplotlib支持中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体字体
plt.rcParams['axes.unicode_minus'] = False    # 解决负号 '-' 显示为方块的问题

# 读取数据
data_path = 'dlt_data_last100.csv'
data = pd.read_csv(data_path)

# 统计前区和后区号码的频率
def count_numbers(column):
    all_numbers = []
    for numbers in data[column]:
        # 去掉字符串中的方括号和单引号，并分割成列表
        numbers_list = numbers.strip("[]").replace("'", "").split(", ")
        all_numbers.extend(numbers_list)
    return Counter(all_numbers)

front_numbers_count = count_numbers('前区')
back_numbers_count = count_numbers('后区')

# 转换为DataFrame以便绘图
front_df = pd.DataFrame(list(front_numbers_count.items()), columns=['号码', '频次']).sort_values(by='号码')
back_df = pd.DataFrame(list(back_numbers_count.items()), columns=['号码', '频次']).sort_values(by='号码')

# 绘制前区号码的柱状图
fig, ax = plt.subplots(figsize=(14, 7))
bar = sns.barplot(x='号码', y='频次', data=front_df, color='red')  # 取消渐变，使用纯色

# 添加网格背景
ax.grid(True, which='major', axis='y', linestyle='--', color='lightgray', alpha=0.7)

# 在柱上标注数值
for p in bar.patches:
    ax.text(p.get_x() + p.get_width() / 2., p.get_height(),
            f'{int(p.get_height())}',
            ha='center', va='bottom', fontsize=10)

# 图表美化
plt.title('前区号码频率统计', fontsize=14)
plt.xlabel('号码')
plt.ylabel('频次')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('front_numbers_frequency.png')
plt.show()

# 绘制后区号码的柱状图
fig, ax = plt.subplots(figsize=(10, 6))
bar = sns.barplot(x='号码', y='频次', data=back_df, color='blue')  # 取消渐变，使用纯色

# 添加网格背景
ax.grid(True, which='major', axis='y', linestyle='--', color='lightgray', alpha=0.7)

# 在柱上标注数值
for p in bar.patches:
    ax.text(p.get_x() + p.get_width() / 2., p.get_height(),
            f'{int(p.get_height())}',
            ha='center', va='bottom', fontsize=10)

# 图表美化
plt.title('后区号码频率统计', fontsize=14)
plt.xlabel('号码')
plt.ylabel('频次')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('back_numbers_frequency.png')
plt.show()