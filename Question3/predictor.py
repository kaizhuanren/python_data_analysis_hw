import pandas as pd
import numpy as np
from config import PROCESSED_DATA_PATH, OUTPUT_DIR
import matplotlib.pyplot as plt
import os

def predict_next_year_counts():
    df = pd.read_csv(PROCESSED_DATA_PATH)
    df['year'] = df['year'].astype(int)
    trend = df.groupby('year').size()
    x = np.array(trend.index)
    y = np.array(trend.values)
    if len(x) < 2:
        return
    coeffs = np.polyfit(x, y, 1)
    next_year = x[-1] + 1
    pred = int(np.polyval(coeffs, next_year))
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, marker='o', label='历史数据')
    plt.plot([next_year], [pred], 'ro', label='预测')
    plt.title('下一届论文数量预测')
    plt.xlabel('年份')
    plt.ylabel('论文数量')
    plt.legend()
    plt.savefig(os.path.join(OUTPUT_DIR, f'wordcloud_{next_year}.png'))

if __name__ == '__main__':
    predict_next_year_counts()