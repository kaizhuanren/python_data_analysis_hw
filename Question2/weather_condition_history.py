import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv('weather_history_2022_to_2024_processed.csv')

# 数据预处理
def preprocess_weather_data(df):

    # 简化天气类型（只取最后一个字）
    df['白天天气类型'] = df['白天天气'].apply(lambda x: re.sub(r'.*([晴阴云雨雪])$', r'\1', x))
    df['夜间天气类型'] = df['夜间天气'].apply(lambda x: re.sub(r'.*([晴阴云雨雪])$', r'\1', x))

    # 将"云"转换为"多云"
    df['白天天气类型'] = df['白天天气类型'].replace('云', '多云')
    df['夜间天气类型'] = df['夜间天气类型'].replace('云', '多云')

    return df


# 计算天气分布
def calculate_weather_distribution(df):
    # 按月份和天气类型分组统计
    day_weather = df.groupby(['月份', '白天天气类型']).size().reset_index(name='天数')
    night_weather = df.groupby(['月份', '夜间天气类型']).size().reset_index(name='天数')

    # 计算三年同月的平均值
    day_weather['平均天数'] = day_weather['天数'] / 3
    night_weather['平均天数'] = night_weather['天数'] / 3

    # 保留一位小数
    day_weather['平均天数'] = day_weather['平均天数'].round(1)
    night_weather['平均天数'] = night_weather['平均天数'].round(1)

    return day_weather, night_weather


# 创建优化的颜色映射
def create_weather_color_map():
    return {
        '晴': '#FFD700',  # 金色 - 晴天
        '阴': '#A9A9A9',  # 灰色 - 阴天
        '多云': '#87CEEB',  # 天蓝色 - 多云
        '雨': '#32CD32',  # 绿色 - 雨天
        '雪': '#ADD8E6'  # 浅蓝色 - 雪天
    }


# 按季度绘制天气分布图
def plot_weather_by_quarter(day_weather, night_weather):
    # 定义季度和月份分组
    quarters = {
        '第一季度 (1-3月)': [1, 2, 3],
        '第二季度 (4-6月)': [4, 5, 6],
        '第三季度 (7-9月)': [7, 8, 9],
        '第四季度 (10-12月)': [10, 11, 12]
    }

    # 创建颜色映射
    color_map = create_weather_color_map()
    weather_types = ['晴', '阴', '多云', '雨', '雪']

    # 为每个季度创建图表
    for quarter_name, months in quarters.items():
        plt.figure(figsize=(16, 10), dpi=100)
        plt.suptitle(f'2022-2024年{quarter_name}天气分布', fontsize=22, y=0.97)

        # 创建三个子图（每个月份一个）
        axes = [plt.subplot(1, 3, i + 1) for i in range(3)]

        for idx, month in enumerate(months):
            ax = axes[idx]

            # 获取当月数据
            day_data = day_weather[day_weather['月份'] == month]
            night_data = night_weather[night_weather['月份'] == month]

            # 确保所有天气类型都有数据
            for w_type in weather_types:
                if w_type not in day_data['白天天气类型'].values:
                    day_data = pd.concat([day_data, pd.DataFrame({
                        '月份': [month],
                        '白天天气类型': [w_type],
                        '平均天数': [0]
                    })])
                if w_type not in night_data['夜间天气类型'].values:
                    night_data = pd.concat([night_data, pd.DataFrame({
                        '月份': [month],
                        '夜间天气类型': [w_type],
                        '平均天数': [0]
                    })])

            # 排序数据（按固定顺序）
            day_data = day_data.sort_values('白天天气类型',
                                            key=lambda x: x.map({k: i for i, k in enumerate(weather_types)}))
            night_data = night_data.sort_values('夜间天气类型',
                                                key=lambda x: x.map({k: i for i, k in enumerate(weather_types)}))

            # 设置柱状图位置
            bar_width = 0.35
            index = np.arange(len(weather_types))

            # 绘制白天天气柱状图
            for i, w_type in enumerate(weather_types):
                day_val = day_data[day_data['白天天气类型'] == w_type]['平均天数'].values[0]
                ax.bar(i - bar_width / 2, day_val, bar_width,
                       color=color_map[w_type], alpha=0.9, edgecolor='black', linewidth=1,
                       label='白天' if i == 0 else "")

            # 绘制夜间天气柱状图
            for i, w_type in enumerate(weather_types):
                night_val = night_data[night_data['夜间天气类型'] == w_type]['平均天数'].values[0]
                ax.bar(i + bar_width / 2, night_val, bar_width,
                       color=color_map[w_type], alpha=0.9, hatch='//', edgecolor='black', linewidth=1,
                       label='夜间' if i == 0 else "")

            # 设置子图标题和标签
            ax.set_title(f'{month}月', fontsize=16, pad=12, fontweight='bold')
            ax.set_xticks(index)
            ax.set_xticklabels(weather_types, fontsize=12)
            if idx == 1: ax.set_xlabel('天气类型', fontsize=13, labelpad=10)
            if idx == 0: ax.set_ylabel('平均天数', fontsize=13, labelpad=10)
            ax.grid(axis='y', linestyle='--', alpha=0.7)
            ax.set_ylim(0, max(day_data['平均天数'].max(), night_data['平均天数'].max()) * 1.25)

            # 添加数据标签
            for i, w_type in enumerate(weather_types):
                day_val = day_data[day_data['白天天气类型'] == w_type]['平均天数'].values[0]
                night_val = night_data[night_data['夜间天气类型'] == w_type]['平均天数'].values[0]

                if day_val > 0:
                    ax.text(i - bar_width / 2, day_val + 0.5, f'{day_val:.1f}',
                            ha='center', fontsize=10, fontweight='bold')
                if night_val > 0:
                    ax.text(i + bar_width / 2, night_val + 0.5, f'{night_val:.1f}',
                            ha='center', fontsize=10, fontweight='bold')

            # 添加图例（仅第一个子图）
            if idx == 0:
                ax.legend(loc='upper left', fontsize=11, framealpha=0.9, title='时段', title_fontsize=12)

        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.savefig(f'天气分布_{quarter_name}.png', dpi=120, bbox_inches='tight')
        plt.show()


# 主流程
if __name__ == "__main__":
    # 预处理数据
    processed_df = preprocess_weather_data(df)

    # 计算天气分布
    day_weather, night_weather = calculate_weather_distribution(processed_df)

    # 可视化结果
    plot_weather_by_quarter(day_weather, night_weather)