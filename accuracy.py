import time
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# ---------------------------------------------------------------------------------
# STEP 1: GLOBAL DATA GENERATION ENGINE (N = 10,000 BASE LOGS)
# ---------------------------------------------------------------------------------
np.random.seed(42)
N_total_clean = 10000

print("=" * 95)
print(" INTEGRATED EXPERIMENTAL ENGINE: CLASSIFICATION QUALITY & ACCURACY BENCHMARK")
print("=" * 95)
print("[INFO] Simulating 10,000 baseline clean logs for user profile...")

# Standard baseline distributions for legitimate user activity
clean_time = np.random.normal(12.0, 1.5, N_total_clean)        
clean_ip = np.full(N_total_clean, 2130706433)                 
clean_device = np.full(N_total_clean, 987654321)             
clean_inactivity = np.random.exponential(120, N_total_clean)  

# REALISTIC BEHAVIORAL DRIFT INJECTION:
# Simulating authentic human variations (occasional late-night tasking and extended idle gaps)
for i in range(10, 115):
    clean_time[i] = 18.05        # 6:03 PM (Legitimate slight overtime)
    clean_inactivity[i] = 530    # Authentic longer operational delay

X_clean_pool = np.column_stack((clean_time, clean_ip, clean_device, clean_inactivity))

# Injecting N = 500 malicious adversarial attack vectors
N_attack = 500
attack_time = np.random.uniform(0.0, 6.0, N_attack)           
attack_ip = np.random.randint(1000000000, 2000000000, N_attack) 
attack_device = np.random.randint(10000000, 50000000, N_attack) 
attack_inactivity = np.random.uniform(1000, 3000, N_attack)   

X_test_attack = np.column_stack((attack_time, attack_ip, attack_device, attack_inactivity))


# ---------------------------------------------------------------------------------
# THE EXACT SPECIFIED AI EVALUATION ENGINE (MANUSCRIPT DEFINITION 2 & 3)
# ---------------------------------------------------------------------------------
def evaluate_ai_system(dataset, mean, std):
    predictions = []
    gamma = [10, 15, 12, 8] # Gamma risk weights specified in the paper
    epsilon = 1e-6          # Safeguard value preventing divide-by-zero bounds
    
    for row in dataset:
        total_penalty = 0
        for j in range(4):
            # Identity-based constraints handle static corporate assets
            if (j == 1 and row[j] != 2130706433) or (j == 2 and row[j] != 987654321):
                total_penalty += 50
                continue
                
            if std[j] == 0:
                continue
                
            # EXACT MANUSCRIPT ALGEBRAIC MAPPING FROM DEFINITION 2
            z_score_dist = np.abs((row[j] - mean[j]) / (std[j] + epsilon))
            w_j = int(max(0, min(50, z_score_dist * gamma[j])))
            total_penalty += w_j
            
        if total_penalty >= 80: # Critical threshold constraint matching T_SECURE zone
            predictions.append(1) # Threat detected (triggers MFA / Block)
        else:
            predictions.append(0) # Approved access
    return np.array(predictions)


# ---------------------------------------------------------------------------------
# STEP 2: METRICS EVALUATION LOOP ACROSS SPECTRUM OF WINDOW SIZES (TABLE II + III)
# ---------------------------------------------------------------------------------
print("\n" + "-"*42 + " CLASSIFICATION PERFORMANCE " + "-"*42)
window_sizes = [10, 25, 50, 100, 250]

for N in window_sizes:
    # Slice the baseline profile matrix dynamically
    X_train_dynamic = X_clean_pool[:N]
    X_test_clean_dynamic = X_clean_pool[N:N+2000] # Test slice of 2,000 clean requests
    
    # Construct validation space: 2000 benign requests + 500 adversarial attack vectors
    X_test_dynamic = np.vstack((X_test_clean_dynamic, X_test_attack))
    y_true_dynamic = np.array([0] * len(X_test_clean_dynamic) + [1] * N_attack)
    
    # Calculate behavioral statistical invariants (Mean and Standard Deviation)
    mean_dyn = np.mean(X_train_dynamic, axis=0)
    std_dyn = np.std(X_train_dynamic, axis=0)
    
    # Execute inference loop
    y_pred_dyn = evaluate_ai_system(X_test_dynamic, mean_dyn, std_dyn)
    
    # Extract Raw Confusion Matrix values
    tn, fp, fn, tp = confusion_matrix(y_true_dynamic, y_pred_dyn).ravel()
    
    # Compute Scientific ML Metrics directly from execution predictions
    accuracy = accuracy_score(y_true_dynamic, y_pred_dyn) * 100
    precision = precision_score(y_true_dynamic, y_pred_dyn, zero_division=0) * 100
    recall = recall_score(y_true_dynamic, y_pred_dyn) * 100
    f1 = f1_score(y_true_dynamic, y_pred_dyn) * 100
    
    # Print metrics matching the structural requirements of Table 3
    print(f"Window Size N = {N:<4} | Matrix: [TP:{tp:<3} TN:{tn:<4} FP:{fp:<3} FN:{fn}]")
    print(f"                | Accuracy: {accuracy:.2f}% | Precision: {precision:.2f}% | Recall: {recall:.2f}% | F1-Score: {f1:.2f}%")
    print("-" * 112)

print("=" * 95 + "\n")
