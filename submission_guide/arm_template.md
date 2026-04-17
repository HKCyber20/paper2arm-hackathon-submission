# ARM (Agent-Ready Manuscript) 模板

> 版本: v1.0 | Paper2ARM Hackathon 标准格式

本文档提供 ARM 的标准模板，用于组织论文复现成果，确保其他 Agent 能够理解和复现您的结果。

---

## ARM 目录结构

```
ARM/
├── paper/              # 论文相关文件
│   ├── paper.pdf       # 原始论文 PDF
│   ├── metadata.json   # 论文元数据
│   └── parsed/         # 解析后的文本
│
├── plan/               # 复现计划
│   └── plan.md         # 复现计划文档
│
├── code/               # 源代码
│   ├── preprocessing/  # 数据预处理
│   ├── model/          # 模型定义
│   ├── training/       # 训练脚本
│   ├── evaluation/     # 评估脚本
│   └── visualization/  # 可视化
│
├── trace/              # Agent 执行日志
│   └── *.jsonl         # EARS 记录文件
│
├── dataset/            # 数据集
│   ├── raw/            # 原始数据
│   └── processed/      # 处理后数据
│
├── result/             # 结果与图表
│   ├── figures/        # 生成的图表
│   ├── intermediate/   # 中间结果
│   └── final/          # 最终结果
│
├── report/             # 报告与配置
│   ├── ARM_Reproduction_Guide.md  # 复现指导手册
│   ├── ARM_Notebook.ipynb         # Jupyter Notebook
│   ├── Dockerfile                 # 镜像构建文件
│   └── requirements.txt           # Python 依赖
│
├── information/        # 经验与信息
│   └── human_experience.md        # 人类经验笔记
│
└── others/             # 其他文件
    └── ...
```

---

## 1. paper/ 目录模板

### metadata.json

```json
{
  "title": "论文标题",
  "authors": ["作者1", "作者2", "作者3"],
  "year": 2024,
  "venue": "会议/期刊名称",
  "doi": "10.xxxx/xxxxx",
  "arxiv": "arXiv:2401.xxxxx",
  "url": "https://...",
  "abstract": "论文摘要...",
  "keywords": ["keyword1", "keyword2"],
  "code_url": "https://github.com/...",
  "dataset_url": "https://..."
}
```

---

## 2. plan/ 目录模板

### plan.md

```markdown
# 复现计划

## 论文信息
- **标题**: [论文标题]
- **作者**: [作者列表]
- **发表**: [年份] - [会议/期刊]
- **链接**: [论文链接]

## 核心方法
[1-2句话概括论文的核心方法]

## 复现目标
- [ ] R0: 跑通代码
- [ ] R1: 复现论文主要结果
- [ ] R2: 深度扩展（如有）

## 任务分解

### 任务 1: 环境准备
- [ ] 安装依赖
- [ ] 下载数据集
- [ ] 配置运行环境

### 任务 2: 数据预处理
- [ ] 加载原始数据
- [ ] 数据清洗
- [ ] 特征工程

### 任务 3: 模型实现
- [ ] 实现模型架构
- [ ] 配置训练参数
- [ ] 训练模型

### 任务 4: 结果复现
- [ ] 生成图表
- [ ] 计算指标
- [ ] 对比论文结果

## 依赖清单
- Python 3.10+
- PyTorch 2.0+
- NumPy, Pandas, Matplotlib
- [其他依赖]

## 预期结果
[描述预期复现的图表和指标]

## 风险评估
- [风险1]: [描述和应对措施]
- [风险2]: [描述和应对措施]
```

---

## 3. code/ 目录模板

### main.py

