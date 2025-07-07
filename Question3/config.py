CONFERENCE_MAP = {
    'NeurIPS': 'nips',
    'CVPR': 'cvpr',
    'ICML': 'icml',
    'KDD': 'kdd',
    'AAAI': 'aaai'
}
START_YEAR = 2020
DATA_DIR = 'data'
OUTPUT_DIR = 'output'
RAW_DATA_PATH = f'{DATA_DIR}/raw_papers.csv'
PROCESSED_DATA_PATH = f'{DATA_DIR}/processed_papers.csv'
TREND_PLOT_PATH = f'{OUTPUT_DIR}/conference_trends.png'
WORDCLOUD_DIR = OUTPUT_DIR