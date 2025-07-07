import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False    # 正确显示负号

# 读取CSV文件
df = pd.read_csv('hurun_baifu_list_2024_categorized.csv')

# 处理"财富值变化"列
def convert_growth(value):
    if value != 'NEW':
        return float(value.strip('%'))  # 去除百分号并转为浮点数
    else:
        return None

# 创建转换后的增长率列
df['growth_numeric'] = df['财富值变化'].apply(convert_growth)

# 筛选增长率为NEW的数据
high_growth_df = df[df['财富值变化'] == 'NEW']

# 统计行业分布
industry_counts = high_growth_df['二级类别'].value_counts()

# 设置美观的配色方案
colors = plt.cm.viridis(np.linspace(0, 1, len(industry_counts)))

# 创建图表
plt.figure(figsize=(14, 8))
bars = plt.bar(industry_counts.index, industry_counts.values, color=colors)

# 添加数据标签
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height)}',
             ha='center', va='bottom', fontsize=10, fontweight='bold')

# 设置图表属性
plt.title('2024胡润百富榜：新增企业家行业分布',
          fontsize=16, pad=20, fontweight='bold')
plt.xlabel('行业类别', fontsize=12, labelpad=10)
plt.ylabel('上榜人数', fontsize=12, labelpad=10)
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# 添加副标题说明
plt.figtext(0.5, 0.9,
            f"数据说明：包含所有新上榜(NEW)的企业家，总计{len(high_growth_df)}人",
            ha="center", fontsize=10, style='italic')

# 优化布局
plt.tight_layout()
plt.subplots_adjust(bottom=0.15)  # 为副标题留出空间

# 保存并显示
plt.savefig('wealth_growth_new.png', dpi=300, bbox_inches='tight')
plt.show()

for i in [20, 50]:
    # 筛选增长率>i%的数据
    high_growth_df = df[(df['growth_numeric'] > i)]

    # 统计行业分布
    industry_counts = high_growth_df['二级类别'].value_counts()

    # 设置美观的配色方案
    colors = plt.cm.viridis(np.linspace(0, 1, len(industry_counts)))

    # 创建图表
    plt.figure(figsize=(14, 8))
    bars = plt.bar(industry_counts.index, industry_counts.values, color=colors)

    # 添加数据标签
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{int(height)}',
                 ha='center', va='bottom', fontsize=10, fontweight='bold')

    # 设置图表属性
    plt.title(f'2024胡润百富榜：高增长企业家行业分布(增长率>{i}%)',
              fontsize=16, pad=20, fontweight='bold')
    plt.xlabel('行业类别', fontsize=12, labelpad=10)
    plt.ylabel('上榜人数', fontsize=12, labelpad=10)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # 添加副标题说明
    plt.figtext(0.5, 0.9,
                f"数据说明：包含所有财富增长率超过{i}%的企业家，总计{len(high_growth_df)}人",
                ha="center", fontsize=10, style='italic')

    # 优化布局
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.15)  # 为副标题留出空间

    # 保存并显示
    plt.savefig(f'higherthan_{i}%.png', dpi=300, bbox_inches='tight')
    plt.show()