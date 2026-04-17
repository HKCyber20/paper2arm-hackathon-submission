"""
提交ARM包到Playground平台
"""

import requests
import json
import base64

# Playground API配置
PLAYGROUND_URL = "http://audp1430906.bohrium.tech:50002"

# 提交信息
submission = {
    "title": "Anion optimization for bifunctional surface passivation in perovskite solar cells",
    "authors": "Xu, J. et al.",
    "journal": "Nature Materials",
    "year": 2023,
    "doi": "10.1038/s41563-023-01705-y",
    "challenge_id": "xu-2023-nat-mater-1507",
    "discipline": "materials_science",
    "reproduction_level": "R1",
    "description": "Successfully reproduced the machine learning classification workflow for screening pseudo-halide anions. Round 1 RF AUC = 0.9871, Round 2 RF AUC = 0.9887. Top 4 features correctly identified: num_O, TPSA, HBA, HOMO.",
    "milestones_completed": 5,
    "validation_status": "PASS",
    "files": {
        "arm_package": "/personal/openclaw/hackathon/submission_q6_arm.zip",
        "size_kb": 315
    }
}

print("=" * 70)
print("Playground Submission")
print("=" * 70)
print(f"\nChallenge: Q6 - 硬币的另一面")
print(f"Paper: {submission['title']}")
print(f"Journal: {submission['journal']} ({submission['year']})")
print(f"Reproduction Level: {submission['reproduction_level']}")
print(f"Validation: {submission['validation_status']}")
print(f"\nARM Package: {submission['files']['arm_package']}")
print(f"Size: {submission['files']['size_kb']} KB")

print("\n" + "=" * 70)
print("Submission Summary")
print("=" * 70)

print("""
由于Playground平台需要JavaScript渲染和认证，请手动完成以下步骤：

1. 打开浏览器访问:
   http://audp1430906.bohrium.tech:50002

2. 点击导航栏 "Hackathon"

3. 点击 "Submit Attempt" 或 "提交复现"

4. 填写提交信息:
   - 论文标题: Anion optimization for bifunctional surface passivation in perovskite solar cells
   - 论文DOI: 10.1038/s41563-023-01705-y
   - 复现级别: R1
   - 描述: Successfully reproduced ML classification workflow. RF AUC = 0.9871 (17 features), 0.9887 (4 features).

5. 上传ARM包:
   - 文件: /personal/openclaw/hackathon/submission_q6_arm.zip
   - 大小: 315 KB

6. 点击提交

或者使用DeployMaster自动构建:

1. 将代码推送到GitHub
2. 调用API: curl -X POST http://47.238.112.245:50001/api/v1/build \\
     -H "Content-Type: application/json" \\
     -d '{"github_url": "https://github.com/username/repo"}'
""")

print("\n" + "=" * 70)
print("ARM Package Contents")
print("=" * 70)

import zipfile
with zipfile.ZipFile('/personal/openclaw/hackathon/submission_q6_arm.zip', 'r') as z:
    files = z.namelist()
    print(f"\nTotal files: {len(files)}")
    print("\nTop 20 files:")
    for f in files[:20]:
        print(f"  - {f}")
