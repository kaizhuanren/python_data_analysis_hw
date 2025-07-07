import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv('weather_history_2022_to_2024_processed.csv')

# 计算风力分布
def calculate_wind_distribution(df):
    # 按月份和风力等级分组统计
    day_wind = df.groupby(['月份', '白天风力(级)']).size().reset_index(name='天数')
    night_wind = df.groupby(['月份', '夜间风力(级)']).size().reset_index(name='天数')

    # 计算三年同月的平均值
    day_wind['平均天数'] = day_wind['天数'] / 3
    night_wind['平均天数'] = night_wind['天数'] / 3

    # 保留一位小数
    day_wind['平均天数'] = day_wind['平均天数'].round(1)
    night_wind['平均天数'] = night_wind['平均天数'].round(1)

    return day_wind, night_wind


# 绘制风力柱状图
def plot_wind_bar(day_wind, night_wind):
    # 创建图表和子图
    fig, axes = plt.subplots(4, 3, figsize=(18, 15), sharey=True)
    fig.suptitle('2022-2024年月平均风力分布（白天与夜间对比）', fontsize=20, y=0.98)

    # 设置颜色映射
    wind_levels = sorted(df['白天风力(级)'].unique())
    colors = plt.cm.viridis(np.linspace(0, 1, len(wind_levels)))
    color_map = dict(zip(wind_levels, colors))

    # 按月份绘制
    for month in range(1, 13):
        # 确定子图位置
        row = (month - 1) // 3
        col = (month - 1) % 3
        ax = axes[row, col]

        # 获取当月数据
        day_data = day_wind[day_wind['月份'] == month]
        night_data = night_wind[night_wind['月份'] == month]

        # 确保所有风力等级都有数据
        for level in wind_levels:
            if level not in day_data['白天风力(级)'].values:
                day_data = pd.concat([day_data, pd.DataFrame({
                    '月份': [month],
                    '白天风力(级)': [level],
                    '平均天数': [0]
                })])
            if level not in night_data['夜间风力(级)'].values:
                night_data = pd.concat([night_data, pd.DataFrame({
                    '月份': [month],
                    '夜间风力(级)': [level],
                    '平均天数': [0]
                })])

        # 排序数据
        day_data = day_data.sort_values('白天风力(级)')
        night_data = night_data.sort_values('夜间风力(级)')

        # 设置柱状图位置
        bar_width = 0.35
        index = np.arange(len(wind_levels))

        # 绘制白天风力柱状图
        for i, level in enumerate(wind_levels):
            day_val = day_data[day_data['白天风力(级)'] == level]['平均天数'].values[0]
            ax.bar(i - bar_width / 2, day_val, bar_width,
                   color=color_map[level], alpha=0.8, label='白天' if i == 0 else "")

        # 绘制夜间风力柱状图
        for i, level in enumerate(wind_levels):
            night_val = night_data[night_data['夜间风力(级)'] == level]['平均天数'].values[0]
            ax.bar(i + bar_width / 2, night_val, bar_width,
                   color=color_map[level], alpha=0.8, hatch='//', label='夜间' if i == 0 else "")

        # 设置子图标题和标签
        ax.set_title(f'{month}月', fontsize=14, pad=10)
        ax.set_xticks(index)
        ax.set_xticklabels(wind_levels)
        ax.set_xlabel('风力等级', fontsize=12)
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        # 添加数据标签
        for i, level in enumerate(wind_levels):
            day_val = day_data[day_data['白天风力(级)'] == level]['平均天数'].values[0]
            night_val = night_data[night_data['夜间风力(级)'] == level]['平均天数'].values[0]

            if day_val > 0:
                ax.text(i - bar_width / 2, day_val + 0.3, f'{day_val:.1f}',
                        ha='center', fontsize=10)
            if night_val > 0:
                ax.text(i + bar_width / 2, night_val + 0.3, f'{night_val:.1f}',
                        ha='center', fontsize=10)

        # 只给左上角子图添加图例
        if month == 1:
            ax.legend(loc='upper left', fontsize=12, framealpha=0.9)

    # 设置公共Y轴标签
    fig.text(0.04, 0.5, '平均天数', va='center', rotation='vertical', fontsize=14)

    plt.tight_layout(rect=[0.04, 0, 1, 0.96])
    plt.savefig('风力分布柱状图.png', dpi=120, bbox_inches='tight')
    plt.show()


