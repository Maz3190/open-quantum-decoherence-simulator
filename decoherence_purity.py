import numpy as np
import matplotlib.pyplot as plt

# 1. Initial Pure Quantum State: |psi(0)> = alpha|0> + beta|1>
# Equal superposition maximizes initial quantum coherence (rho_01 = 0.5)
alpha = 1.0 / np.sqrt(2.0)
beta = 1.0 / np.sqrt(2.0)
psi_0 = np.array([[alpha], [beta]], dtype=complex)

# Initial pure density matrix: rho(0) = |psi(0)><psi(0)|
rho_0 = psi_0 @ psi_0.conj().T

# 2. Time Grid & Environmental Coupling Parameters
t = np.linspace(0, 10.0, 500)  # Time in arbitrary units (e.g., ps)
omega_0 = 2.5                  # System energy splitting frequency
gamma_strong = 0.8             # Strong environment coupling (fast decoherence)
gamma_weak = 0.2               # Weak environment coupling (slow decoherence)

def evolve_dephasing(rho_init, time_array, omega, gamma):
    """
    Evolves a two-level reduced density matrix under pure environmental dephasing:
    Off-diagonal coherences decay as exp(-gamma * t - i * omega * t).
    """
    coherences = []
    purities = []
    linear_entropies = []

    for ti in time_array:
        decay = np.exp(-gamma * ti) * np.exp(-1j * omega * ti)
        rho_t = np.array([
            [rho_init[0, 0], rho_init[0, 1] * decay],
            [rho_init[1, 0] * np.conj(decay), rho_init[1, 1]]
        ], dtype=complex)

        # Off-diagonal coherence magnitude |rho_01(t)|
        coherences.append(np.abs(rho_t[0, 1]))
        # State purity: Tr(rho^2) -> 1 for pure state, 0.5 for maximally mixed
        purity = np.real(np.trace(rho_t @ rho_t))
        purities.append(purity)
        # Linear entropy: S_L = 1 - Tr(rho^2)
        linear_entropies.append(1.0 - purity)

    return np.array(coherences), np.array(purities), np.array(linear_entropies)

coh_strong, pur_strong, ent_strong = evolve_dephasing(rho_0, t, omega_0, gamma_strong)
coh_weak, pur_weak, ent_weak = evolve_dephasing(rho_0, t, omega_0, gamma_weak)

# 3. Visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.2))

# Panel A: Off-Diagonal Coherence Decay |rho_01(t)|
ax1.plot(t, coh_strong, color="#c0392b", linewidth=2.2,
         label=f"Strong Bath Coupling ($\\gamma = {gamma_strong}$)")
ax1.plot(t, coh_weak, color="#2980b9", linewidth=2.2, linestyle="--",
         label=f"Weak Bath Coupling ($\\gamma = {gamma_weak}$)")
ax1.axhline(0.0, color="#7f8c8d", linestyle=":", linewidth=1.2)
ax1.set_title("Suppression of Quantum Interference ($|\\rho_{01}(t)| \\to 0$)", fontsize=11)
ax1.set_xlabel("Interaction Time ($t$)", fontsize=10)
ax1.set_ylabel("Off-Diagonal Coherence $|\\rho_{01}(t)|$", fontsize=10)
ax1.set_ylim(-0.02, 0.55)
ax1.legend(frameon=True, fontsize=9)
ax1.grid(True, linestyle=":", alpha=0.6)

# Panel B: Purity Loss Tr(rho^2) & Linear Entropy Growth
ax2.plot(t, pur_strong, color="#8e44ad", linewidth=2.2,
         label="Purity $\\mathrm{Tr}(\\rho^2)$ ($\\gamma = 0.8$)")
ax2.plot(t, ent_strong, color="#27ae60", linewidth=2.2, linestyle="-.",
         label="Linear Entropy $1 - \\mathrm{Tr}(\\rho^2)$ ($\\gamma = 0.8$)")
ax2.axhline(1.0, color="#34495e", linestyle=":", linewidth=1.2, label="Pure State Limit ($1.0$)")
ax2.axhline(0.5, color="#7f8c8d", linestyle="--", linewidth=1.2, label="Classical Mixed Limit ($0.5$)")
ax2.set_title("Quantum-to-Classical Transition: Purity & Entropy Dynamics", fontsize=11)
ax2.set_xlabel("Interaction Time ($t$)", fontsize=10)
ax2.set_ylabel("Measure Value", fontsize=10)
ax2.set_ylim(0.0, 1.08)
ax2.legend(frameon=True, fontsize=8.5, loc="center right")
ax2.grid(True, linestyle=":", alpha=0.6)

plt.tight_layout()
plt.savefig("decoherence_purity_decay.png", dpi=300)
plt.show()
print(f"Final Purity (gamma={gamma_strong}, t={t[-1]}): {pur_strong[-1]:.4f}")