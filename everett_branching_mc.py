import numpy as np
import matplotlib.pyplot as plt

# 1. Quantum State Parameters: |psi> = alpha|0> + beta|1>
# Asymmetric superposition to distinguish Born rule from naive branch counting
p0_true = 0.75
p1_true = 1.0 - p0_true
alpha = np.sqrt(p0_true)
beta = np.sqrt(p1_true)

M = 12  # Number of sequential measurements (2^12 = 4,096 total Everettian branches)

# 2. Exact Branch Tree Enumeration
# For k outcomes of |0> in M measurements, branch weight is |alpha|^(2k) * |beta|^(2(M-k))
k_values = np.arange(M + 1)
# Number of branches with k |0>-outcomes (naive branch counting distribution)
from scipy.special import comb
branch_counts = comb(M, k_values)
naive_probs = branch_counts / (2**M)
born_probs = branch_counts * (p0_true**k_values) * (p1_true**(M - k_values))

# 3. Monte Carlo Trajectory Sampling (Observer Worldlines)
mc_steps = np.logspace(1, 4.5, 40, dtype=int)
mc_estimated_p0 = []
rng = np.random.default_rng(42)

for n_traj in mc_steps:
    # Each trajectory samples M sequential quantum outcomes according to Born weights
    outcomes = rng.choice([1, 0], size=(n_traj, M), p=[p0_true, p1_true])
    # Relative frequency of |0> across all trajectories
    mc_estimated_p0.append(np.mean(outcomes))

# 4. Visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.2))

# Panel A: Branch Weight Distribution (Born Rule vs Naive Counting)
fractions = k_values / M
ax1.bar(fractions - 0.015, naive_probs, width=0.03, color="#95a5a6", alpha=0.85,
        label="Naive Branch Counting ($1/2^M$)")
ax1.bar(fractions + 0.015, born_probs, width=0.03, color="#2980b9", alpha=0.9,
        label="Everettian Born-Weighted Measure")
ax1.axvline(p0_true, color="#c0392b", linestyle="--", linewidth=1.8,
            label=f"True Born Probability ($|\\alpha|^2 = {p0_true}$)")
ax1.set_title(f"Branch Measure Distribution ($M = {M}$ Splits, $2^M = {2**M}$ Branches)", fontsize=11)
ax1.set_xlabel("Fraction of $|0\\rangle$ Outcomes Along Branch ($k/M$)", fontsize=10)
ax1.set_ylabel("Total Probability Measure", fontsize=10)
ax1.legend(frameon=True, fontsize=8.5)
ax1.grid(True, linestyle=":", alpha=0.6)

# Panel B: Monte Carlo Convergence of Observer Frequencies
ax2.semilogx(mc_steps, mc_estimated_p0, "o-", color="#2980b9", markersize=4, linewidth=1.5,
             label="Monte Carlo Trajectory Frequency")
ax2.axhline(p0_true, color="#c0392b", linestyle="--", linewidth=1.8,
            label=f"Exact Born Limit ($|\\alpha|^2 = {p0_true}$)")
ax2.axhline(0.5, color="#7f8c8d", linestyle=":", linewidth=1.5,
            label="Naive Branch-Counting Limit ($0.50$)")
ax2.set_title("Monte Carlo Trajectory Convergence to the Born Rule", fontsize=11)
ax2.set_xlabel("Number of Sampled Trajectories ($N_{\\mathrm{MC}}$)", fontsize=10)
ax2.set_ylabel("Observed Relative Frequency of $|0\\rangle$", fontsize=10)
ax2.set_ylim(0.4, 0.9)
ax2.legend(frameon=True, fontsize=8.5)
ax2.grid(True, which="both", linestyle=":", alpha=0.6)

plt.tight_layout()
plt.savefig("born_rule_convergence.png", dpi=300)
plt.show()
print(f"Final MC Estimate (N={mc_steps[-1]}): {mc_estimated_p0[-1]:.4f} vs Exact: {p0_true:.4f}")