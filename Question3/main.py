# main.py

import os
from config import DATA_DIR, OUTPUT_DIR
from scraper import scrape_all_conferences
from data_processor import process_data
from analyzer import run_analysis
from predictor import predict_next_year_counts

def main():
    """
    项目主流程
    """
    # if not os.path.exists(DATA_DIR):
    #     os.makedirs(DATA_DIR)
    # if not os.path.exists(OUTPUT_DIR):
    #     os.makedirs(OUTPUT_DIR)
    # print("=" * 50)
    # print("学术论文发表趋势分析项目启动")
    # print("=" * 50)
    # # 项目主流程入口
    # process_data()
    # print("\n--- 步骤 3: 开始数据分析与可视化 ---")
    # run_analysis()
    print("\n--- 步骤 4: 开始预测下一届论文数量 ---")
    predict_next_year_counts()
    print("\n" + "=" * 50)
    print("所有任务已完成！")
    print(f"请在 '{DATA_DIR}/' 目录下查看数据文件。")
    print(f"请在 '{OUTPUT_DIR}/' 目录下查看分析图表。")
    print("=" * 50)

if __name__ == "__main__":
    main()