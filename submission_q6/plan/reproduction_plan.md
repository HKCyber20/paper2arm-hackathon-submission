# 复现计划：硬币的另一面

## 论文信息
- **标题**: Anion optimization for bifunctional surface passivation in perovskite solar cells
- **期刊**: Nature Materials 22, 1507-1514 (2023)
- **核心任务**: 使用机器学习筛选拟卤素阴离子，预测与钙钛矿表面的结合能

## 复现目标
复现论文中的机器学习分类流程：
1. Round 1: 使用17个特征训练5种分类器
2. Round 2: 使用Top 4特征重新训练
3. 验证Random Forest AUC ≥ 0.95 (17特征) 和 ≥ 0.85 (4特征)

## 数据
- 267个拟卤素阴离子
- 19个分子描述符特征
- 结合能标签（高Eb > 3eV vs 低Eb ≤ 3eV）

## 方法
- 工具: scikit-learn, xgboost
- 算法: Random Forest, Gradient Boosting, XGBoost, Logistic Regression, SVC
- 验证: 85/15分层划分，10折交叉验证

## 预期结果
- Round 1 RF AUC ≈ 0.96
- Round 2 RF AUC ≈ 0.87
- Top 4特征: num_O, TPSA, HBA, HOMO

## 复现级别
R1 - 复现论文主要结果
