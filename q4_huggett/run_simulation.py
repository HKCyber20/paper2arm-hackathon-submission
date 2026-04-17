"""
Huggett (1993) 模型复现 - 主运行脚本
====================================
运行8组参数的模拟，生成Table 1和Table 2
"""

import numpy as np
import json
from huggett_model import HuggettModel

def run_all_simulations():
    """
    运行所有8组参数的模拟
    """
    
    # 参数设置
    beta = 0.99322
    e_h = 1.0
    e_l = 0.1
    pi_hh = 0.925
    pi_hl = 0.075
    pi_lh = 0.5
    pi_ll = 0.5
    n_a = 180
    a_max = 8.0
    
    # 借贷约束的4个取值
    a_mins = [-2.0, -4.0, -6.0, -8.0]
    
    # 风险厌恶系数的2个取值
    gammas = [1.5, 3.0]
    
    # 论文参考值
    reference_table1_q = [1.0124, 0.9962, 0.9944, 0.9935]
    reference_table1_r = [-7.127, 2.311, 3.427, 3.990]
    reference_table2_q = [1.0448, 1.0045, 0.9970, 0.9940]
    reference_table2_r = [-23.122, -2.658, 1.819, 3.677]
    
    # 存储结果
    results = {
        "table1": {"q": [], "r": [], "q_ref": reference_table1_q, "r_ref": reference_table1_r},
        "table2": {"q": [], "r": [], "q_ref": reference_table2_q, "r_ref": reference_table2_r}
    }
    
    # Agent Track 记录
    agent_track = {
        "grid_setup": {
            "description": "均匀网格 (uniform grid)",
            "n_a": n_a,
            "a_max": a_max,
            "grid_type": "linear",
            "rationale": "使用均匀网格覆盖资产区间[a_min, a_max]，在借贷约束附近保持足够分辨率"
        },
        "convergence_criteria": {
            "vfi_tol": 1e-5,
            "distribution_tol": 1e-10,
            "brent_xtol": 1e-10,
            "description": "VFI使用最大范数差值<1e-5，稳态分布迭代<1e-10，Brent法求解<1e-10"
        },
        "annualization": {
            "formula": "r_annual = (1/q - 1) * 100",
            "description": "债券价格q与利率关系: q = 1/(1+r)，年化利率转换为百分比"
        }
    }
    
    print("=" * 70)
    print("Huggett (1993) 模型复现")
    print("=" * 70)
    print()
    
    # Table 1: gamma = 1.5
    print("Table 1: γ = 1.5")
    print("-" * 70)
    gamma = 1.5
    
    for i, a_min in enumerate(a_mins):
        print(f"\nCase {i+1}: a_min = {a_min}")
        print("-" * 40)
        
        # 创建模型
        model = HuggettModel(
            gamma=gamma,
            beta=beta,
            e_h=e_h,
            e_l=e_l,
            pi_hh=pi_hh,
            pi_hl=pi_hl,
            pi_lh=pi_lh,
            pi_ll=pi_ll,
            n_a=n_a,
            a_min=a_min,
            a_max=a_max
        )
        
        # 寻找均衡
        q_star, r_annual = model.find_equilibrium(q_min=0.9, q_max=1.1)
        
        results["table1"]["q"].append(float(q_star))
        results["table1"]["r"].append(float(r_annual))
        
        # 计算误差
        q_error = abs(q_star - reference_table1_q[i]) / reference_table1_q[i] * 100
        r_error = abs(r_annual - reference_table1_r[i])
        
        print(f"  Reference q: {reference_table1_q[i]:.4f}, Computed q: {q_star:.4f}, Error: {q_error:.3f}%")
        print(f"  Reference r: {reference_table1_r[i]:.3f}%, Computed r: {r_annual:.3f}%, Error: {r_error:.3f}%")
    
    print()
    print("=" * 70)
    
    # Table 2: gamma = 3.0
    print("\nTable 2: γ = 3.0")
    print("-" * 70)
    gamma = 3.0
    
    for i, a_min in enumerate(a_mins):
        print(f"\nCase {i+1}: a_min = {a_min}")
        print("-" * 40)
        
        # 创建模型
        model = HuggettModel(
            gamma=gamma,
            beta=beta,
            e_h=e_h,
            e_l=e_l,
            pi_hh=pi_hh,
            pi_hl=pi_hl,
            pi_lh=pi_lh,
            pi_ll=pi_ll,
            n_a=n_a,
            a_min=a_min,
            a_max=a_max
        )
        
        # 寻找均衡
        q_star, r_annual = model.find_equilibrium(q_min=0.9, q_max=1.1)
        
        results["table2"]["q"].append(float(q_star))
        results["table2"]["r"].append(float(r_annual))
        
        # 计算误差
        q_error = abs(q_star - reference_table2_q[i]) / reference_table2_q[i] * 100
        r_error = abs(r_annual - reference_table2_r[i])
        
        print(f"  Reference q: {reference_table2_q[i]:.4f}, Computed q: {q_star:.4f}, Error: {q_error:.3f}%")
        print(f"  Reference r: {reference_table2_r[i]:.3f}%, Computed r: {r_annual:.3f}%, Error: {r_error:.3f}%")
    
    print()
    print("=" * 70)
    
    # 保存结果
    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    with open("agent_track.json", "w") as f:
        json.dump(agent_track, f, indent=2)
    
    print("\nResults saved to results.json")
    print("Agent track saved to agent_track.json")
    
    return results, agent_track


