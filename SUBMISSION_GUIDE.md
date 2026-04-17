# Paper2ARM Hackathon 提交指南

## 提交包信息

| 项目 | 详情 |
|------|------|
| **总包文件** | `all_submissions_arm.zip` (753 KB) |
| **单题包** | `submission_q6_arm.zip` (315 KB) |
| **题目数量** | 7题全部完成 |
| **Git仓库** | `/personal/openclaw/hackathon/.git` |

## 7道题目完成情况

| 题号 | 题目名称 | 领域 | 验证结果 | 状态 |
|------|----------|------|----------|------|
| Q1 | 木木张和豆角焖面的顿悟 | 分子动力学 (DeePMD) | RMSE=0.005 eV/atom | ✅ PASS |
| Q2 | 陈大佬和雷哥的风电场保卫战 | CFD/流体力学 | R²=0.9967 | ✅ PASS |
| Q3 | 欧神凌晨三点的抉择 | 离子束物理 (RustBCA) | R²(Si)=0.9997, R²(Ge)=0.9991 | ✅ PASS |
| Q4 | 胡汉三和王阿姨的储蓄之争 | 宏观经济学 (Huggett) | 8/8组参数通过 | ✅ PASS |
| Q5 | 组学戴乙己教授的反击 | 3D基因组学 (Hi-C) | CTCF比值2.37x | ✅ PASS |
| Q6 | 硬币的另一面 | 机器学习 (sklearn) | AUC=0.9887 | ✅ PASS |
| Q7 | 菜市场散伙后的"钉子户"调查 | 基因组学 (TSA-seq) | Pearson r=0.9434 | ✅ PASS |

## 提交方式

### 方式1：手动提交到Playground（推荐）

1. **访问平台**
   ```
   http://audp1430906.bohrium.tech:50002
   ```

2. **登录账号**
   - 使用Bohrium账号登录

3. **导航到提交页面**
   - 点击顶部导航栏 "Hackathon"
   - 点击 "Submit Attempt" 或 "提交复现"

4. **填写提交信息**

   示例（Q6）：
   ```
   论文标题: Anion optimization for bifunctional surface passivation in perovskite solar cells
   论文DOI: 10.1038/s41563-023-01705-y
   期刊: Nature Materials
   年份: 2023
   复现级别: R1
   描述: 成功复现ML分类流程。Round 1 RF AUC=0.9871(17特征)，Round 2 RF AUC=0.9887(4特征)。Top 4特征：num_O, TPSA, HBA, HOMO。
   ```

5. **上传ARM包**
   - 选择文件：`submission_q6_arm.zip` 或 `all_submissions_arm.zip`
   - 等待上传完成

6. **提交**
   - 点击 "提交" 按钮
   - 保存提交ID以便查询

### 方式2：DeployMaster自动构建

由于DeployMaster需要从GitHub仓库构建，您需要：

1. **创建GitHub仓库**
   ```bash
   # 在GitHub上创建新仓库
   # 例如: https://github.com/yourusername/paper2arm-hackathon
   ```

2. **推送代码**
   ```bash
   cd /personal/openclaw/hackathon
   git remote add origin https://github.com/yourusername/paper2arm-hackathon.git
   git branch -M main
   git push -u origin main
   ```

3. **调用DeployMaster API**
   ```bash
   curl -X POST http://47.238.112.245:50001/api/v1/build \
     -H "Content-Type: application/json" \
     -d '{"github_url": "https://github.com/yourusername/paper2arm-hackathon"}'
   ```

4. **查询构建状态**
   ```bash
   curl http://47.238.112.245:50001/api/v1/build/<task_id>
   ```

## ARM包结构

```
submission_q*/
├── paper/              # 论文元数据
│   └── paper_info.json
├── plan/               # 复现计划
│   └── reproduction_plan.md
├── code/               # 源代码
│   ├── main.py
│   └── ...
├── dataset/            # 数据集
├── result/             # 结果与图表
│   ├── *.png
│   └── results_summary.json
├── report/             # Dockerfile + requirements.txt
│   ├── Dockerfile
│   └── requirements.txt
├── trace/              # Agent执行日志
├── information/        # 经验笔记
└── README.md           # 项目说明
```

## 验证清单

提交前请确认：

- [ ] ARM包包含9个一级目录
- [ ] 代码可直接运行
- [ ] 包含Dockerfile和requirements.txt
- [ ] 包含结果与论文对比分析
- [ ] 包含Agent执行日志（trace）
- [ ] 文件大小不超过50MB

## 提交后

1. **查询状态**
   - 使用提交ID在Playground查询审核状态
   - 通常需要1-3个工作日

2. **查看评分**
   - 4C维度评分：Completeness, Correctness, Clarity, Cost
   - 复现级别：R0/R1/R2

3. **更新提交**
   - 如需修改，可在原提交页面点击"更新"
   - 上传新的ARM包

## 技术支持

- Playground文档: http://audp1430906.bohrium.tech:50002/docs
- DeployMaster API: http://47.238.112.245:50001/docs
- Hackathon讨论区: http://audp1430906.bohrium.tech:50002/discuss

---

**祝您提交顺利！**