# 绘制风力饼图
def plot_wind_pie(day_wind, night_wind):
    # 创建图表和子图
    fig, axes = plt.subplots(4, 6, figsize=(22, 15))
    fig.suptitle('2022-2024年月平均风力分布比例（白天与夜间）', fontsize=20, y=0.98)

    # 设置颜色映射
    wind_levels = sorted(df['白天风力(级)'].unique())
    colors = plt.cm.viridis(np.linspace(0, 1, len(wind_levels)))
    color_map = dict(zip(wind_levels, colors))

    # 按月份绘制
    for month in range(1, 13):
        # 确定子图位置
        row = (month - 1) // 3
        col = ((month - 1) % 3) * 2
        ax_day = axes[row, col]
        ax_night = axes[row, col + 1]

        # 获取当月数据
        day_data = day_wind[day_wind['月份'] == month]
        night_data = night_wind[night_wind['月份'] == month]

        # 确保所有风力等级都有数据
        for level in wind_levels:
            if level not in day_data['白天风力(级)'].values:
                day_data = pd.concat([day_data, pd.DataFrame({
                    '月份': [month],
                    '白天风力(级)': [level],
                    '平均天数': [0]
                })])
            if level not in night_data['夜间风力(级)'].values:
                night_data = pd.concat([night_data, pd.DataFrame({
                    '月份': [month],
                    '夜间风力(级)': [level],
                    '平均天数': [0]
                })])

        # 排序数据
        day_data = day_data.sort_values('白天风力(级)')
        night_data = night_data.sort_values('夜间风力(级)')

        # 计算总天数用于百分比
        day_total = day_data['平均天数'].sum()
        night_total = night_data['平均天数'].sum()

        # 过滤掉天数为0的等级
        day_data = day_data[day_data['平均天数'] > 0]
        night_data = night_data[night_data['平均天数'] > 0]

        # 绘制白天风力饼图
        wedges_day, texts_day, autotexts_day = ax_day.pie(
            day_data['平均天数'],
            autopct=lambda p: f'{p:.1f}%' if p > 5 else '',
            startangle=90,
            colors=[color_map[l] for l in day_data['白天风力(级)']],
            wedgeprops=dict(width=0.5, edgecolor='w'),
            pctdistance=0.85
        )

        # 设置饼图标题
        ax_day.set_title(f'{month}月 - 白天', fontsize=14)

        # 绘制夜间风力饼图
        wedges_night, texts_night, autotexts_night = ax_night.pie(
            night_data['平均天数'],
            autopct=lambda p: f'{p:.1f}%' if p > 5 else '',
            startangle=90,
            colors=[color_map[l] for l in night_data['夜间风力(级)']],
            wedgeprops=dict(width=0.5, edgecolor='w', hatch='//'),
            pctdistance=0.85
        )
        ax_night.set_title(f'{month}月 - 夜间', fontsize=14)

        # 添加中心文本
        center_text_props = dict(ha='center', va='center', fontsize=10, fontweight='bold')
        ax_day.text(0, 0, f'总天数\n{day_total:.1f}', **center_text_props)
        ax_night.text(0, 0, f'总天数\n{night_total:.1f}', **center_text_props)

    # 创建图例
    legend_elements = [plt.Rectangle((0, 0), 1, 1, color=color_map[l], label=f'{l}级')
                       for l in wind_levels]
    fig.legend(handles=legend_elements, loc='lower center', ncol=len(wind_levels),
               fontsize=12, framealpha=0.9, title='风力等级', title_fontsize=13)

    plt.tight_layout(rect=[0, 0.05, 1, 0.96])
    plt.savefig('风力分布饼图.png', dpi=120, bbox_inches='tight')
    plt.show()

# 创建优化的颜色映射
def create_wind_color_map(wind_levels):
    # 创建从蓝到红的多色渐变
    colors = [
        '#1f77b4',  # 蓝色 (1-2级)
        '#2ca02c',  # 绿色 (3-4级)
        '#ff7f0e',  # 橙色 (5-6级)
        '#d62728',  # 红色 (7-8级)
        '#9467bd',  # 紫色 (9-10级)
        '#8c564b',  # 棕色 (11-12级)
        '#e377c2'   # 粉色 (>12级)
    ]
    return dict(zip(wind_levels, colors))

