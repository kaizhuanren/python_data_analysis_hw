import pandas as pd
import re
import ast

def clean_expert_data(input_path='expert_data.csv', output_path='cleaned_expert_data.csv'):


    df = pd.read_csv(input_path)

    # 提取彩龄
    df['彩龄(年)'] = df['彩龄'].str.extract(r'(\d+)').astype(int)

    # 提取文章数量
    df['文章数量(篇)'] = df['文章数量'].str.extract(r'(\d+)').astype(int)

    # 提取双色球专家等级
    def get_ssq_level(levels_str):
        try:
            levels_list = ast.literal_eval(levels_str)
            for level in levels_list:
                if '双色球' in level:
                    match = re.search(r'双色球(.*?)(专家)', level)
                    if match:
                        return match.group(1) if match.group(1) else '初级'
            return '无等级'
        except (ValueError, SyntaxError):
            return '无等级'
    df['双色球专家等级'] = df['彩种等级'].apply(get_ssq_level)

    # 提取双色球获奖次数
    def extract_prize_counts(record):
        if pd.isna(record) or record == 'N/A' or '双色球' not in record:
            return 0, 0, 0
        
        ssq_part_match = re.search(r'(双色球.*?)(?:大乐透|$)', record)
        ssq_part = ssq_part_match.group(1) if ssq_part_match else ''

        first_prize = re.search(r'一等奖(\d+)次', ssq_part)
        second_prize = re.search(r'二等奖(\d+)次', ssq_part)
        third_prize = re.search(r'三等奖(\d+)次', ssq_part)
        
        return (
            int(first_prize.group(1)) if first_prize else 0,
            int(second_prize.group(1)) if second_prize else 0,
            int(third_prize.group(1)) if third_prize else 0
        )

    prize_counts = df['大奖战绩'].apply(extract_prize_counts)
    df['双色球一等奖次数'] = [p[0] for p in prize_counts]
    df['双色球二等奖次数'] = [p[1] for p in prize_counts]
    df['双色球三等奖次数'] = [p[2] for p in prize_counts]

    # 计算总获奖次数
    df['双色球获奖总次数'] = df['双色球一等奖次数'] + df['双色球二等奖次数'] + df['双色球三等奖次数']

    # 保存需要的列
    cleaned_df = df[[
        '用户ID', '彩龄(年)', '文章数量(篇)', '双色球专家等级',
        '双色球一等奖次数', '双色球二等奖次数', '双色球三等奖次数', '双色球获奖总次数'
    ]]

    cleaned_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"清洗后的数据已保存至: {output_path}")

if __name__ == '__main__':
    clean_expert_data()
