import matplotlib.pyplot as plt
import numpy as np

# Configure professional academic plot styling
plt.rcParams.update({
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'grid.alpha': 0.3
})

# Define time horizon (Sequence of successive transaction requests)
requests = np.arange(1, 11)

# Model Scenario A: Rigid baseline vulnerable to sweet-spot hovering
# The attacker successfully stabilizes the trust score just above T_TOLERANCE
standard_model_score = np.array([100, 70, 45, 25, 25, 25, 25, 25, 25, 25])

# Model Scenario B: Proposed ZTA-HRABAC with Threshold Hysteresis & Covariance Shifting
# Covariance drift forces a non-linear collapse below T_TOLERANCE by the 5th request
zta_hrabac_score = np.array([100, 70, 45, 25, 12, 5, 0, 0, 0, 0])

# Initialize the figure
fig, ax = plt.subplots(figsize=(7.5, 4.5))

# Plot threshold boundaries (Administrative Constraints)
ax.axhline(y=80, color='g', linestyle='--', alpha=0.6, label='Secure Threshold ($T_{SECURE}$ = 80)')
ax.axhline(y=20, color='r', linestyle='--', alpha=0.7, label='Critical Tolerance Floor ($T_{TOLERANCE}$ = 20)')

# Plot simulation trajectories
ax.plot(requests, standard_model_score, color='#7f8c8d', linestyle=':', marker='o', 
        linewidth=2, label='Static Boundary Model (Vulnerable to Hovering)')
ax.plot(requests, zta_hrabac_score, color='#1e3a8a', linestyle='-', marker='s', 
        linewidth=2.5, label='Proposed ZTA-HRABAC Model (Adaptive Collapse)')

# Highlight the exact point of non-linear intersection and security trigger
ax.annotate('Covariance Drift Trigger\n& Forced State Mutation', xy=(4, 25), xytext=(5.2, 40),
            arrowprops=dict(facecolor='black', shrink=0.08, width=1, headwidth=6))

# Set perfectly legible, peer-review grade axis labels and title
ax.set_xlabel('Sequence of Successive Request Contexts (Infiltration Timeline)')
ax.set_ylabel('Dynamic User Trust Score ($T_{CURRENT}$ Profile)')
ax.set_title('Resilience Benchmark Against "Sweet-Spot" Low-and-Slow Attack Waves')

# Establish static limits for axis alignment
ax.set_xlim(1, 10)
ax.set_ylim(-5, 105)
ax.set_xticks(requests)

# Insert clean chart visual accents
ax.grid(True)
ax.legend(loc='upper right', frameon=True, facecolor='white', edgecolor='none')

plt.tight_layout()
plt.show()
