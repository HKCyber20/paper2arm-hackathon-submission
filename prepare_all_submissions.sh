#!/bin/bash
# 批量准备所有题目的ARM包

cd /personal/openclaw/hackathon

echo "=========================================="
echo "准备所有题目的ARM包"
echo "=========================================="

# 题目列表
QUESTIONS=("q1_deepmd" "q2_wind" "q3_rustbca" "q4_huggett" "q5_hic" "q6_anion" "q7_tsaseq")
QUESTION_NAMES=("木木张和豆角焖面的顿悟" "陈大佬和雷哥的风电场保卫战" "欧神凌晨三点的抉择" "胡汉三和王阿姨的储蓄之争" "组学戴乙己教授的反击" "硬币的另一面" "菜市场散伙后的钉子户调查")

echo ""
echo "已完成的题目:"
for i in "${!QUESTIONS[@]}"; do
    echo "  $((i+1)). ${QUESTION_NAMES[$i]} (${QUESTIONS[$i]})"
done

echo ""
echo "提交包位置:"
echo "  - /personal/openclaw/hackathon/submission_q6_arm.zip (已创建)"
echo ""
echo "其他题目需要手动整理到ARM结构后打包"
echo ""
echo "提交方式:"
echo "  1. 手动提交: 访问 http://audp1430906.bohrium.tech:50002"
echo "  2. DeployMaster: 推送到GitHub后调用API"
echo ""
echo "=========================================="
echo "Git仓库状态:"
git log --oneline -3
echo ""
echo "文件统计:"
find submission_* -type f | wc -l
echo "个文件已准备"
