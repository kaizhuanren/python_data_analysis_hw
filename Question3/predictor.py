import pandas as pd
import numpy as np
from scipy.stats import linregress
from config import PROCESSED_DATA_PATH, OUTPUT_DIR
import matplotlib.pyplot as plt
import os
import matplotlib


matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']  
matplotlib.rcParams['axes.unicode_minus'] = False

def predict_conference_counts():
    try:
        df = pd.read_csv(PROCESSED_DATA_PATH)
    except FileNotFoundError:
        print(f"Error: The file at {PROCESSED_DATA_PATH} was not found.")
        return

    if 'year' not in df.columns or 'conference' not in df.columns:
        print("Error: The CSV must contain 'year' and 'conference' columns.")
        return

    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    df.dropna(subset=['year'], inplace=True)
    df['year'] = df['year'].astype(int)

    conferences = df['conference'].unique()

    for conference in conferences:
        conference_df = df[df['conference'] == conference]
        trend = conference_df.groupby('year').size()
        if len(trend) < 3:
            continue
        x = np.array(trend.index)
        y = np.array(trend.values)
        slope, intercept, r_value, p_value, std_err = linregress(x, y)
        r_squared = r_value**2
        next_year = x[-1] + 1
        linear_pred = int(slope * next_year + intercept)
        poly_coeffs = np.polyfit(x, y, 2)
        poly_pred = int(np.polyval(poly_coeffs, next_year))
        print(f'会议: {conference}')
        print(f'历史年份: {x}')
        print(f'历史论文数: {y}')
        print(f'线性回归: slope={slope:.3f}, intercept={intercept:.3f}, R²={r_squared:.3f}, p-value={p_value:.3f}')
        print(f'线性预测({next_year}): {linear_pred}')
        print(f'多项式预测({next_year}): {poly_pred}')
        print('-'*40)
        plt.figure(figsize=(12, 7))
        plt.plot(x, y, 'o-', label='历史数据')
        plt.plot([x[-1], next_year], [y[-1], linear_pred], 'r--', label='线性预测趋势')
        plt.plot(next_year, linear_pred, 'ro', label=f'线性预测: {linear_pred}')
        plt.plot([x[-1], next_year], [y[-1], poly_pred], 'g--', label='多项式预测趋势')
        plt.plot(next_year, poly_pred, 'gs', label=f'多项式预测: {poly_pred}')
        plt.title(f'会议 "{conference}" 论文数量预测\n线性回归 R²: {r_squared:.3f}, p-value: {p_value:.3f}')
        plt.xlabel('年份')
        plt.ylabel('论文数量')
        plt.legend()
        plt.grid(True)
        output_filename = os.path.join(OUTPUT_DIR, f'prediction_{conference.replace(" ", "_")}_{next_year}.png')
        plt.savefig(output_filename)
        plt.close()

if __name__ == '__main__':
    predict_conference_counts()