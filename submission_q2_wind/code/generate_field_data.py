"""
生成模拟的风机尾流数据（基于论文描述的双峰特征）
"""
import numpy as np

# 参数设置
n_x = 125  # 流向截面数
n_y = 26   # 展向点数

# 展向坐标
y = np.linspace(-1, 1, n_y)

# 流向坐标
x = np.linspace(0, 10, n_x)

# 初始化速度亏损场
field = np.zeros((n_x, n_y))

# 双高斯模型参数随流向位置的变化
for i, xi in enumerate(x):
    # 振幅随流向衰减
    a = 0.8 * np.exp(-xi / 3.5) + 0.05
    
    # 双峰位置随流向向外移动
    l = 0.15 + 0.25 * (1 - np.exp(-xi / 2))
    
    # 峰宽随流向增加
    sigma = 0.12 + 0.18 * (1 - np.exp(-xi / 3))
    
    # 计算双高斯分布
    dg = a * (np.exp(-(y - l)**2 / (2 * sigma**2)) + 
              np.exp(-(y + l)**2 / (2 * sigma**2)))
    
    field[i] = dg

# 添加一些噪声使数据更真实
np.random.seed(42)
noise = np.random.normal(0, 0.01, field.shape)
field = np.clip(field + noise, 0, None)

# 保存数据
np.savetxt('field.txt', field, fmt='%.6f')
print(f"Generated field data: {field.shape}")
print(f"  Min: {field.min():.4f}")
print(f"  Max: {field.max():.4f}")
print(f"  Mean: {field.mean():.4f}")
