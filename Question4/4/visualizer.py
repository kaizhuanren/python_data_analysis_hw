import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager
import os

def visualize_expert_data(input_path='cleaned_expert_data.csv'):
    # 设置中文字体
    try:
        font_path = r'C:\Windows\Fonts\simhei.ttf'
        font_prop = font_manager.FontProperties(fname=font_path)
        plt.rcParams['font.sans-serif'] = [font_prop.get_name()]
        plt.rcParams['axes.unicode_minus'] = False
        print("中文字体设置成功。")
    except FileNotFoundError:
        print("警告：未找到'simhei.ttf'字体，图表中的中文可能无法正确显示。")
        print("请确保 C:\\Windows\\Fonts\\simhei.ttf 路径下有该字体文件，或修改为其他可用中文字体路径。")

    # 读取数据
    try:
        df = pd.read_csv(input_path)
    except FileNotFoundError:
        print(f"错误: 文件未找到 at '{input_path}'")
        print("请先运行 data_cleaner.py 来生成清洗后的数据文件。")
        return

    # 添加单位彩龄中奖率
    df['单位彩龄中奖率'] = df.apply(
        lambda row: row['双色球获奖总次数'] / row['彩龄(年)'] if row['彩龄(年)'] > 0 else 0,
        axis=1
    )

    # 彩龄分布图
    plt.figure(figsize=(10, 6))
    sns.histplot(df['彩龄(年)'], bins=10, kde=True)
    plt.title('专家彩龄分布')
    plt.xlabel('彩龄 (年)')
    plt.ylabel('专家数量')
    plt.grid(axis='y', alpha=0.75)
    plt.savefig('output/彩龄分布.png')
    plt.show()

    # 文章数量分布图
    plt.figure(figsize=(10, 6))
    sns.histplot(df['文章数量(篇)'], bins=20, kde=True)
    plt.title('专家发表文章数量分布')
    plt.xlabel('文章数量 (篇)')
    plt.ylabel('专家数量')
    plt.grid(axis='y', alpha=0.75)
    plt.savefig('output/文章数量分布.png')
    plt.show()

    # 等级分布图
    plt.figure(figsize=(10, 6))
    level_order = ['无等级', '初级', '中级', '高级', '特级', '天王级']
    sns.countplot(data=df, x='双色球专家等级', order=level_order)
    plt.title('双色球专家等级分布')
    plt.xlabel('专家等级')
    plt.ylabel('专家数量')
    plt.grid(axis='y', alpha=0.75)
    plt.savefig('output/双色球专家等级分布.png')
    plt.show()

    # 彩龄 vs 中奖总数
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='彩龄(年)', y='双色球获奖总次数', alpha=0.6)
    sns.regplot(data=df, x='彩龄(年)', y='双色球获奖总次数', scatter=False, color='red')
    plt.title('彩龄与双色球获奖总次数的关系')
    plt.xlabel('彩龄 (年)')
    plt.ylabel('双色球获奖总次数')
    plt.grid(True)
    plt.savefig('output/彩龄与获奖关系.png')
    plt.show()

    # 文章数量 vs 中奖总数
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='文章数量(篇)', y='双色球获奖总次数', alpha=0.6)
    sns.regplot(data=df, x='文章数量(篇)', y='双色球获奖总次数', scatter=False, color='red')
    plt.title('文章数量与双色球获奖总次数的关系')
    plt.xlabel('文章数量 (篇)')
    plt.ylabel('双色球获奖总次数')
    plt.grid(True)
    plt.savefig('output/文章数量与获奖关系.png')
    plt.show()

    # 等级 vs 中奖总数
    plt.figure(figsize=(12, 7))
    sns.boxplot(data=df, x='双色球专家等级', y='双色球获奖总次数', order=level_order)
    sns.stripplot(data=df, x='双色球专家等级', y='双色球获奖总次数', order=level_order, color=".25", alpha=0.6)
    plt.title('双色球专家等级与获奖总次数的关系')
    plt.xlabel('专家等级')
    plt.ylabel('双色球获奖总次数')
    plt.grid(axis='y', alpha=0.75)
    plt.savefig('output/专家等级与获奖关系.png')
    plt.show()

    # 新增：单位彩龄中奖率 vs 文章数量
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='文章数量(篇)', y='单位彩龄中奖率', alpha=0.6)
    sns.regplot(data=df, x='文章数量(篇)', y='单位彩龄中奖率', scatter=False, color='red')
    plt.title('文章数量与单位彩龄中奖率的关系')
    plt.xlabel('文章数量 (篇)')
    plt.ylabel('单位彩龄中奖率')
    plt.grid(True)
    plt.savefig('output/文章数量与单位彩龄中奖率关系.png')
    plt.show()

    # 新增：等级 vs 单位彩龄中奖率
    plt.figure(figsize=(12, 7))
    sns.boxplot(data=df, x='双色球专家等级', y='单位彩龄中奖率', order=level_order)
    sns.stripplot(data=df, x='双色球专家等级', y='单位彩龄中奖率', order=level_order, color=".25", alpha=0.6)
    plt.title('双色球专家等级与单位彩龄中奖率的关系')
    plt.xlabel('专家等级')
    plt.ylabel('单位彩龄中奖率')
    plt.grid(axis='y', alpha=0.75)
    plt.savefig('output/专家等级与单位彩龄中奖率关系.png')
    plt.show()


if __name__ == '__main__':
    if not os.path.exists('output'):
        os.makedirs('output')
    visualize_expert_data()
