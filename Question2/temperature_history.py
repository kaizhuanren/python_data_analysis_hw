import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv('weather_history_2022_to_2024_processed.csv.csv')

# 计算月平均气温
def calculate_monthly_avg(df):
    # 按年月分组计算月平均值
    monthly_avg = df.groupby(['年份', '月份']).agg({
        '最高气温(℃)': 'mean',
        '最低气温(℃)': 'mean'
    }).reset_index()

    # 计算三年同月的平均值
    result = monthly_avg.groupby('月份').agg({
        '最高气温(℃)': 'mean',
        '最低气温(℃)': 'mean'
    }).reset_index()

    # 保留一位小数
    result['最高气温(℃)'] = result['最高气温(℃)'].round(1)
    result['最低气温(℃)'] = result['最低气温(℃)'].round(1)
    return result


# 可视化函数
def plot_temperature_trend(monthly_avg):
    plt.figure(figsize=(12, 7), dpi=100)

    # 创建更浓的季节背景色
    plt.axvspan(0.5, 3.5, color='skyblue', alpha=0.5) #冬季
    plt.axvspan(3.5, 6.5, color='lightgreen', alpha=0.4) #春季
    plt.axvspan(6.5, 9.5, color='gold', alpha=0.4)  # 夏季
    plt.axvspan(9.5, 12.5, color='sandybrown', alpha=0.5)  # 秋季

    # 添加季节标签
    seasons = [(2, '冬季'), (5, '春季'), (8, '夏季'), (11, '秋季')]
    for pos, name in seasons:
        plt.text(pos, monthly_avg['最低气温(℃)'].min() - 3, name,
                 ha='center', fontsize=11, color='darkblue', weight='bold')

    # 创建折线图（使用更粗的线条）
    plt.plot(
        monthly_avg['月份'],
        monthly_avg['最高气温(℃)'],
        'o-',
        color='crimson',
        linewidth=3,
        markersize=9,
        markerfacecolor='white',
        markeredgewidth=2,
        label='平均最高气温'
    )
    plt.plot(
        monthly_avg['月份'],
        monthly_avg['最低气温(℃)'],
        's--',
        color='navy',
        linewidth=2.5,
        markersize=8,
        markerfacecolor='white',
        markeredgewidth=2,
        label='平均最低气温'
    )

    # 添加数据标签（改进位置）
    for i, row in monthly_avg.iterrows():
        plt.text(
            row['月份'],
            row['最高气温(℃)'] + 0.8,
            f"{row['最高气温(℃)']}℃",
            ha='center',
            fontsize=10,
            weight='bold',
            color='crimson'
        )
        plt.text(
            row['月份'],
            row['最低气温(℃)'] - 1.2,
            f"{row['最低气温(℃)']}℃",
            ha='center',
            fontsize=10,
            weight='bold',
            color='navy'
        )

    # 设置图表元素
    plt.title('2022-2024年月平均气温变化趋势', fontsize=16, pad=15, weight='bold')
    plt.xlabel('月份', fontsize=13, labelpad=10)
    plt.ylabel('温度(℃)', fontsize=13, labelpad=10)
    plt.xticks(range(1, 13),
               ['1月', '2月', '3月', '4月', '5月', '6月',
                '7月', '8月', '9月', '10月', '11月', '12月'],
               fontsize=11)
    plt.xlim(0.5, 12.5)

    # 设置网格和刻度
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.gca().xaxis.set_major_locator(MultipleLocator(1))

    y_min = monthly_avg['最低气温(℃)'].min() - 5
    y_max = monthly_avg['最高气温(℃)'].max() + 5
    plt.ylim(y_min, y_max)

    # 添加图例
    plt.legend(
        loc='upper center',
        bbox_to_anchor=(0.5, -0.12),  # 位于图表下方
        ncol=2,
        frameon=True,
        fontsize=12,
        edgecolor='gray'
    )

    # 添加零度参考线
    plt.axhline(y=0, color='gray', linestyle='-', alpha=0.3)

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.15)
    plt.savefig('T2_2022-2024年月平均气温变化趋势折线图.png', bbox_inches='tight')
    plt.show()


# 主流程
if __name__ == "__main__":

    # 计算月平均值
    monthly_avg = calculate_monthly_avg(df)

    # 可视化结果
    plot_temperature_trend(monthly_avg)
