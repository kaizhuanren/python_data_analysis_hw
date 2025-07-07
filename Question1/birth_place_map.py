import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Map

# 读取数据
df = pd.read_csv('hurun_baifu_list_2024_processed.csv')

# 1. 过滤非中国和空值数据
df = df[df['出生地_中文'].notna()]  # 移除空值
df = df[df['出生地_中文'].str.startswith('中国')]  # 只保留中国出生地


# 2. 提取省份信息
def extract_province(birthplace):
    parts = birthplace.split('-')
    if len(parts) < 2:  # 只有"中国"没有省份
        return None
    province = parts[1]

    # 处理特殊行政区
    special_regions = {
        '香港': '香港特别行政区',
        '澳门': '澳门特别行政区',
        '台湾': '台湾省'
    }
    return special_regions.get(province, province)


df['省份'] = df['出生地_中文'].apply(extract_province)

# 3. 移除无效省份数据
df = df.dropna(subset=['省份'])

# 4. 统计各省富豪数量
province_counts = df['省份'].value_counts().reset_index()
province_counts.columns = ['省份', '富豪人数']

# 5. 标准化省份名称（确保与地图数据匹配）
province_mapping = {
    '北京': '北京市',
    '上海': '上海市',
    '天津': '天津市',
    '重庆': '重庆市',
    '内蒙古': '内蒙古自治区',
    '新疆': '新疆维吾尔自治区',
    '广西': '广西壮族自治区',
    '宁夏': '宁夏回族自治区',
    '西藏': '西藏自治区',
    '黑龙江': '黑龙江省',
    '吉林': '吉林省',
    '辽宁': '辽宁省',
    '河北': '河北省',
    '河南': '河南省',
    '山东': '山东省',
    '山西': '山西省',
    '陕西': '陕西省',
    '甘肃': '甘肃省',
    '青海': '青海省',
    '四川': '四川省',
    '云南': '云南省',
    '贵州': '贵州省',
    '湖北': '湖北省',
    '湖南': '湖南省',
    '安徽': '安徽省',
    '江西': '江西省',
    '江苏': '江苏省',
    '浙江': '浙江省',
    '福建': '福建省',
    '广东': '广东省',
    '海南': '海南省',
    '香港特别行政区': '香港特别行政区',
    '澳门特别行政区': '澳门特别行政区',
    '台湾省': '台湾省'
}

province_counts['省份'] = province_counts['省份'].map(province_mapping)
province_counts = province_counts.groupby('省份', as_index=False).sum()  # 合并相同省份

# 6. 准备地图数据
map_data = province_counts[['省份', '富豪人数']].values.tolist()

# 7. 创建地图热力图
c = (
    Map()
    .add("富豪人数",
         map_data,
         "china",
         is_map_symbol_show=False,
         label_opts=opts.LabelOpts(is_show=True))  # 显示省份名称
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="2024胡润富豪榜出生地分布",
            subtitle="数据来源：胡润百富榜",
            pos_left="center"
        ),
        visualmap_opts=opts.VisualMapOpts(
            max_=max(province_counts['富豪人数']),
            range_color=["#e0f3f8", "#4575b4"],  # 蓝-深蓝渐变
            is_piecewise=True,  # 显示分段
            pos_left="left",
            pos_bottom="bottom",
            pieces=[
                {"min": 100, "label": ">100人", "color": "#08306b"},
                {"min": 50, "max": 99, "label": "50-99人", "color": "#2171b5"},
                {"min": 20, "max": 49, "label": "20-49人", "color": "#6baed6"},
                {"min": 10, "max": 19, "label": "10-19人", "color": "#bdd7e7"},
                {"min": 1, "max": 9, "label": "1-9人", "color": "#eff3ff"},
                {"min": 0, "max": 0, "label": "0人", "color": "#f7fbff"}
            ]
        ),
        tooltip_opts=opts.TooltipOpts(
            formatter="{b}<br/>富豪人数: {c}人"
        ),
        legend_opts=opts.LegendOpts(is_show=False)
    )
    .set_series_opts(
        label_opts=opts.LabelOpts(
            font_size=10,
            formatter="{b}",
            position="inside",
            color="#333"
        )
    )
)

# 8. 保存为HTML文件
c.render("富豪出生地分布_2024.html")