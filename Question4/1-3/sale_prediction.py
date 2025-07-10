import pandas as pd
import matplotlib.pyplot as plt
from pmdarima import auto_arima
from statsmodels.tsa.statespace.sarimax import SARIMAX
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体为SimHei
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题

# 读取数据并预处理
df = pd.read_csv('dlt_data_last100.csv', parse_dates=['开奖日期'])
df.sort_values('开奖日期', inplace=True)
df = df.set_index('开奖日期')
sales = df['销售额'].values

# 使用auto_arima自动寻找最佳ARIMA参数
model = auto_arima(
    sales,
    seasonal=True,
    m=3,
    stepwise=True,
    trace=False,  # 关闭搜索过程输出
    suppress_warnings=True,
    error_action='ignore'
)

# 使用最佳参数拟合完整模型
best_order = model.order
best_seasonal_order = model.seasonal_order
final_model = SARIMAX(
    sales,
    order=best_order,
    seasonal_order=best_seasonal_order
)
results = final_model.fit(disp=False)

# 预测下一期销售额
forecast = results.get_forecast(steps=1)
predicted_value = forecast.predicted_mean[0]
conf_int = forecast.conf_int()[0]

# 输出训练参数和预测结果
print(f'训练完成参数:')
print(f'ARIMA阶数: {best_order}')
print(f'季节性阶数: {best_seasonal_order}')
print(f'\n预测结果:')
print(f'下一期(7月2日)预测销售额: {predicted_value:,.2f}元')
print(f'95%置信区间: [{conf_int[0]:,.2f}, {conf_int[1]:,.2f}]')

# 可视化结果 - 优化后的美观图表
plt.figure(figsize=(12, 7), dpi=100, facecolor='#f5f5f5')  # 设置浅灰背景
ax = plt.gca()
ax.set_facecolor('#fafafa')  # 设置坐标区背景色

# 绘制历史数据
dates = df.index
plt.plot(dates, sales, 'o-', color='#1f77b4', linewidth=2.5,
         markersize=6, markerfacecolor='white', markeredgewidth=1.5,
         label='历史销售额')

# 绘制预测点
next_date = pd.Timestamp('2025-07-02')
plt.plot(next_date, predicted_value, 'D', color='#d62728',
         markersize=10, label='预测值')

# 绘制置信区间（使用误差线）
plt.errorbar(next_date, predicted_value,
             yerr=[[predicted_value - conf_int[0]],
             [conf_int[1] - predicted_value]],
             fmt='none', ecolor='#d62728', elinewidth=3,
             capsize=8, capthick=2, alpha=0.8)

# 添加标签和标题
plt.title('大乐透销售额趋势分析与预测', fontsize=16, pad=20,
          fontweight='bold', color='#2c3e50')
plt.xlabel('开奖日期', fontsize=12, labelpad=10)
plt.ylabel('销售额 (元)', fontsize=12, labelpad=10)

# 格式化坐标轴
plt.gca().yaxis.set_major_formatter('{x:,.0f}')
plt.xticks(rotation=25, fontsize=10)
plt.yticks(fontsize=10)

# 网格和边框美化
ax.grid(True, linestyle='--', linewidth=0.7, alpha=0.7, color='#cccccc')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#cccccc')
ax.spines['bottom'].set_color('#cccccc')

# 添加数据标签
last_value = sales[-1]
plt.annotate(f'{last_value:,.0f}',
             xy=(dates[-1], last_value),
             xytext=(dates[-1] + pd.Timedelta(days=2), last_value),
             fontsize=9)

# 添加图例和说明文本
plt.legend(loc='upper left', frameon=True, facecolor='white')
plt.figtext(0.5, 0.01, f'基于ARIMA{best_order}模型预测 | 置信区间95%',
            ha='center', fontsize=9, color='#7f7f7f')

plt.tight_layout()
plt.subplots_adjust(bottom=0.15)
plt.savefig('销售额预测_优化版.png', dpi=120, bbox_inches='tight')
plt.show()