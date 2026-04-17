# Paper2ARM Hackathon 提交流程指南

> 版本: v1.0 | 最后更新: 2026-04-16

本文档详细介绍如何将您的论文复现成果提交到 Playground 平台和 DeployMaster 自动构建系统。

---

## 📋 提交前准备

### 1. 确认 ARM 包完整性

在提交之前，请确保您的 ARM 包符合以下要求：

- [ ] 包含完整的 9 个一级目录（paper, plan, code, trace, dataset, result, report, information, others）
- [ ] 代码可直接运行，无语法错误
- [ ] 包含 Dockerfile 和 requirements.txt
- [ ] 包含复现结果与论文的对比分析
- [ ] 包含 Agent 执行日志（trace）

详细检查清单请参考：[submission_checklist.md](./submission_checklist.md)

---

## 步骤 1：准备 ARM 包

### 1.1 组织 ARM 目录结构

使用 `file2arm-organization` skill 自动整理文件：

```bash
# 确保您在工作空间根目录
cd /path/to/your/workspace

# 使用 skill 整理文件
# 这将创建 ARM/ 目录并将文件分类到相应子目录
```

预期结构：
```
ARM/
├── paper/         # 论文 PDF 和元数据
├── plan/          # 复现计划
├── code/          # 源代码
├── trace/         # Agent 执行日志
├── dataset/       # 数据集
├── result/        # 结果与图表
├── report/        # Notebook + Dockerfile + requirements.txt
├── information/   # 经验笔记
└── others/        # 其他文件
```

### 1.2 生成 ARM 文档

使用 `arm-markdown` skill 生成复现指导手册：

```bash
# 生成 ARM_Reproduction_Guide.md
# 该文档包含完整的复现步骤和说明
```

### 1.3 生成 Dockerfile

使用 `arm-dockerfile` skill 生成 Dockerfile：

```bash
# 生成 Dockerfile
# 确保使用 Bohrium 平台兼容的配置
```

Dockerfile 必须包含：
- 基础镜像：`registry.dp.tech/dptech/ubuntu:20.04-py3.10`
- SSH 三件套：`openssh-server`, `supervisor`, `net-tools`
- 国内镜像源（阿里云 apt, 清华 pip）
- 所有必需的 Python 依赖

### 1.4 打包 ARM

```bash
# 将 ARM 文件夹打包为 ZIP
cd /path/to/your/workspace
zip -r arm_submission.zip ARM/

# 验证 ZIP 内容
unzip -l arm_submission.zip | head -30
```

---

## 步骤 2：提交到 Playground 平台

### 2.1 访问 Playground

打开浏览器访问：
```
http://audp1430906.bohrium.tech:50002
```

### 2.2 导航到提交页面

1. 点击顶部导航栏的 **"Hackathon"**
2. 选择 **"Submit Attempt"** 或 **"提交复现"**

### 2.3 填写提交信息

**必需信息：**

| 字段 | 说明 | 示例 |
|------|------|------|
| 论文标题 | 完整论文标题 | "Deep Learning for Molecular Property Prediction" |
| 论文 ID | Bohrium 论文库 ID | 通过 bohrium-paper-search 获取 |
| 复现级别 | R0 / R1 / R2 | R1 |
| 描述 | 复现成果简介 | "成功复现了主要实验结果..." |

**获取论文 ID：**

```bash
# 使用 bohrium-paper-search skill 搜索论文
python ~/.openclaw/skills/bohrium-paper-search/search_paper.py \
  --query "论文标题" \
  --access-key YOUR_ACCESS_KEY
```

### 2.4 上传 ARM 包

1. 点击 **"选择文件"** 或拖放区域
2. 选择您打包的 `arm_submission.zip`
3. 等待文件上传完成
4. 点击 **"提交"** 或 **"Submit"**

### 2.5 确认提交

提交成功后，您将看到：
- 提交确认页面
- 提交 ID（用于后续查询）
- 预计审核时间

---

## 步骤 3：（可选）触发 DeployMaster 构建

DeployMaster 是一个自动构建系统，可以从 GitHub 仓库自动构建 Docker 镜像。

### 3.1 准备 GitHub 仓库

确保您的代码已推送到 GitHub：

```bash
# 初始化仓库（如尚未初始化）
git init
git add .
git commit -m "Initial commit for Paper2ARM Hackathon"

# 推送到 GitHub
git remote add origin https://github.com/username/repo-name.git
git push -u origin main
```

仓库结构要求：
```
repo/
├── ARM/                    # ARM 文件夹
│   └── report/
│       └── Dockerfile      # 必须位于此路径
├── README.md
└── .gitignore
```

### 3.2 调用 DeployMaster API

**创建构建任务：**

```bash
# 使用 curl 提交构建请求
curl -X POST http://47.238.112.245:50001/api/v1/build \
  -H "Content-Type: application/json" \
  -d '{
    "github_url": "https://github.com/username/repo-name"
  }'
```

**预期响应：**
```json
{
  "task_id": "730abe14-18e9-4ff0-9170-56f34927eeed",
  "github_url": "https://github.com/username/repo-name",
  "status": "pending",
  "message": "Build task created successfully"
}
```

### 3.3 查询构建状态

```bash
# 使用返回的 task_id 查询状态
curl http://47.238.112.245:50001/api/v1/build/730abe14-18e9-4ff0-9170-56f34927eeed
```

**状态说明：**