def print_summary_table(results):
    """
    打印结果汇总表
    """
    print("\n" + "=" * 80)
    print("复现结果汇总")
    print("=" * 80)
    
    # Table 1
    print("\nTable 1: γ = 1.5")
    print("-" * 80)
    print(f"{'a_min':<10} {'q (ref)':<12} {'q (comp)':<12} {'q error %':<12} {'r (ref)':<12} {'r (comp)':<12} {'r error':<12}")
    print("-" * 80)
    
    a_mins = [-2.0, -4.0, -6.0, -8.0]
    for i, a_min in enumerate(a_mins):
        q_ref = results["table1"]["q_ref"][i]
        q_comp = results["table1"]["q"][i]
        r_ref = results["table1"]["r_ref"][i]
        r_comp = results["table1"]["r"][i]
        
        q_error = abs(q_comp - q_ref) / q_ref * 100
        r_error = abs(r_comp - r_ref)
        
        print(f"{a_min:<10} {q_ref:<12.4f} {q_comp:<12.4f} {q_error:<12.3f} {r_ref:<12.3f} {r_comp:<12.3f} {r_error:<12.3f}")
    
    # Table 2
    print("\nTable 2: γ = 3.0")
    print("-" * 80)
    print(f"{'a_min':<10} {'q (ref)':<12} {'q (comp)':<12} {'q error %':<12} {'r (ref)':<12} {'r (comp)':<12} {'r error':<12}")
    print("-" * 80)
    
    for i, a_min in enumerate(a_mins):
        q_ref = results["table2"]["q_ref"][i]
        q_comp = results["table2"]["q"][i]
        r_ref = results["table2"]["r_ref"][i]
        r_comp = results["table2"]["r"][i]
        
        q_error = abs(q_comp - q_ref) / q_ref * 100
        r_error = abs(r_comp - r_ref)
        
        print(f"{a_min:<10} {q_ref:<12.4f} {q_comp:<12.4f} {q_error:<12.3f} {r_ref:<12.3f} {r_comp:<12.3f} {r_error:<12.3f}")
    
    print("\n" + "=" * 80)
    
    # 验证标准检查
    print("\n验证标准检查:")
    print("-" * 80)
    
    all_q_pass = True
    all_r_pass = True
    
    for table_name in ["table1", "table2"]:
        for i in range(4):
            q_ref = results[table_name]["q_ref"][i]
            q_comp = results[table_name]["q"][i]
            r_ref = results[table_name]["r_ref"][i]
            r_comp = results[table_name]["r"][i]
            
            q_error = abs(q_comp - q_ref) / q_ref * 100
            r_error = abs(r_comp - r_ref)
            
            if q_error >= 1.0:
                all_q_pass = False
                print(f"  {table_name} case {i+1}: q误差 {q_error:.3f}% >= 1% [FAIL]")
            
            if r_error >= 2.0:
                all_r_pass = False
                print(f"  {table_name} case {i+1}: r误差 {r_error:.3f} >= 2 [FAIL]")
    
    if all_q_pass:
        print("  ✓ 所有q相对误差 < 1%")
    if all_r_pass:
        print("  ✓ 所有r绝对误差 < 2个百分点")
    
    if all_q_pass and all_r_pass:
        print("\n  ✓✓✓ 所有验证标准通过! ✓✓✓")
    
    print("=" * 80)


if __name__ == "__main__":
    results, agent_track = run_all_simulations()
    print_summary_table(results)
