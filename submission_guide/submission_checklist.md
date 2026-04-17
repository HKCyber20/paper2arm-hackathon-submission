# Paper2ARM Hackathon 提交检查清单

> 版本: v1.0 | 最后更新: 2026-04-16

本文档提供完整的 ARM (Agent-Ready Manuscript) 提交检查清单，确保您的复现成果符合 Playground 平台和 DeployMaster 自动构建系统的要求。

---

## 📋 提交前检查清单

### 1. ARM 目录结构完整性

确保您的 ARM 文件夹包含以下 9 个必需子目录：

```
ARM/
├── paper/         # 论文相关文件 (PDF, 元数据)
├── plan/          # 复现计划文档
├── code/          # 源代码文件 (.py, .sh, .r, .jl)
├── trace/         # Agent 执行日志 (EARS 记录)
├── dataset/       # 数据集文件
├── result/        # 结果与图表
├── report/        # Notebook + Dockerfile
├── information/   # 模型信息与经验总结
└── others/        # 其他文件
```

**检查项:**
- [ ] 所有 9 个一级目录已创建（即使为空）
- [ ] 目录名称全小写，与标准一致
- [ ] 无文件散落在 ARM/ 根目录下

---

### 2. 代码文件 (code/)

**必需文件:**
- [ ] 主运行脚本（如 `main.py`, `train.py`, `run.sh`）
- [ ] 数据预处理脚本（如有）
- [ ] 模型定义/训练脚本
- [ ] 评估/测试脚本
- [ ] 可视化脚本（生成图表）

**代码质量检查:**
- [ ] 代码可直接运行，无语法错误
- [ ] 包含清晰的注释说明
- [ ] 关键参数可配置（不硬编码路径）
- [ ] 入口脚本有使用说明（docstring 或 README）

---

### 3. 结果文件 (result/)

**必需内容:**
- [ ] 生成的图表（PNG/JPG/SVG 格式）
- [ ] 数值结果文件（CSV/JSON/TXT）
- [ ] 模型输出/预测结果
- [ ] 训练日志（如有）

**组织方式:**
```
result/
├── figures/              # 所有生成的图表
│   ├── figure1.png
│   └── figure2.png
├── intermediate_results/ # 中间结果
└── final_results/        # 最终结果
    ├── metrics.json
    └── predictions.csv
```

---

### 4. 论文对比分析

**必需文档:**
- [ ] 复现结果与论文对比表
- [ ] 偏差说明（如有）
- [ ] 无法复现部分的解释

**对比表模板:**

| 指标/图表 | 论文报告值 | 复现结果 | 偏差 | 说明 |
|-----------|-----------|----------|------|------|
| Accuracy | 95.2% | 94.8% | -0.4% | 在误差范围内 |
| Figure 1 | - | ✓ | - |  visually similar |

---

### 5. Dockerfile (report/Dockerfile)

**用于 DeployMaster 自动构建，必需包含:**

- [ ] 基础镜像（推荐 `registry.dp.tech/dptech/ubuntu:20.04-py3.10`）
- [ ] 系统依赖安装（apt-get）
- [ ] Python 依赖安装（pip）
- [ ] SSH 服务配置（Bohrium 平台要求）
- [ ] 工作目录设置
- [ ] 无 COPY/ADD 指令（Bohrium 限制）

**关键要求:**
- [ ] 使用国内镜像源（阿里云 apt, 清华 pip）
- [ ] 包含 SSH 三件套：`openssh-server`, `supervisor`, `net-tools`
- [ ] 镜像大小不超过 40GB
- [ ] 设置 `DEBIAN_FRONTEND=noninteractive`

---

### 6. requirements.txt

**必需包含:**
- [ ] 所有 Python 依赖包及版本号
- [ ] 与 Dockerfile 中的 pip 安装一致

**示例格式:**
```
torch==2.0.1
numpy==1.24.3
pandas==2.0.3
matplotlib==3.7.2
scikit-learn==1.3.0
```

---

### 7. traces/ 目录 (EARS 记录)

**Agent 执行记录:**
- [ ] 复现过程的完整 trace 日志
- [ ] 存储于 `ARM/trace/` 目录
- [ ] 文件格式：`.jsonl`

