import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from pmdarima import auto_arima

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

historical = pd.read_csv("temperature_2020_to_2024_real.csv")
historical['date'] = pd.to_datetime(historical['日期'])
historical.set_index('date', inplace=True)

daily_2025 = pd.read_csv("temperature_2025_real.csv")
daily_2025['date'] = pd.to_datetime(daily_2025['日期'])
daily_2025.set_index('date', inplace=True)

# 准备训练数据 (2020-2024年月平均最高温度)
# 使用重采样计算月平均最高温度
train = historical['最高气温(℃)'].resample('MS').mean()

# 准备2025年1-6月真实月平均温度
# 同样使用重采样计算月平均
monthly_2025 = daily_2025['最高气温(℃)'].resample('MS').mean().loc['2025-01':'2025-06']

# 自动选择最佳SARIMA参数
model = auto_arima(
    train,
    seasonal=True,
    m=12,
    stepwise=True,
    suppress_warnings=True,
    error_action='ignore'
)
print(f"最优SARIMA参数: {model.order} 季节性参数: {model.seasonal_order}")

# 训练SARIMA模型
sarima_model = SARIMAX(
    train,
    order=model.order,
    seasonal_order=model.seasonal_order
).fit(disp=False)

# 预测2025年1-6月
forecast = sarima_model.get_forecast(steps=6)
forecast_mean = forecast.predicted_mean
conf_int = forecast.conf_int()

# 合并预测结果和真实值
results = pd.DataFrame({
    '预测值': forecast_mean,
    '真实值': monthly_2025.values,  # 直接使用数组值避免索引问题
    '预测下限': conf_int.iloc[:, 0],
    '预测上限': conf_int.iloc[:, 1]
}, index=monthly_2025.index)  # 使用2025年月索引

# 计算预测误差
mae = np.mean(np.abs(results['预测值'] - results['真实值']))
rmse = np.sqrt(np.mean((results['预测值'] - results['真实值'])**2))
print(f"预测误差指标 - MAE: {mae:.2f}℃, RMSE: {rmse:.2f}℃")

# 可视化结果
plt.figure(figsize=(12, 6))
plt.plot(results.index, results['真实值'], 'o-', label='真实值', color='#1f77b4')
plt.plot(results.index, results['预测值'], 's--', label='预测值', color='#ff7f0e')
plt.fill_between(
    results.index,
    results['预测下限'],
    results['预测上限'],
    color='orange',
    alpha=0.15,
    label='95%置信区间'
)

plt.title('2025年1-6月平均最高温度预测 vs 真实值', fontsize=14)
plt.xlabel('月份', fontsize=12)
plt.ylabel('温度(℃)', fontsize=12)
plt.legend()
plt.grid(linestyle='--', alpha=0.7)
plt.tight_layout()

# 保存图表
plt.savefig('气温预测对比.png', dpi=300)
plt.show()

# 输出预测结果
print("\n2025年1-6月预测结果:")
print(results[['预测值', '真实值']].round(1))