```python
"""
主运行脚本

Usage:
    python main.py --config config.yaml
    python main.py --mode train
    python main.py --mode evaluate
"""

import argparse
import yaml
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_config(config_path):
    """加载配置文件"""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def main():
    parser = argparse.ArgumentParser(description='论文复现主脚本')
    parser.add_argument('--config', type=str, default='config.yaml',
                        help='配置文件路径')
    parser.add_argument('--mode', type=str, default='train',
                        choices=['train', 'evaluate', 'predict'],
                        help='运行模式')
    parser.add_argument('--data_dir', type=str, default='../dataset',
                        help='数据目录')
    parser.add_argument('--output_dir', type=str, default='../result',
                        help='输出目录')
    
    args = parser.parse_args()
    
    # 加载配置
    config = load_config(args.config)
    
    # 根据模式执行
    if args.mode == 'train':
        train(config, args)
    elif args.mode == 'evaluate':
        evaluate(config, args)
    elif args.mode == 'predict':
        predict(config, args)


def train(config, args):
    """训练流程"""
    logger.info("开始训练...")
    # 实现训练逻辑
    pass


def evaluate(config, args):
    """评估流程"""
    logger.info("开始评估...")
    # 实现评估逻辑
    pass


def predict(config, args):
    """预测流程"""
    logger.info("开始预测...")
    # 实现预测逻辑
    pass


if __name__ == '__main__':
    main()
```

### config.yaml

```yaml
# 模型配置
model:
  name: "ModelName"
  hidden_dim: 256
  num_layers: 4
  dropout: 0.1

# 训练配置
training:
  epochs: 100
  batch_size: 32
  learning_rate: 0.001
  optimizer: "Adam"
  scheduler: "cosine"

# 数据配置
data:
  train_path: "../dataset/train.csv"
  val_path: "../dataset/val.csv"
  test_path: "../dataset/test.csv"
  num_workers: 4

# 输出配置
output:
  checkpoint_dir: "../result/checkpoints"
  log_dir: "../result/logs"
  figure_dir: "../result/figures"
```

---

## 4. report/ 目录模板

### ARM_Reproduction_Guide.md

```markdown
# [论文标题] - 复现指导手册

> ARM-Markdown：Agent Ready Manuscript
> 生成日期: [日期]
> 复现级别: [R0/R1/R2]

## 1. 概述

### 研究问题
[描述论文要解决的核心问题]

### 核心方法
[描述论文提出的方法]

### 预期成果
[描述预期复现的图表和指标]

## 2. 环境配置

### 系统要求
- Ubuntu 20.04+
- Python 3.10+
- CUDA 11.8+ (如需要 GPU)

### 依赖安装
```bash
pip install -r requirements.txt
```

### Docker 构建
```bash
docker build -f Dockerfile -t reproduction:latest .
```

## 3. 数据集

### 数据来源
[描述数据来源和获取方式]

### 数据结构
| 列名 | 类型 | 说明 |
|------|------|------|
| ... | ... | ... |

### 数据预处理
```python
# 预处理代码示例
```

## 4. 复现步骤

### 步骤 1: 数据准备
**目标**: [本步骤目标]

```python
# 完整可运行的代码
```

**预期输出**: [描述预期输出]

### 步骤 2: 模型训练
**目标**: [本步骤目标]

```python
# 完整可运行的代码
```

**预期输出**: [描述预期输出]

### 步骤 3: 结果生成
**目标**: [本步骤目标]

```python
# 完整可运行的代码
```

**预期输出**: [描述预期输出]

## 5. 结果与分析

### 关键指标
| 指标 | 论文值 | 复现值 | 偏差 |
|------|--------|--------|------|
| ... | ... | ... | ... |

### 图表对比
| 图编号 | 论文图 | 复现图 | 对比说明 |
|--------|--------|--------|----------|
| Fig 1 | [描述] | [描述] | [对比] |

### 分析与结论
[对复现结果的分析]

## 6. 附录

### 完整代码
<details>
<summary>点击展开</summary>

```python
# 完整代码
```

</details>

### 参考资料
- [论文链接]
- [代码仓库]
- [数据集链接]
```

### requirements.txt

```
# 深度学习框架
torch==2.0.1
torchvision==0.15.2

# 科学计算
numpy==1.24.3
scipy==1.11.1

# 数据处理
pandas==2.0.3

# 可视化
matplotlib==3.7.2
seaborn==0.12.2

# 机器学习
scikit-learn==1.3.0

# 其他依赖
pyyaml==6.0.1
tqdm==4.65.0
```

---

## 5. result/ 目录模板

### 结果文件组织

