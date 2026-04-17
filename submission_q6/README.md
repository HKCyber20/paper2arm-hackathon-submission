# Paper2ARM Hackathon Submission - Q6: 硬币的另一面

## 论文信息
- **标题**: Anion optimization for bifunctional surface passivation in perovskite solar cells
- **期刊**: Nature Materials 22, 1507-1514 (2023)
- **DOI**: 10.1038/s41563-023-01705-y
- **通讯作者**: Edward H. Sargent

## 复现内容
使用机器学习筛选拟卤素阴离子，预测与钙钛矿表面的结合能。

## 目录结构
```
submission_q6/
├── paper/              # 论文元数据
├── plan/               # 复现计划
├── code/               # 源代码
│   ├── main.py         # 主程序
│   └── generate_full_dataset.py
├── dataset/            # 数据集
├── result/             # 结果与图表
├── report/             # Dockerfile + requirements.txt
├── trace/              # Agent执行日志
├── information/        # 经验笔记
└── README.md           # 本文件
```

## 快速开始

### 本地运行
```bash
cd code
python main.py
```

### Docker构建
```bash
cd report
docker build -t q6-anion .
docker run q6-anion
```

### Bohrium提交
```bash
lbg job submit \
  -c "python /workspace/code/main.py" \
  -im registry.dp.tech/dptech/ubuntu:20.04-py3.10 \
  -sc c2_m4_cpu \
  -pjid <project_id>
```

## 验证结果
- Round 1 (17特征): RF AUC = 0.9871 ✅
- Round 2 (4特征): RF AUC = 0.9887 ✅
- Top 4特征识别正确 ✅

## 复现级别
R1 - 成功复现论文主要结果

## 提交信息
- **提交日期**: 2026-04-16
- **提交者**: BohrClaw Agent
- **状态**: PASS
