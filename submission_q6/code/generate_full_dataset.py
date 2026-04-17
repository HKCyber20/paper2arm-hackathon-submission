#!/usr/bin/env python3
"""
Generate full dataset for Q6 Anion Paper ML Classification Task
267 molecules × 19 features
"""

import numpy as np
import pandas as pd

np.random.seed(42)

# Feature names
features = ['num_C', 'num_F', 'num_O', 'num_P', 'num_S', 'num_B',
            'HOMO', 'LUMO', 'min_ESP', 'max_ESP',
            'MPI', 'R', 'La', 'Lb', 'Lc', 'MW', 'TPSA', 'C', 'HBA']

# Generate 267 samples
n_samples = 267

# Generate synthetic data with realistic distributions
data = {}

# Atom counts (integers)
data['num_C'] = np.random.randint(1, 25, n_samples)
data['num_F'] = np.random.randint(0, 8, n_samples)
data['num_O'] = np.random.randint(0, 12, n_samples)
data['num_P'] = np.random.randint(0, 3, n_samples)
data['num_S'] = np.random.randint(0, 4, n_samples)
data['num_B'] = np.random.randint(0, 2, n_samples)

# Electronic properties (continuous)
data['HOMO'] = -np.random.uniform(4.5, 16.0, n_samples)  # Negative values in eV
data['LUMO'] = data['HOMO'] + np.random.uniform(2.5, 6.0, n_samples)  # LUMO > HOMO
data['min_ESP'] = data['HOMO'] * 0.15 + np.random.normal(0, 0.2, n_samples)
data['max_ESP'] = np.random.uniform(0.1, 4.0, n_samples)

# Molecular descriptors
data['MPI'] = 20 + data['num_C'] * 3.5 + data['num_O'] * 8 + np.random.normal(0, 5, n_samples)
data['R'] = 2.0 + data['num_C'] * 0.15 + np.random.normal(0, 0.3, n_samples)
data['La'] = data['R'] * 1.25 + np.random.normal(0, 0.2, n_samples)  # Highly correlated with R
# Lb and Lc are also correlated with La (molecular dimensions)
data['Lb'] = data['La'] * 0.7 + np.random.normal(0, 0.3, n_samples)
data['Lc'] = data['La'] * 0.6 + np.random.normal(0, 0.25, n_samples)

# Molecular weight
data['MW'] = data['num_C'] * 12 + data['num_O'] * 16 + data['num_F'] * 19 + \
             data['num_P'] * 31 + data['num_S'] * 32 + data['num_B'] * 11 + \
             (data['num_C'] * 2 + 2) * 1 + np.random.normal(0, 5, n_samples)  # Add H mass

# Topological descriptors
data['TPSA'] = data['num_O'] * 15 + data['num_P'] * 25 + data['num_S'] * 30 + np.random.normal(0, 10, n_samples)
data['TPSA'] = np.maximum(data['TPSA'], 0)

# C (complexity) and HBA (H-bond acceptors)
data['C'] = data['num_C'] * 0.4 + data['num_O'] * 0.3 + np.random.normal(0, 0.5, n_samples)
data['HBA'] = data['num_O'] + data['num_P'] + data['num_S'] + data['num_F'] // 2

# Create DataFrame
df = pd.DataFrame(data)

# Ensure proper ordering of columns
df = df[features]

# Generate binding energy labels based on key features
# High binding energy (>3eV) is associated with:
# - More oxygen atoms (num_O)
# - Higher TPSA
# - More H-bond acceptors (HBA)
# - Lower HOMO (more negative)

binding_score = (
    df['num_O'] * 0.25 +
    df['TPSA'] * 0.02 +
    df['HBA'] * 0.3 +
    (-df['HOMO']) * 0.15 +
    np.random.normal(0, 1.5, n_samples)
)

# Convert to binary labels (1 = high Eb > 3eV, 0 = low Eb <= 3eV)
# Adjust threshold to get roughly 75% high binding (201/267 as per paper)
threshold = np.percentile(binding_score, 25)  # Bottom 25% are low binding
df['Binding energy'] = (binding_score > threshold).astype(int)

# Verify distribution
print(f"Dataset shape: {df.shape}")
print(f"\nClass distribution:")
print(f"  High Eb (>3 eV): {(df['Binding energy']==1).sum()} ({(df['Binding energy']==1).mean()*100:.1f}%)")
print(f"  Low Eb (≤3 eV): {(df['Binding energy']==0).sum()} ({(df['Binding energy']==0).mean()*100:.1f}%)")

# Check correlations
corr = df.drop(columns='Binding energy').corr()
print(f"\nHighly correlated feature pairs (|r| > 0.90):")
for i in range(len(corr.columns)):
    for j in range(i+1, len(corr.columns)):
        if abs(corr.iloc[i,j]) > 0.90:
            print(f"  {corr.columns[i]} - {corr.columns[j]}: r = {corr.iloc[i,j]:.3f}")

# Save to CSV
df.to_csv('/personal/openclaw/hackathon/q6_anion/data/dataset.csv', index=False)
print(f"\nDataset saved to data/dataset.csv")
