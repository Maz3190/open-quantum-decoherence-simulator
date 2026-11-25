import numpy as np
import matplotlib.pyplot as plt

# 1. Spatial & Momentum Grid Setup (Atomic Units: hbar = 1, m = 1)
N = 2048
L = 200.0
x = np.linspace(-L / 2, L / 2, N, endpoint=False)
dx = x[1] - x[0]
k = 2 * np.pi * np.fft.fftfreq(N, d=dx)

# 2. Initial Gaussian Wavepacket Moving Toward a Finite Potential Barrier
x0 = -35.0      # Initial center
sigma = 4.0     # Wavepacket spatial width
k0 = 2.0        # Initial carrier momentum (Kinetic Energy E0 ~ k0^2 / 2 = 2.0)

psi = (1.0 / (2 * np.pi * sigma**2)**0.25) * np.exp(-(x - x0)**2 / (4 * sigma**2)) * np.exp(1j * k0 * x)
psi /= np.sqrt(np.sum(np.abs(psi)**2) * dx)

# Finite rectangular barrier centered at x = 0 with height V0 ~ E0 (50/50 beam-splitter regime)
V0 = 2.05
barrier_width = 2.0
V = np.where(np.abs(x) <= barrier_width / 2, V0, 0.0)

# 3. Split-Operator Fourier Method (SOFM) Time Propagation
dt = 0.05
steps = 750
exp_V_half = np.exp(-0.5j * V * dt)
exp_T = np.exp(-0.5j * (k**2) * dt)

snapshots = {0: np.abs(psi)**2}
capture_steps = [320, steps]

for step in range(1, steps + 1):
    psi = exp_V_half * psi
    psi_k = np.fft.fft(psi)
    psi_k = exp_T * psi_k
    psi = np.fft.ifft(psi_k)
    psi = exp_V_half * psi
    if step in capture_steps:
        snapshots[step] = np.abs(psi)**2

# Calculate reflected vs transmitted probability weights
reflected_prob = np.sum(np.abs(psi[x < 0])**2) * dx
transmitted_prob = np.sum(np.abs(psi[x > 0])**2) * dx
total_norm = reflected_prob + transmitted_prob

# 4. Visualization
fig, axes = plt.subplots(3, 1, figsize=(10, 7.5), sharex=True)
titles = [
    f"Initial State ($t = 0$): Incident Gaussian Wavepacket ($E_0 \\approx {0.5*k0**2:.2f}$)",
    f"Barrier Interaction ($t = {320*dt:.1f}$): Coherent Superposition Inside Barrier",
    f"Spatial Branching ($t = {steps*dt:.1f}$): Reflected ($P_R = {reflected_prob:.2f}$) vs. Transmitted ($P_T = {transmitted_prob:.2f}$)"
]
colors = ["#2980b9", "#8e44ad", "#27ae60"]

for ax, (step_idx, density), title, col in zip(axes, snapshots.items(), titles, colors):
    ax.plot(x, density, color=col, linewidth=1.8, label="$|\\psi(x, t)|^2$")
    ax.fill_between(x, density, color=col, alpha=0.2)
    ax_v = ax.twinx()
    ax_v.plot(x, V, color="#c0392b", linestyle="--", linewidth=1.3, label="Potential Barrier $V(x)$")
    ax_v.set_ylim(0, 3.0)
    ax_v.set_ylabel("$V(x)$", color="#c0392b", fontsize=9)
    ax.set_ylabel("$|\\psi(x, t)|^2$", fontsize=9.5)
    ax.set_title(title, fontsize=10.5)
    ax.grid(True, linestyle=":", alpha=0.6)

axes[-1].set_xlabel("Spatial Coordinate $x$ (Atomic Units)", fontsize=10)
plt.xlim(-75, 75)
plt.tight_layout()
plt.savefig("wavepacket_splitting.png", dpi=300)
plt.show()
print(f"Norm Conservation Check: {total_norm:.6f} | Reflected: {reflected_prob:.3f} | Transmitted: {transmitted_prob:.3f}")
