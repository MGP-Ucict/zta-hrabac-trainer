import os
import joblib
import numpy as np
from sklearn.ensemble import IsolationForest

class AIModelTrainer:
    def __init__(self, storage_path="storage/app/ai_models/"):
        """
        Initialize trainer with storage path.
        """
        self.storage_path = storage_path
        os.makedirs(self.storage_path, exist_ok=True)

    def train_and_save_user_model(self, user_id, historical_data):
        """
        Train Isolation Forest model and save locally.
        Input matrix features layout: [time, ip_address, device_hash, inactivity]
        """
        X = np.array(historical_data)
        if X.shape[0] < 50:
            print(f"[AI-Trust Error] Insufficient data for user {user_id}. Minimum window size N=50 required.")
            return False

        # Contamination matches the institutional false-positive boundary constraints
        model = IsolationForest(contamination=0.05, random_state=42, n_jobs=-1)
        model.fit(X)

        full_path = os.path.join(self.storage_path, f"user_{user_id}_model.pkl")
        joblib.dump(model, full_path)
        print(f"[AI-Trust] Model serialized and saved at: {full_path}")
        return True

    def calculate_rules_and_penalties(self, user_id, current_context_vector, historical_data):
        """
        Evaluate real-time context vector against historical profile to dynamically recalibrate penalty weights.
        Vectors are structured as 4-dimensional spaces (n=4 metrics).
        """
        full_path = os.path.join(self.storage_path, f"user_{user_id}_model.pkl")
        
        # Empirical baseline values matching the paper specifications
        default_penalties = {
            "workingTimeScore": 30, 
            "locationScore": 30, 
            "deviceScore": 30, 
            "inactivityTimeScore": 50
        }

        if not os.path.exists(full_path):
            return default_penalties

        # Load the serialized unsupervised model configuration
        model = joblib.load(full_path)
        X_hist = np.array(historical_data)
        
        # Calculate behavioral statistical invariants
        mean_behavior = np.mean(X_hist, axis=0)
        std_behavior = np.std(X_hist, axis=0) + 1e-6 # Epsilon factor to prevent zero-division bounds
        
        # Linear deduction distance based on Z-Scores
        z_scores = np.abs((np.array(current_context_vector) - mean_behavior) / std_behavior)

        # Dynamic mapping locked to Definition 2 thresholds: min 0, max 50 points
        return {
            "workingTimeScore": int(max(0, min(50, z_scores[0] * 10))),
            "locationScore": int(max(0, min(50, z_scores[1] * 15))),
            "deviceScore": int(max(0, min(50, z_scores[2] * 12))), 
            "inactivityTimeScore": int(max(0, min(50, z_scores[3] * 8)))
        }

if __name__ == "__main__":
    trainer = AIModelTrainer()
    np.random.seed(42)
    
    # Simulating 4D historical log window data: 
    # [Working Hour (Normal), Allowed IP Address, Device Fingerprint Hash, Session Inactivity Time]
    simulated_time = np.random.normal(12.0, 1.5, 100)
    simulated_ip = [2130706433] * 100
    simulated_device = [987654321] * 100 # Simulated integer hash representing the authorized device fingerprint
    simulated_inactivity = np.random.exponential(120, 100)
    
    user_77_history = np.column_stack((simulated_time, simulated_ip, simulated_device, simulated_inactivity)).tolist()
    
    # Execute background worker training lifecycle
    trainer.train_and_save_user_model(77, user_77_history)
    
    # Test Evaluation with an incoming request context vector
    # Real-time request values: Time=13.0, IP=2130706433, Device=987654321, Inactivity=45 seconds
    current_request_context = [13.0, 2130706433, 987654321, 45]
    
    print("\n[AI-Trust Execution Output] Dynamic Penalty Configuration:")
    penalties = trainer.calculate_rules_and_penalties(77, current_request_context, user_77_history)
    print(penalties)
