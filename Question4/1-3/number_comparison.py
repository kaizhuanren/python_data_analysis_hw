import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.font_manager import FontProperties
import ast

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

# 读取数据
df = pd.read_csv("dlt_data_last100.csv")

# 转换日期格式并提取星期几
df['开奖日期'] = pd.to_datetime(df['开奖日期'])
df['星期'] = df['开奖日期'].dt.weekday.map({0: '周一', 2: '周三', 5: '周六'})

# 转换字符串为实际列表
df['前区'] = df['前区'].apply(ast.literal_eval)
df['后区'] = df['后区'].apply(ast.literal_eval)

# 创建前区号码矩阵 (35个号码)
front_matrix = np.zeros((3, 35))  # 3行(周一、三、六) x 35列(前区号码)
back_matrix = np.zeros((3, 12))  # 3行(周一、三、六) x 12列(后区号码)

# 映射星期到索引
weekday_to_idx = {'周一': 0, '周三': 1, '周六': 2}

# 统计每个号码在不同星期的出现次数
for _, row in df.iterrows():
    week_idx = weekday_to_idx[row['星期']]

    # 统计前区
    for num in row['前区']:
        num_int = int(num) - 1  # 转换为0-34的索引
        front_matrix[week_idx, num_int] += 1

    # 统计后区
    for num in row['后区']:
        num_int = int(num) - 1  # 转换为0-11的索引
        back_matrix[week_idx, num_int] += 1

# 转换为频率 (出现次数/该星期的总期数)
for i in range(3):
    total_days = (df['星期'] == list(weekday_to_idx.keys())[i]).sum()
    front_matrix[i] /= total_days
    back_matrix[i] /= total_days

# 创建热力图（优化布局）
plt.figure(figsize=(15, 12))

# 前区热力图 (红色系)
ax1 = plt.subplot(2, 1, 1)
sns.heatmap(front_matrix,
            cmap='Reds',
            annot=False,
            linewidths=0.5,
            yticklabels=['周一', '周三', '周六'],
            xticklabels=np.arange(1, 36))
plt.title('大乐透前区号码分布热力图 (按星期分组)', fontsize=14, pad=20)  # 增加标题与图的间距
plt.xlabel('前区号码 (1-35)', fontsize=12, labelpad=10)  # 增加标签与图的间距
plt.ylabel('开奖日期', fontsize=12, labelpad=15)

# 后区热力图 (蓝色系)
ax2 = plt.subplot(2, 1, 2)
sns.heatmap(back_matrix,
            cmap='Blues',
            annot=False,
            linewidths=0.5,
            yticklabels=['周一', '周三', '周六'],
            xticklabels=np.arange(1, 13))
plt.title('大乐透后区号码分布热力图 (按星期分组)', fontsize=14, pad=20)  # 增加标题与图的间距
plt.xlabel('后区号码 (1-12)', fontsize=12, labelpad=10)  # 增加标签与图的间距
plt.ylabel('开奖日期', fontsize=12, labelpad=15)

# 优化布局
plt.subplots_adjust(hspace=0.4)  # 增加子图之间的垂直间距

# 调整x轴标签位置和大小，避免重叠
for ax in [ax1, ax2]:
    ax.tick_params(axis='x', which='major', labelsize=9, pad=5)
    ax.tick_params(axis='y', which='major', labelsize=11, pad=5)

plt.tight_layout(pad=3.0)  # 增加整体边距
plt.savefig('dlt_heatmap_comparison.png', dpi=300, bbox_inches='tight')
plt.show()