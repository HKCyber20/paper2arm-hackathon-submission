"""
Paper2Arm Hackathon 第2题：陈大佬和雷哥的风电场保卫战
双高斯拟合风机尾流数据
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import json

# 加载数据
print("=" * 60)
print("第2题：风电场保卫战 - 双高斯拟合")
print("=" * 60)

field = np.loadtxt("field.txt")
print(f"\n数据加载成功: {field.shape}")
print(f"  - 流向截面数: {field.shape[0]} (x/D ∈ [0, 10])")
print(f"  - 展向点数: {field.shape[1]} (y/D ∈ [-1, 1])")

# 定义双高斯模型
def double_gaussian(y, a, l, sigma):
    """
    双高斯模型
    DG(y) = a * [exp(-(y-l)²/(2σ²)) + exp(-(y+l)²/(2σ²))]
    """
    return a * (np.exp(-(y - l)**2 / (2 * sigma**2)) + 
                np.exp(-(y + l)**2 / (2 * sigma**2)))

# 展向坐标
y = np.linspace(-1, 1, 26)

# ==================== Milestone 1: 数据可视化 ====================
print("\n" + "=" * 60)
print("Milestone 1: 数据加载与可视化")
print("=" * 60)

# 绘制热力图
fig, ax = plt.subplots(figsize=(10, 6))
im = ax.imshow(field, aspect='auto', cmap='RdYlBu_r', 
               extent=[-1, 1, 10, 0], vmin=0, vmax=field.max())
ax.set_xlabel('y/D (Spanwise)', fontsize=12)
ax.set_ylabel('x/D (Streamwise)', fontsize=12)
ax.set_title('Wind Turbine Wake Velocity Deficit Field', fontsize=14)
plt.colorbar(im, ax=ax, label='ΔU/U∞')
plt.tight_layout()
plt.savefig('heatmap.png', dpi=150, bbox_inches='tight')
print("✓ 生成热力图: heatmap.png")

# 选取3个截面绘制原始数据
x_positions = [0, 50, 100]  # 对应 x/D ≈ 0, 4, 8
x_labels = ['0', '4', '8']

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for i, (idx, label) in enumerate(zip(x_positions, x_labels)):
    axes[i].plot(y, field[idx], 'b-', linewidth=2, label='CFD Data')
    axes[i].set_xlabel('y/D', fontsize=11)
    axes[i].set_ylabel('ΔU/U∞', fontsize=11)
    axes[i].set_title(f'x/D = {label}', fontsize=12)
    axes[i].legend()
    axes[i].grid(True, alpha=0.3)
    axes[i].set_ylim([0, field.max() * 1.1])
plt.tight_layout()
plt.savefig('cross_sections_raw.png', dpi=150, bbox_inches='tight')
print("✓ 生成截面原始数据图: cross_sections_raw.png")

# ==================== Milestone 2: 双高斯拟合 ====================
print("\n" + "=" * 60)
print("Milestone 2: 双高斯拟合")
print("=" * 60)

# 存储拟合结果
fit_results = []
fit_field = np.zeros_like(field)

# 对每个截面进行拟合
print("\n开始逐截面拟合 (125个截面)...")
print("使用multi-start策略避免近转子区拟合失败")

for i in range(125):
    data_slice = field[i]
    
    # Multi-start策略：尝试多组初始值
    best_result = None
    best_residual = float('inf')
    
    # 定义多组初始猜测
    initial_guesses = [
        [0.3, 0.29, 0.2],
        [0.5, 0.3, 0.15],
        [0.2, 0.25, 0.25],
        [0.4, 0.35, 0.18],
        [0.6, 0.2, 0.3],
        [0.15, 0.4, 0.12],
        [0.35, 0.15, 0.22],
        [0.45, 0.32, 0.16],
    ]
    
    for p0 in initial_guesses:
        try:
            popt, _ = curve_fit(double_gaussian, y, data_slice,
                               p0=p0,
                               bounds=([0, 0, 0.01], [1, 1.5, 2]),
                               maxfev=5000)
            
            # 计算残差
            fitted = double_gaussian(y, *popt)
            residual = np.sum((data_slice - fitted)**2)
            
            if residual < best_residual:
                best_residual = residual
                best_result = popt
                
        except Exception as e:
            continue
    
    if best_result is None:
        # 如果所有尝试都失败，使用默认参数
        best_result = [0.3, 0.29, 0.2]
        print(f"  警告: 截面 {i} 拟合失败，使用默认参数")
    
    a, l, sigma = best_result
    fit_results.append({
        'x_index': i,
        'x_over_D': i * 10 / 124,  # x/D from 0 to 10
        'a': float(a),
        'l': float(l),
        'sigma': float(sigma)
    })
    
    # 生成拟合曲线
    fit_field[i] = double_gaussian(y, a, l, sigma)
    
    if (i + 1) % 25 == 0:
        print(f"  进度: {i+1}/125 截面完成")

print("✓ 所有截面拟合完成")

# 保存拟合结果
with open('fit_results.json', 'w') as f:
    json.dump(fit_results, f, indent=2)
print("✓ 保存拟合结果: fit_results.json")

# 计算全场R²
ss_res = np.sum((field - fit_field)**2)
ss_tot = np.sum((field - field.mean())**2)
r2_score = 1 - ss_res / ss_tot

print(f"\n{'='*60}")
print(f"全场 R² = {r2_score:.4f}")
print(f"{'='*60}")

# 验证标准
if r2_score >= 0.95:
    grade = "Excellent"
elif r2_score >= 0.925:
    grade = "Good"
elif r2_score >= 0.90:
    grade = "Pass"
else:
    grade = "Fail"

print(f"评级: {grade}")
print(f"参考实现: R² = 0.977")

# ==================== Milestone 3: 结果可视化 ====================
print("\n" + "=" * 60)
print("Milestone 3: 结果可视化")
print("=" * 60)

# 绘制拟合vs数据对比图（3个截面）
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for i, (idx, label) in enumerate(zip(x_positions, x_labels)):
    axes[i].plot(y, field[idx], 'b-', linewidth=2, label='CFD Data', marker='o', markersize=4)
    axes[i].plot(y, fit_field[idx], 'r--', linewidth=2, label='DG Fit')
    axes[i].set_xlabel('y/D', fontsize=11)
    axes[i].set_ylabel('ΔU/U∞', fontsize=11)
    axes[i].set_title(f'x/D = {label}', fontsize=12)
    axes[i].legend()
    axes[i].grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('fit_vs_data.png', dpi=150, bbox_inches='tight')
print("✓ 生成拟合对比图: fit_vs_data.png")

# 绘制参数随流向位置的变化趋势
x_over_D = [r['x_over_D'] for r in fit_results]
a_values = [r['a'] for r in fit_results]
l_values = [r['l'] for r in fit_results]
sigma_values = [r['sigma'] for r in fit_results]

fig, axes = plt.subplots(3, 1, figsize=(10, 10))

axes[0].plot(x_over_D, a_values, 'b-', linewidth=2)
axes[0].set_ylabel('a(x) - Amplitude', fontsize=11)
axes[0].set_title('Double Gaussian Parameters vs Streamwise Position', fontsize=13)
axes[0].grid(True, alpha=0.3)
axes[0].set_xlim([0, 10])

axes[1].plot(x_over_D, l_values, 'g-', linewidth=2)
axes[1].set_ylabel('l(x) - Mean Offset', fontsize=11)
axes[1].grid(True, alpha=0.3)
axes[1].set_xlim([0, 10])

axes[2].plot(x_over_D, sigma_values, 'r-', linewidth=2)
axes[2].set_xlabel('x/D (Streamwise)', fontsize=11)
axes[2].set_ylabel('σ(x) - Std Dev', fontsize=11)
axes[2].grid(True, alpha=0.3)
axes[2].set_xlim([0, 10])

plt.tight_layout()
plt.savefig('parameters_trend.png', dpi=150, bbox_inches='tight')
print("✓ 生成参数趋势图: parameters_trend.png")

# 绘制拟合重建的热力图
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
im1 = axes[0].imshow(field, aspect='auto', cmap='RdYlBu_r', 
                     extent=[-1, 1, 10, 0], vmin=0, vmax=field.max())
axes[0].set_title('Original CFD Data', fontsize=12)
axes[0].set_xlabel('y/D')
axes[0].set_ylabel('x/D')
plt.colorbar(im1, ax=axes[0])

im2 = axes[1].imshow(fit_field, aspect='auto', cmap='RdYlBu_r', 
                     extent=[-1, 1, 10, 0], vmin=0, vmax=field.max())
axes[1].set_title('DG Reconstruction', fontsize=12)
axes[1].set_xlabel('y/D')
axes[1].set_ylabel('x/D')
plt.colorbar(im2, ax=axes[1])

plt.tight_layout()
plt.savefig('reconstructed_field.png', dpi=150, bbox_inches='tight')
print("✓ 生成重建场对比图: reconstructed_field.png")

# ==================== Milestone 4: Agent Track ====================
print("\n" + "=" * 60)
print("Milestone 4: Agent Track")
print("=" * 60)

agent_track = """# Agent Track - 风电场保卫战

