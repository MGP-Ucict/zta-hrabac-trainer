# AI-Trust-HRABAC: Zero-Trust Adaptive Access Control Validation Suite

This repository contains the official empirical validation framework and source code for the **AI-Trust-HRABAC** model, a decoupled, two-tier Zero-Trust Architecture designed for next-generation core banking infrastructure.

The included modules validate the context-aware dynamic penalty weight mapping, execute continuous risk calibration via localized Z-score distance metrics, and provide the complete cross-validation and hyperparameter sensitivity (ablation) pipeline required to replicate the findings presented in the manuscript.

---

## 🛠️ System Requirements & Dependencies

The suite is engineered to operate efficiently with standard scientific Python environments. All background computation cycles maintain an O(1) evaluation footprint appropriate for high-throughput production workloads.

### Prerequisites
* **Python 3.8+**
* **NumPy** (High-performance array manipulations)
* **Scikit-Learn** (Unsupervised Isolation Forest architecture)
* **Joblib** (Model serialization pipelines)

### Installation
Install the necessary dependencies via `pip`:
```bash
pip install numpy scikit-learn joblib
```

---

## 📂 Repository Structure & Component Blueprint

The source matrix is divided into distinct operational scripts mapping onto the core chapters of the implementation manuscript:

### 1. `ai_model_trainer.py` (Core Infrastructure Module)
* **Manuscript Reference:** Section V-A (Decoupled Off-Chain Web Layer Infrastructure).
* **Functionality:** Implements the production-level `AIModelTrainer` class. It manages user behavioral telemetry profiling, automates background Isolation Forest clustering over a continuous 4-dimensional space, handles secure file-system serialization (`.pkl`), and calculates live contextual risk deductions.
* **Feature Vector Layout (n=4 continuous metrics):** 
  x = [x_{\text{time}}, x_{\text{ip}}, x_{\text{device}}, x_{\text{inactivity}}]

### 2. `benchmark_tables.py` (Empirical Evaluation Suite)
* **Manuscript Reference:** Section V-B (Performance Verification & Ablation Analysis).
* **Functionality:** The primary validation execution script. It generates a high-fidelity synthetic database of N=10,000 sequential banking logs to profile standard user routines. It then benchmarks the proposed dynamic framework against a rigid, hand-tuned static baseline across two stress-test scenarios:
  * **Scenario A (Benign Behavioral Drift):** Legitimate corporate users shifting transaction vectors slightly outside traditional operational windows.
  * **Scenario B (Multi-Vector Threat Injection):** Coordinated brute-force, device-spoofing, and session-hijacking attacks.
* **Outputs:** Automatically computes the raw data arrays, False Positive Rates (FPR), False Negative Rates (FNR), and execution latencies required to populate **Table I** and **Table II**.

---

## 🚀 Execution Guide & Reproducibility Pipeline

To trigger the automated cross-validation loops and reproduce the manuscript's comparative data matrices, run the integrated evaluation engine:

```bash
python benchmark_tables.py
```

### Expected Console Output Architecture
Upon successful execution, the pipeline handles sequential data generation and outputs clean statistical results directly matching your validation drafts:

=====

![Runned tests output](./image.png)

## 🔬 Mathematical Integration Summary

The dynamic penalty scoring evaluated inside `evaluate_ai_system()` directly satisfies the algebraic constraints established below **Definition 2** in the text:

$$W_j(x_j) = \text{int}\left( \max\left(0, \min\left(50, \, \left\vert{} \frac{x_j - \mu_j}{\sigma_j + \epsilon} \right\vert{} \cdot \gamma_j \right)\right) \right)$$

Where:
* $\mu_j$ and $\sigma_j$ represent the moving statistical invariants computed across the sliding profile window.
* $\epsilon = 10^{-6}$ acts as the regularization guard against zero-division errors.
* $\gamma_j$ isolates institutional scaling coefficients ($\gamma_{\text{time}}=10$, $\gamma_{\text{location}}=15$, $\gamma_{\text{device}}=12$, $\gamma_{\text{inactivity}}=8$) manipulated dynamically via the Policy Management Point (PMP) to optimize boundary definitions under volatile operational threat levels.