| 状态 | 说明 |
|------|------|
| pending | 等待构建 |
| building | 正在构建 |
| success | 构建成功 |
| failed | 构建失败 |
| push_failed | 构建成功但推送镜像失败 |

**成功响应示例：**
```json
{
  "id": 2,
  "task_id": "730abe14-18e9-4ff0-9170-56f34927eeed",
  "github_url": "https://github.com/username/repo-name",
  "repo_name": "username/repo-name",
  "status": "success",
  "progress": "Build and push completed!",
  "docker_image_uri": "registry.dp.tech/davinci/repo-name:20260416120000",
  "verify_commands": [
    "python -c \"import torch; print(torch.__version__)\"",
    "python main.py --help"
  ],
  "created_at": "2026-04-16T12:00:00Z",
  "completed_at": "2026-04-16T12:30:00Z"
}
```

### 3.4 查看构建统计

```bash
# 查看所有任务和系统状态
curl http://47.238.112.245:50001/api/v1/stats
```

### 3.5 重试失败的构建

```bash
# 如果构建失败，可以重试
curl -X POST http://47.238.112.245:50001/api/v1/build/730abe14-18e9-4ff0-9170-56f34927eeed/retry
```

---

## 审核标准和评分维度

### 4C 评分维度

| 维度 | 权重 | 说明 |
|------|------|------|
| **Completeness** (完整性) | 30% | 是否覆盖了论文要求的所有实验和结果 |
| **Correctness** (正确性) | 40% | 复现结果与论文报告的一致程度 |
| **Clarity** (清晰度) | 20% | 代码和文档的可读性、可维护性 |
| **Cost** (成本效率) | 10% | 资源使用的合理性、运行效率 |

### 复现级别定义

**R0 - 跑通代码**
- 代码能正常运行
- 输出格式正确
- 不验证数值准确性

**R1 - 复现论文结果**
- 主要实验结果与论文一致
- 关键指标误差在合理范围内（通常 < 5%）
- 图表 visually similar

**R2 - 深度复现**
- 完成 R1 所有要求
- 实现论文 Future Work 中的改进
- 或提出新的扩展实验

### 审核流程

1. **自动检查**：系统检查 ARM 结构完整性
2. **代码执行**：自动运行 notebook 验证可执行性
3. **结果对比**：自动对比复现结果与论文报告
4. **人工审核**：专家对关键结果进行审核
5. **评分发布**：发布 4C 维度评分

---

## 常见问题 (FAQ)

### Q1: 提交后多久能收到审核结果？

通常需要 1-3 个工作日。您可以使用提交 ID 在 Playground 平台查询审核状态。

### Q2: Dockerfile 构建失败怎么办？

常见原因和解决方法：

| 错误 | 原因 | 解决 |
|------|------|------|
| `apt-get install failed` | 网络问题或包名错误 | 检查包名，确保使用阿里云源 |
| `pip install failed` | 依赖冲突或版本不兼容 | 检查版本兼容性，使用清华源 |
| `COPY failed` | 使用了 COPY/ADD 指令 | Bohrium 不支持，移除这些指令 |
| `image too large` | 镜像超过 40GB | 精简依赖，移除不必要的包 |

### Q3: 如何更新已提交的 ARM？

1. 在 Playground 平台找到您的提交
2. 点击 **"Update"** 或 **"更新"**
3. 上传新的 ZIP 文件
4. 说明更新内容

### Q4: 没有 GitHub 仓库可以使用 DeployMaster 吗？

不可以。DeployMaster 需要从 GitHub 仓库读取 Dockerfile。如果您没有 GitHub 账号，可以：
1. 注册 GitHub 账号（免费）
2. 仅使用 Playground 平台提交（不触发自动构建）

### Q5: 复现结果与论文有偏差怎么办？

在提交时说明：
1. 偏差的具体数值
2. 可能的原因分析
3. 您认为偏差是否在可接受范围内

审核时会考虑合理的偏差范围。

### Q6: 如何获取 Bohrium 论文 ID？

```bash
# 使用 bohrium-paper-search skill
python ~/.openclaw/skills/bohrium-paper-search/search_paper.py \
  --query "论文标题关键词" \
  --access-key YOUR_ACCESS_KEY
```

或在 Bohrium 平台搜索论文，从 URL 中获取 ID。

### Q7: trace 文件是什么？如何获取？

trace 文件记录 Agent 执行复现过程的完整日志，是 EARS (Execution Audit and Replay System) 的一部分。

获取方式：
```bash
# 从 OpenClaw sessions 目录复制
cp /root/.openclaw/agents/main/sessions/*.jsonl ARM/trace/
```

### Q8: 可以提交多个论文的复现吗？

可以。每个论文的复现作为一个独立的 Attempt 提交。

---

## 相关资源

- [submission_checklist.md](./submission_checklist.md) - 提交检查清单
- [arm_template.md](./arm_template.md) - ARM 模板
- [dockerfile_template](./dockerfile_template) - Dockerfile 模板
- [example_submission.json](./example_submission.json) - 提交格式示例

---

## 技术支持

如遇到问题，可以通过以下方式获取帮助：

1. 查看 Playground 平台文档：http://audp1430906.bohrium.tech:50002/docs
2. 查看 DeployMaster API 文档：http://47.238.112.245:50001/docs
3. 在 Hackathon 讨论区发帖求助
4. 联系技术支持团队

---

**祝您提交顺利！**