# 按季度绘制柱状图
def plot_wind_by_quarter(day_wind, night_wind, wind_levels):
    # 定义季度和月份分组
    quarters = {
        '第一季度 (1-3月)': [1, 2, 3],
        '第二季度 (4-6月)': [4, 5, 6],
        '第三季度 (7-9月)': [7, 8, 9],
        '第四季度 (10-12月)': [10, 11, 12]
    }

    # 创建颜色映射
    color_map = create_wind_color_map(wind_levels)

    # 为每个季度创建图表
    for quarter_name, months in quarters.items():
        plt.figure(figsize=(15, 8), dpi=100)
        plt.suptitle(f'2022-2024年{quarter_name}风力分布', fontsize=18, y=0.97)

        # 创建三个子图（每个月份一个）
        axes = [plt.subplot(1, 3, i + 1) for i in range(3)]

        for idx, month in enumerate(months):
            ax = axes[idx]

            # 获取当月数据
            day_data = day_wind[day_wind['月份'] == month]
            night_data = night_wind[night_wind['月份'] == month]

            # 确保所有风力等级都有数据
            for level in wind_levels:
                if level not in day_data['白天风力(级)'].values:
                    day_data = pd.concat([day_data, pd.DataFrame({
                        '月份': [month],
                        '白天风力(级)': [level],
                        '平均天数': [0]
                    })])
                if level not in night_data['夜间风力(级)'].values:
                    night_data = pd.concat([night_data, pd.DataFrame({
                        '月份': [month],
                        '夜间风力(级)': [level],
                        '平均天数': [0]
                    })])

            # 排序数据
            day_data = day_data.sort_values('白天风力(级)')
            night_data = night_data.sort_values('夜间风力(级)')

            # 设置柱状图位置
            bar_width = 0.35
            index = np.arange(len(wind_levels))

            # 绘制白天风力柱状图
            for i, level in enumerate(wind_levels):
                day_val = day_data[day_data['白天风力(级)'] == level]['平均天数'].values[0]
                ax.bar(i - bar_width / 2, day_val, bar_width,
                       color=color_map[level], alpha=0.85, label='白天' if i == 0 else "")

            # 绘制夜间风力柱状图
            for i, level in enumerate(wind_levels):
                night_val = night_data[night_data['夜间风力(级)'] == level]['平均天数'].values[0]
                ax.bar(i + bar_width / 2, night_val, bar_width,
                       color=color_map[level], alpha=0.85, hatch='//', label='夜间' if i == 0 else "")

            # 设置子图标题和标签
            ax.set_title(f'{month}月', fontsize=14, pad=10)
            ax.set_xticks(index)
            ax.set_xticklabels(wind_levels, rotation=45 if len(wind_levels) > 5 else 0)
            ax.set_xlabel('风力等级', fontsize=11)
            ax.set_ylabel('平均天数', fontsize=11)
            ax.grid(axis='y', linestyle='--', alpha=0.7)
            ax.set_ylim(0, max(day_data['平均天数'].max(), night_data['平均天数'].max()) * 1.2)

            # 添加数据标签
            for i, level in enumerate(wind_levels):
                day_val = day_data[day_data['白天风力(级)'] == level]['平均天数'].values[0]
                night_val = night_data[night_data['夜间风力(级)'] == level]['平均天数'].values[0]

                if day_val > 0:
                    ax.text(i - bar_width / 2, day_val + 0.5, f'{day_val:.1f}',
                            ha='center', fontsize=9, fontweight='bold')
                if night_val > 0:
                    ax.text(i + bar_width / 2, night_val + 0.5, f'{night_val:.1f}',
                            ha='center', fontsize=9, fontweight='bold')

            # 添加图例（仅第一个子图）
            if idx == 0:
                ax.legend(loc='upper left', fontsize=10, framealpha=0.9)

        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.savefig(f'风力分布_{quarter_name}.png', dpi=120, bbox_inches='tight')
        plt.show()

# 主流程
if __name__ == "__main__":

    # 获取所有风力等级
    wind_levels = sorted(set(df['白天风力(级)'].unique()) |set(df['夜间风力(级)'].unique()))
    # 计算风力分布
    day_wind, night_wind = calculate_wind_distribution(df)

    # 可视化结果
    plot_wind_by_quarter(day_wind, night_wind, wind_levels)
    plot_wind_bar(day_wind, night_wind)
    plot_wind_pie(day_wind, night_wind)