## 关键决策点记录

### 1. 数据理解
- 数据来源: field.txt (125×26矩阵)
- 行方向: 流向位置 x/D ∈ [0, 10], 125个截面
- 列方向: 展向位置 y/D ∈ [-1, 1], 26个点
- 数值含义: 归一化速度亏损 ΔU/U∞

### 2. 拟合策略
- 使用scipy.optimize.curve_fit进行非线性最小二乘拟合
- 采用multi-start策略: 尝试8组不同的初始猜测
- 选择残差最小的结果作为最终拟合参数
- 参数约束: a∈[0,1], l∈[0,1.5], σ∈[0.01,2]

### 3. 参数约束设置
- 振幅a: [0, 1] - 速度亏损不超过来流速度
- 均值偏移l: [0, 1.5] - 双峰位置在合理范围内
- 标准差σ: [0.01, 2] - 避免过窄或过宽的峰

### 4. 验证方法
- 计算全场R²评估拟合质量
- 目视检查拟合曲线与原始数据的吻合度
- 对比参数变化趋势的物理合理性

## 遇到的问题与解决

### 问题: 近转子区拟合困难
- 现象: x/D ≈ 0附近速度分布高度非高斯
- 解决: multi-start策略，尝试多组初始值

### 结果
- 全场R² = {:.4f}
- 评级: {}
- 参考值: 0.977
""".format(r2_score, grade)

with open('agent_track.md', 'w') as f:
    f.write(agent_track)
print("✓ 生成Agent Track记录: agent_track.md")

#