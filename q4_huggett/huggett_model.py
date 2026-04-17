"""
Huggett (1993) 异质性代理人不完全市场模型复现
=============================================
使用向量化加速的 VFI
"""

import numpy as np
from scipy.optimize import brentq
import json

class HuggettModel:
    """
    Huggett (1993) 模型实现 - 向量化版本
    """
    
    def __init__(self, gamma=1.5, beta=0.99322, 
                 e_h=1.0, e_l=0.1,
                 pi_hh=0.925, pi_hl=0.075, pi_lh=0.5, pi_ll=0.5,
                 n_a=180, a_min=-2.0, a_max=8.0):
        """
        初始化模型参数
        """
        self.gamma = gamma
        self.beta = beta
        self.e = np.array([e_h, e_l])
        
        self.Pi = np.array([[pi_hh, pi_hl],
                            [pi_lh, pi_ll]])
        
        self.n_a = n_a
        self.a_min = a_min
        self.a_max = a_max
        
        # 构建资产网格
        self.a_grid = np.linspace(self.a_min, self.a_max, self.n_a)
        
        # 初始化
        self.V = np.zeros((n_a, 2))
        self.policy_a = np.zeros((n_a, 2), dtype=int)
        self.mu = np.ones((n_a, 2)) / (n_a * 2)
        
    def utility(self, c):
        """CRRA效用函数 - 向量化"""
        if self.gamma == 1:
            return np.log(c)
        else:
            return c**(1 - self.gamma) / (1 - self.gamma)
    
    def solve_household_problem(self, q, tol=1e-5, max_iter=2000):
        """
        使用向量化值函数迭代求解家庭问题
        """
        n_a = self.n_a
        n_e = 2
        
        # 初始化值函数
        V = np.zeros((n_a, n_e))
        V_new = np.zeros((n_a, n_e))
        policy_a = np.zeros((n_a, n_e), dtype=int)
        
        # 预计算消费矩阵 C[i_a, i_e, i_a_prime]
        # c = e + a - q * a_prime
        a_grid_col = self.a_grid.reshape(-1, 1, 1)  # (n_a, 1, 1)
        e_row = self.e.reshape(1, -1, 1)  # (1, n_e, 1)
        a_prime = self.a_grid.reshape(1, 1, -1)  # (1, 1, n_a)
        
        C = e_row + a_grid_col - q * a_prime  # (n_a, n_e, n_a)
        
        # 标记不可行的消费
        feasible = C > 1e-10
        
        for iteration in range(max_iter):
            # 对每个 (a, e) 状态，在所有 a' 上计算期望效用
            # EV[a_prime, e] = sum_{e'} Pi[e, e'] * V_interp(a_prime, e')
            
            # 对每个 e'，在 a_prime 上插值 V
            EV = np.zeros((n_a, n_e, n_a))
            for i_e_prime in range(n_e):
                V_interp = np.interp(self.a_grid, self.a_grid, V[:, i_e_prime])
                for i_e in range(n_e):
                    EV[:, i_e, :] += self.Pi[i_e, i_e_prime] * V_interp.reshape(1, -1)
            
            # 计算总效用矩阵
            U = np.full((n_a, n_e, n_a), -1e20)
            U[feasible] = self.utility(C[feasible]) + self.beta * EV[feasible]
            
            # 找到最优的 a'
            for i_a in range(n_a):
                for i_e in range(n_e):
                    best_idx = np.argmax(U[i_a, i_e, :])
                    V_new[i_a, i_e] = U[i_a, i_e, best_idx]
                    policy_a[i_a, i_e] = best_idx
            
            # 检查收敛
            diff = np.max(np.abs(V_new - V))
            V = V_new.copy()
            
            if iteration % 200 == 0:
                print(f"    VFI iteration {iteration}, diff={diff:.2e}")
            
            if diff < tol:
                print(f"  VFI converged after {iteration + 1} iterations, diff={diff:.2e}")
                break
        else:
            print(f"  VFI reached max iterations ({max_iter}), diff={diff:.2e}")
        
        self.V = V
        self.policy_a = policy_a
        return V, policy_a
    
    def compute_stationary_distribution(self, policy_a, max_iter=5000, tol=1e-10):
        """计算稳态分布"""
        n_a = self.n_a
        n_e = 2
        
        mu = np.ones((n_a, n_e)) / (n_a * n_e)
        
        for iteration in range(max_iter):
            mu_new = np.zeros((n_a, n_e))
            
            for i_a in range(n_a):
                for i_e in range(n_e):
                    if mu[i_a, i_e] > 1e-15:
                        i_a_prime = policy_a[i_a, i_e]
                        for i_e_prime in range(n_e):
                            prob = self.Pi[i_e, i_e_prime]
                            mu_new[i_a_prime, i_e_prime] += mu[i_a, i_e] * prob
            
            total = np.sum(mu_new)
            if total > 0:
                mu_new = mu_new / total
            
            diff = np.max(np.abs(mu_new - mu))
            mu = mu_new
            
            if diff < tol:
                print(f"  Distribution converged after {iteration + 1} iterations")
                break
        
        self.mu = mu
        return mu
    
    def compute_excess_demand(self, q):
        """计算超额需求"""
        V, policy_a = self.solve_household_problem(q)
        mu = self.compute_stationary_distribution(policy_a)
        
        total_bond_demand = 0.0
        for i_a in range(self.n_a):
            for i_e in range(2):
                a_prime = self.a_grid[policy_a[i_a, i_e]]
                total_bond_demand += mu[i_a, i_e] * a_prime
        
        return total_bond_demand
    
    def find_equilibrium(self, q_min=0.9, q_max=1.1):
        """使用Brent法寻找均衡债券价格"""
        print(f"  Searching for equilibrium in q ∈ [{q_min:.4f}, {q_max:.4f}]...")
        
        excess_min = self.compute_excess_demand(q_min)
        excess_max = self.compute_excess_demand(q_max)
        
        print(f"  Excess demand at q={q_min:.4f}: {excess_min:.6f}")
        print(f"  Excess demand at q={q_max:.4f}: {excess_max:.6f}")
        
        if excess_min * excess_max > 0:
            print("  Expanding search range...")
            q_min, q_max = 0.8, 1.2
            excess_min = self.compute_excess_demand(q_min)
            excess_max = self.compute_excess_demand(q_max)
            print(f"  Excess demand at q={q_min:.4f}: {excess_min:.6f}")
            print(f"  Excess demand at q={q_max:.4f}: {excess_max:.6f}")
        
        q_star = brentq(self.compute_excess_demand, q_min, q_max, xtol=1e-10)
        
        r = 1.0 / q_star - 1.0
        r_annual = r * 100.0
        verification = (1 + r) * q_star
        
        print(f"  Equilibrium found: q* = {q_star:.6f}")
        print(f"  Annual interest rate: r = {r_annual:.3f}%")
        print(f"  Verification (1+r)*q = {verification:.10f}")
        
        return q_star, r_annual
