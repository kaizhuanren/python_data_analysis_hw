import pandas as pd

df = pd.read_csv("hurun_baifu_list_2024_processed.csv")

#模糊词分类
keywords = {
    '汽车': ['汽车'],
    '钢铁': ['钢铁', '不锈钢'],
    '房地产':['地产'],
    '医疗健康': ['医', '健康', '生物', '药', '基因', '疫苗', '肿瘤', '保健品', '试剂'],
    '科技制造业':['机器人', '无人机', '监控', '卫星', '航天', '智能硬件', '电子产品', '通信设备', '通信部件'],
    'IT': ['社交', '网', '电子商务', '软件', '数据', '信息', '平台', '芯片', '通信', '电信', '人工智能', '电脑', '生活服务', '自动驾驶', '声学及多媒体产品', 'SaaS解决方案', '计算机', '操作系统', '游戏', '网游'],
    '金融': ['金融', '银行', '保险', '投资', '货币', '区块链', '商业'],
    '材料': ['材', '石英', '半导体', '合金', '电子', '光电'],
    '快消产品': ['服装','鞋', '化妆品','护肤', '用品', '玩具', '珠宝', '烟', '消费品', '日化', '母婴', '生活', '纺', '羊绒'],
    '化工':['化', '塑', '橡胶', '钛白粉', '涂料'],
    '新能源': ['新能源', '光伏', '锂电池', '风电', '水电', '太阳能', '充电'],
    '传统能源': ['能源', '煤炭', '石油', '天然气'],
    '矿产、金属、冶金': ['矿', '金属', '冶', '铝', '铜'],
    '建筑建材': ['建', '陶瓷', '玻璃', '水泥', '地板'],
    '农业':['农', '畜牧', '乳', '糖', '饲料'],
    '食品':['食', '饮料', '酒', '调味', '香料', '面粉'],
    '家居':['家居', '家具', '沙发', '床垫', '橱柜', '厨具'],
    '零售': ['零售', '电商', '杂货'],
    '交通': ['交通', '物流', '运输', '航运', '快递', '航空' , '供应链'],
    '传统制造业':['造', '备', '机', '工业','器', '油缸', '件', '电路', '车', '轮胎', '插座', '五金', '电池', '灯', 'LED', '缆', '包装', '印', '家电', '家用电器'],
    '文娱与教育':['动漫', '教育', '博', '文', '娱', '媒'],
    '服务业': ['餐饮','旅游', '酒店', '企业服务', '殡葬服务', '物业'],
    '环保':['环保', '污水', '环境', '垃圾'],
    '其他':['']
}

# 分类函数
def classify_1(industry):
    industry_name = industry.split('、')[0]
    for category, words in keywords.items():
        for word in words:
            if word in industry_name:
                return category
    return '其他'

# 插入新列到 [所在行业_中文] 列右侧
df.insert(
    loc=df.columns.get_loc('所在行业_中文') + 1,
    column='二级类别',
    value=df['所在行业_中文'].apply(classify_1)
)

#人工检查后修改部分类别
df.iat[102, 12] = '材料'
df.iat[339, 12] = '传统制造业'
df.iat[473, 12] = '服务业'
df.iat[880, 12] = '传统制造业'
df.iat[964, 12] = '传统制造业'
df.iat[967, 12] = '传统制造业'


#大类划分
industries = {
    '房地产与建筑':['房地产', '建筑建材'],
    '金融':['金融'],
    '医疗健康':['医疗健康'],
    '化工与材料':['化工', '材料'],
    '能源与矿产':['传统能源', '新能源', '矿产、金属、冶金'],
    '制造与工业':['传统制造业', '科技制造业', '钢铁'],
    'IT':['IT'],
    '消费与零售':['零售', '快消产品', '食品', '家居'],
    '汽车与交通':['汽车', '交通'],
    '文娱与教育':['文娱与教育'],
    '农业':['农业'],
    '服务业':['服务业'],
    '环保':['环保'],
    '其他':['其他']
}

def classify_2(industry_name):
    for category, words in industries.items():
        for word in words:
            if word in industry_name:
                return category
    return '其他'

df.insert(
    loc=df.columns.get_loc('二级类别') + 1,
    column='一级类别',
    value=df['二级类别'].apply(classify_2)
)


df.to_csv("hurun_baifu_list_2024_categorized.csv", index=False, encoding='utf_8_sig')