```
result/
├── figures/
│   ├── figure1_loss_curve.png
│   ├── figure2_accuracy_comparison.png
│   └── figure3_confusion_matrix.png
├── intermediate/
│   ├── processed_data.csv
│   ├── model_checkpoints/
│   └── training_logs.txt
└── final/
    ├── metrics.json
    ├── predictions.csv
    └── summary_report.md
```

### metrics.json

```json
{
  "experiment_name": "paper_reproduction",
  "timestamp": "2026-04-16T10:00:00Z",
  "metrics": {
    "accuracy": 0.948,
    "precision": 0.951,
    "recall": 0.946,
    "f1_score": 0.948,
    "auc": 0.992
  },
  "comparison": {
    "paper_accuracy": 0.952,
    "difference": -0.004,
    "within_tolerance": true
  },
  "training_info": {
    "epochs": 100,
    "final_loss": 0.123,
    "training_time_minutes": 45
  }
}
```

---

## 6. information/ 目录模板

### human_experience.md

```markdown
# 复现经验笔记

## 关键实现细节

### 细节 1: [标题]
[描述论文中未明确说明但影响结果的实现细节]

### 细节 2: [标题]
[描述另一个关键细节]

## 常见问题与解决

### 问题 1: [问题描述]
**现象**: [具体现象]
**原因**: [原因分析]
**解决**: [解决方法]

### 问题 2: [问题描述]
**现象**: [具体现象]
**原因**: [原因分析]
**解决**: [解决方法]

## 与论文的差异说明

### 差异 1: [差异点]
**论文做法**: [描述]
**本复现做法**: [描述]
**原因**: [说明差异原因]

## 改进建议

- [建议1]
- [建议2]

## 参考资料

- [相关链接或文档]
```

---

## 7. README.md 模板

```markdown
# [论文标题] 复现项目

> Paper2ARM Hackathon 提交项目

## 项目简介

本仓库包含 [论文标题] 的复现代码和结果。

- **论文链接**: [链接]
- **复现级别**: [R0/R1/R2]
- **主要成果**: [简要描述]

## 目录结构

```
ARM/
├── paper/      # 论文相关文件
├── plan/       # 复现计划
├── code/       # 源代码
├── trace/      # Agent 执行日志
├── dataset/    # 数据集
├── result/     # 结果与图表
├── report/     # 报告与配置
├── information/# 经验与信息
└── others/     # 其他文件
```

## 快速开始

### 环境准备

```bash
# 安装依赖
pip install -r ARM/report/requirements.txt

# 或使用 Docker
docker build -f ARM/report/Dockerfile -t reproduction:latest .
docker run -it reproduction:latest
```

### 运行复现

```bash
cd ARM/code
python main.py --config config.yaml --mode train
```

## 结果展示

### 关键指标

| 指标 | 论文值 | 复现值 | 偏差 |
|------|--------|--------|------|
| ... | ... | ... | ... |

### 复现图表

见 `ARM/result/figures/` 目录。

## 许可证

[许可证信息]

## 引用

如果本复现对您有帮助，请引用：

```bibtex
@article{...}
```
```

---

## 附录：完整文件清单

### ARM/paper/
- `paper.pdf` - 原始论文
- `metadata.json` - 论文元数据

### ARM/plan/
- `plan.md` - 复现计划

### ARM/code/
- `main.py` - 主脚本
- `config.yaml` - 配置文件
- `model.py` - 模型定义
- `train.py` - 训练脚本
- `evaluate.py` - 评估脚本
- `utils.py` - 工具函数

### ARM/trace/
- `*.jsonl` - Agent 执行日志

### ARM/dataset/
- `data_description.md` - 数据说明
- `download_script.sh` - 数据下载脚本

### ARM/result/
- `figures/` - 生成的图表
- `metrics.json` - 指标结果
- `predictions.csv` - 预测结果

### ARM/report/
- `ARM_Reproduction_Guide.md` - 复现指导手册
- `ARM_Notebook.ipynb` - Jupyter Notebook
- `Dockerfile` - Docker 镜像配置
- `requirements.txt` - Python 依赖

### ARM/information/
- `human_experience.md` - 人类经验笔记

### ARM/others/
- [其他文件]
