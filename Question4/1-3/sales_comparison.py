import pandas as pd
import matplotlib.pyplot as plt

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号

# 读取数据
df = pd.read_csv("dlt_data_last100.csv")

# 转换日期列
df['开奖日期'] = pd.to_datetime(df['开奖日期'])

# 提取星期几（0-6，周一为0，周三为2，周六为5）
df['星期'] = df['开奖日期'].dt.dayofweek

# 映射星期数字为中文名称
day_mapping = {0: '周一', 2: '周三', 5: '周六'}
df['开奖日'] = df['星期'].map(day_mapping)

# 1. 打印基本统计信息
print("=" * 50)
print("各开奖日销售额统计摘要:")
print("=" * 50)

# 按开奖日分组计算总销售额和平均销售额
sales_summary = df.groupby('开奖日')['销售额'].agg(['sum', 'mean', 'median', 'std'])
sales_summary = sales_summary.rename(columns={
    'sum': '总销售额(元)',
    'mean': '平均销售额(元)',
    'median': '中位销售额(元)',
    'std': '标准差(元)'
})
sales_summary['总销售额(亿元)'] = sales_summary['总销售额(元)'] / 1e8
sales_summary['平均销售额(千万元)'] = sales_summary['平均销售额(元)'] / 1e7
sales_summary['中位销售额(千万元)'] = sales_summary['中位销售额(元)'] / 1e7

# 格式化输出
formatted_summary = sales_summary.copy()
formatted_summary['总销售额(元)'] = formatted_summary['总销售额(元)'].apply(lambda x: f"{x:,.0f}")
formatted_summary['平均销售额(元)'] = formatted_summary['平均销售额(元)'].apply(lambda x: f"{x:,.0f}")
formatted_summary['中位销售额(元)'] = formatted_summary['中位销售额(元)'].apply(lambda x: f"{x:,.0f}")
formatted_summary['标准差(元)'] = formatted_summary['标准差(元)'].apply(lambda x: f"{x:,.0f}")
print(formatted_summary[['总销售额(元)', '平均销售额(元)', '中位销售额(元)', '标准差(元)']])

print("\n" + "=" * 50)
print("各开奖日销售额详细统计:")
print("=" * 50)

# 2. 打印详细统计信息
for day in ['周一', '周三', '周六']:
    day_data = df[df['开奖日'] == day]['销售额']
    day_count = len(day_data)
    total_sales = day_data.sum()
    mean_sales = day_data.mean()
    median_sales = day_data.median()
    min_sales = day_data.min()
    max_sales = day_data.max()
    std_sales = day_data.std()

    print(f"\n{day}开奖日统计 (共{day_count}期):")
    print(f"  总销售额: {total_sales:,.0f}元 ({total_sales / 1e8:.2f}亿元)")
    print(f"  平均销售额: {mean_sales:,.0f}元 ({mean_sales / 1e7:.2f}千万元)")
    print(f"  中位销售额: {median_sales:,.0f}元 ({median_sales / 1e7:.2f}千万元)")
    print(f"  最小销售额: {min_sales:,.0f}元")
    print(f"  最大销售额: {max_sales:,.0f}元")
    print(f"  标准差: {std_sales:,.0f}元")

# 3. 计算并打印对比信息
sat_mean = df[df['开奖日'] == '周六']['销售额'].mean()
mon_mean = df[df['开奖日'] == '周一']['销售额'].mean()
wed_mean = df[df['开奖日'] == '周三']['销售额'].mean()

print("\n" + "=" * 50)
print("开奖日销售额对比分析:")
print("=" * 50)
print(f"周六平均销售额是周一的: {sat_mean / mon_mean:.2f}倍")
print(f"周六平均销售额是周三的: {sat_mean / wed_mean:.2f}倍")
print(f"周三平均销售额是周一的: {wed_mean / mon_mean:.2f}倍")
print(f"周六销售额占总销售额比例: {sales_summary.loc['周六', '总销售额(元)'] / df['销售额'].sum():.2%}")

# 准备箱型图数据
mon_sales = df[df['开奖日'] == '周一']['销售额']
wed_sales = df[df['开奖日'] == '周三']['销售额']
sat_sales = df[df['开奖日'] == '周六']['销售额']

# 创建箱型图
plt.figure(figsize=(10, 6))

# 为每个箱型图设置不同颜色
colors = ['#66B2FF', '#98FB98', '#FFB6C1']  # 蓝色(周一), 浅绿色(周三), 粉色(周六)

# 绘制箱型图
box_plots = plt.boxplot([mon_sales, wed_sales, sat_sales],
                        labels=['周一', '周三', '周六'],
                        patch_artist=True,
                        medianprops={'color': 'red', 'linewidth': 2})

# 为每个箱型图设置不同颜色
for patch, color in zip(box_plots['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_edgecolor('black')  # 设置边框颜色
    patch.set_alpha(0.8)  # 设置透明度

# 设置须线和异常点的样式
plt.setp(box_plots['whiskers'], color='gray', linestyle='-', linewidth=1.5)
plt.setp(box_plots['caps'], color='gray', linewidth=1.5)
plt.setp(box_plots['fliers'], marker='o', markersize=6,
         markerfacecolor='gray', markeredgecolor='none', alpha=0.7)

# 添加标题和标签
plt.title('大乐透不同开奖日销售额分布对比', fontsize=15, pad=15)
plt.ylabel('销售额 (元)', fontsize=12)
plt.xlabel('开奖日', fontsize=12)

# 添加网格线
plt.grid(axis='y', linestyle='--', alpha=0.5)

# 添加图例说明颜色
from matplotlib.patches import Patch

legend_elements = [
    Patch(facecolor=colors[0], edgecolor='black', label='周一'),
    Patch(facecolor=colors[1], edgecolor='black', label='周三'),
    Patch(facecolor=colors[2], edgecolor='black', label='周六')
]
plt.legend(handles=legend_elements, title='开奖日', loc='upper right')

# 调整布局
plt.tight_layout()

# 保存高质量图片
plt.savefig('dlt_sales_comparison.png', dpi=300, bbox_inches='tight')
plt.show()