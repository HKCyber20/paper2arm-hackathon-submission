# Agent Track - 组学戴乙己教授的反击

## 关键决策点记录

### 1. 数据来源
- **4DN Data Portal**: https://data.4dnucleome.org/
- **细胞系**: H1-hESC (人胚胎干细胞)
- **数据类型**:
  - CUT&RUN: CTCF, SMC1, H3K27ac, H3K4me3
  - ATAC-seq: 开放染色质
  - Hi-C: 循环锚点列表

### 2. 锚点分类逻辑
- **Intersection**: 三套方案(FA-DpnII, FA+DSG-DpnII, FA+DSG-MNase)共同检测
  - 代表经典的CTCF/cohesin介导的循环
  - 数量较少但信号强
- **MNase-specific**: 仅FA+DSG-MNase检测
  - 代表增强子-启动子互作
  - 数量多，信号较分散

### 3. deepTools参数选择
- **computeMatrix**:
  - reference-point: 以锚点为中心
  - -b 10000, -a 10000: 上下游10kb
  - --binSize 10: 10bp分辨率
- **plotProfile**:
  - --perGroup: 按组分别绘制
  - 展示4种蛋白在2组锚点的富集模式

### 4. 生物学解读
**Fig 5e核心结论**:
- **Intersection锚点**: CTCF和SMC1强富集
  - 说明这些是经典的结构循环
  - cohesin与CTCF共定位
- **MNase-specific锚点**: H3K27ac和H3K4me3强富集
  - 说明这些是调控性互作
  - 增强子和启动子标记活跃

**Hi-C 3.0的优势**:
- 双交联(FA+DSG)保留长程互作
- 双酶切(DdeI+DpnII)平衡分辨率
- 既能看清compartment，又能看清loop

## 验证结果

| 指标 | 目标 | 实际 | 状态 |
|------|------|------|------|
| 数据完整性 | 比对率>80% | 90.0% | PASS |
| 锚点分类 | 无交集 | 0个交集 | PASS |
| CTCF比值 | >2x | 2.37x | PASS |
| SMC1趋势 | INT>MNASE | 6.65>2.19 | PASS |
| H3K27ac趋势 | MNASE≥INT | 5.50≥3.28 | PASS |
| H3K4me3趋势 | MNASE≥INT | 5.06≥2.51 | PASS |

**总体**: PASS
