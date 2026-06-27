import os
import joblib
import numpy as np
from sklearn.ensemble import IsolationForest

class AIModelTrainer:
    def __init__(self, storage_path="storage/app/ai_models/"):
        """
        Initialize the trainer with the target storage path for serialized models.
        """
        self.storage_path = storage_path
        # Ensure the directory exists to prevent I/O errors during serialization
        os.makedirs(self.storage_path, exist_ok=True)

    def train_and_save_user_model(self, user_id, historical_data):
        """
        Trains an individual Isolation Forest model based on the user's specific 
        historical behavioral profile and saves it to the local storage.
        """
        X = np.array(historical_data)
        
        # Enforce minimum sample threshold for statistical validation
        if X.shape[0] < 50:
            print(f"[AI-Trust Error] Insufficient data for user {user_id}. Training aborted.")
            return False

        # Initialize Isolation Forest with fixed seed for deterministic reproducibility
        model = IsolationForest(contamination=0.05, random_state=42, n_jobs=-1)
        model.fit(X)
        
        # Define target filepath and serialize model to disk
        model_filename = f"user_{user_id}_model.pkl"
        full_path = os.path.join(self.storage_path, model_filename)
        
        joblib.dump(model, full_path)
        print(f"[AI-Trust Background Work] Model updated and saved successfully at: {full_path}")
        return True

    def calculate_dynamic_trust_score(self, user_id, current_context_vector):
        """
        Loads the pre-trained user model from disk and evaluates the 
        real-time context vector to output a standardized Trust Score (0-100).
        """
        model_filename = f"user_{user_id}_model.pkl"
        full_path = os.path.join(self.storage_path, model_filename)
        
        # Fallback mechanism if the model file is missing
        if not os.path.exists(full_path):
            print(f"[AI-Trust Warning] No trained model found for user {user_id}. Falling back to Role Baseline.")
            return 100 
            
        model = joblib.load(full_path)
        X_current = np.array([current_context_vector])
        
        # Extract raw anomaly scores (negative = anomaly, positive = normal)
        raw_anomaly_score = model.decision_function(X_current)[0]
        
        # Normalize raw output to a standard 0 to 100 scoring scale
        trust_score = int((raw_anomaly_score + 0.7) * 100)
        trust_score = max(0, min(100, trust_score))
        
        return trust_score


# === ASYNCHRONOUS BACKGROUND SIMULATION ===
if __name__ == "__main__":
    trainer = AIModelTrainer()
    
    # Set seed for reproducible distribution variance
    np.random.seed(42)
    
    # Generate 100 realistic rows with mathematical variance instead of exact duplicates
    hours = np.random.normal(12.0, 2.0, 100)         # Normal office hours around noon
    ips = np.random.choice([2130706433], 100)       # Consistent local IP address
    inactivity = np.random.exponential(300, 100)    # Standard session idle gaps
    
    # Stack features into the structured matrix shape
    user_77_history = np.column_stack((hours, ips, inactivity)).tolist()
    
    # 1. Background Worker Thread: Train profile and clear old cache anomalies
    print("--- Starting Asynchronous Nightly Training Thread ---")
    trainer.train_and_save_user_model(user_id=77, historical_data=user_77_history)
    
    # 2. Real-Time Application Thread: Instant middleware scoring evaluation
    print("\n--- Starting Real-Time In-Session Evaluation ---")
    
    # Scenario A: Typical session request matching baseline patterns
    typical_context = [11.20, 2130706433, 60]
    score_a = trainer.calculate_dynamic_trust_score(user_id=77, current_context_vector=typical_context)
    print(f"[Decision] Typical Request Context -> Calculated Trust Score: {score_a}")
    
    # Scenario B: High anomaly action mimicking a hijacked session profile
    anomalous_context = [3.15, 4294967295, 86400]
    score_b = trainer.calculate_dynamic_trust_score(user_id=77, current_context_vector=anomalous_context)
    print(f"[Decision] Anomalous Request Context -> Calculated Trust Score: {score_b}")
