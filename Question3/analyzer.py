import pandas as pd
import matplotlib.pyplot as plt
import ast
import os
from config import PROCESSED_DATA_PATH, OUTPUT_DIR
from wordcloud import WordCloud

def run_analysis():
    df = pd.read_csv(PROCESSED_DATA_PATH)
    df['keywords'] = df['keywords'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])
    df['year'] = df['year'].astype(int)
    trend = df.groupby('year').size()
    plt.figure(figsize=(10, 6))
    plt.plot(trend.index, trend.values, marker='o')
    plt.title('论文发表趋势')
    plt.xlabel('年份')
    plt.ylabel('论文数量')
    plt.savefig(os.path.join(OUTPUT_DIR, 'conference_trends.png'))
    for year in df['year'].unique():
        keywords = [kw for kws in df[df['year'] == year]['keywords'] for kw in kws]
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(keywords))
        wordcloud.to_file(os.path.join(OUTPUT_DIR, f'wordcloud_{year}.png'))

if __name__ == '__main__':
    run_analysis()