**获取方式:**
```bash
# 从 OpenClaw sessions 目录复制
cp /root/.openclaw/agents/main/sessions/*.jsonl ARM/trace/
```

---

### 8. README.md 说明

**必需内容:**
- [ ] 论文标题和基本信息
- [ ] 复现目标说明（R0/R1/R2）
- [ ] 快速开始指南
- [ ] 目录结构说明
- [ ] 依赖安装说明
- [ ] 运行命令示例
- [ ] 结果说明
- [ ] 已知问题和限制

---

### 9. ARM 核心文档

**report/ 目录必需文件:**
- [ ] `ARM_Reproduction_Guide.md` - 复现指导手册
- [ ] `ARM_Notebook.ipynb` - Jupyter Notebook（可选但推荐）
- [ ] `Dockerfile` - 镜像构建文件

**plan/ 目录必需文件:**
- [ ] `plan.md` - 复现计划文档

---

## 🔍 提交前最终检查

### 文件完整性验证
```bash
# 运行以下命令检查 ARM 结构
cd /path/to/your/workspace

# 检查 9 个必需目录
for dir in paper plan code trace dataset result report information others; do
    if [ -d "ARM/$dir" ]; then
        echo "✓ ARM/$dir exists"
    else
        echo "✗ ARM/$dir MISSING"
    fi
done

# 检查关键文件
ls -la ARM/report/Dockerfile
ls -la ARM/report/ARM_Reproduction_Guide.md
ls -la ARM/code/*.py 2>/dev/null || echo "No Python files in code/"
```

### 代码可运行性验证
```bash
# 测试代码是否能正常导入
cd ARM/code
python -c "import main" 2>&1 && echo "✓ Import successful" || echo "✗ Import failed"

# 检查依赖是否完整
pip install -r ../report/requirements.txt --dry-run 2>&1 | head -20
```

### Dockerfile 验证
```bash
# 语法检查
docker build --dry-run -f ARM/report/Dockerfile . 2>&1 | head -20
```

---

## 📤 提交方式

### 方式一：Playground 平台提交

1. 将 ARM 文件夹打包为 ZIP
   ```bash
   zip -r arm_submission.zip ARM/
   ```

2. 访问 Playground: http://audp1430906.bohrium.tech:50002

3. 导航至 Hackathon → Submit Attempt

4. 上传 ZIP 文件并填写信息：
   - 论文标题
   - 论文 ID（通过 Bohrium 论文搜索获取）
   - 复现级别（R0/R1/R2）
   - 描述说明

### 方式二：DeployMaster 自动构建（可选）

1. 确保代码已推送到 GitHub

2. 调用 DeployMaster API:
   ```bash
   curl -X POST http://47.238.112.245:50001/api/v1/build \
     -H "Content-Type: application/json" \
     -d '{"github_url": "https://github.com/username/repo"}'
   ```

3. 查询构建状态:
   ```bash
   curl http://47.238.112.245:50001/api/v1/build/{task_id}
   ```

---

## ⚠️ 常见错误与解决

| 问题 | 原因 | 解决 |
|------|------|------|
| 缺少必需目录 | ARM 结构不完整 | 使用 file2arm-organization skill 整理 |
| Dockerfile 构建失败 | 依赖缺失或语法错误 | 检查 apt/pip 包名和版本 |
| 代码无法运行 | 缺少依赖或路径错误 | 在干净环境测试运行 |
| 结果与论文不符 | 参数设置或数据问题 | 检查超参数和数据预处理 |
| 镜像过大 | 安装了不必要的包 | 精简依赖，使用 `--no-cache-dir` |

---

## 📚 相关文档

- [HOW_TO_SUBMIT.md](./HOW_TO_SUBMIT.md) - 完整提交流程指南
- [arm_template.md](./arm_template.md) - ARM 模板
- [dockerfile_template](./dockerfile_template) - Dockerfile 模板
- [example_submission.json](./example_submission.json) - 提交格式示例

---

**提示**: 提交前建议使用 `upload-arm` skill 进行预检查，确保所有必需文件齐全。
