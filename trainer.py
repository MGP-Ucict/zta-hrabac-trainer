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
        
        Parameters:
        - user_id (int): Unique identifier of the bank employee/user.
        - historical_data (list of lists): Feature matrices containing valid contexts.
          Expected vector format: [current_time, ip_numeric, inactivity_delta_seconds]
        """
        # Convert input data to a numpy array for scikit-learn compatibility
        X = np.array(historical_data)
        
        if X.shape[0] < 50:
            print(f"[AI-Trust Error] Insufficient data for user {user_id}. Training aborted.")
            return False

        # Initialize the Isolation Forest anomaly detection model
        # - contamination=0.05: Assumes roughly 5% anomalous boundaries in the dataset
        # - random_state=42: Forces deterministic splits for strict reproducibility
        # - n_jobs=-1: Utilizes all available CPU cores to boost background performance
        model = IsolationForest(contamination=0.05, random_state=42, n_jobs=-1)
        
        # Fit the unsupervised model to the historical normal behavior of the specific user
        model.fit(X)
        
        # Define the target filepath for saving the serialized model file (.pkl)
        model_filename = f"user_{user_id}_model.pkl"
        full_path = os.path.join(self.storage_path, model_filename)
        
        # Serialize and save the model using joblib (optimized for large numpy arrays)
        joblib.dump(model, full_path)
        print(f"[AI-Trust Background Work] Model updated and saved successfully at: {full_path}")
        return True

    def calculate_dynamic_trust_score(self, user_id, current_context_vector):
        """
        Loads the pre-trained user model from disk or cache and evaluates the 
        real-time context vector to output a standardized Trust Score (0-100).
        
        Parameters:
        - user_id (int): Unique identifier of the user making the request.
        - current_context_vector (list): [current_time, ip_numeric, inactivity_delta_seconds]
        """
        model_filename = f"user_{user_id}_model.pkl"
        full_path = os.path.join(self.storage_path, model_filename)
        
        # Fallback mechanism if the model file is missing (Cold Start / Step 1)
        if not os.path.exists(full_path):
            print(f"[AI-Trust Warning] No trained model found for user {user_id}. Falling back to Role Baseline.")
            return 100 
            
        # Fast deserialization of the trained Isolation Forest model from disk
        model = joblib.load(full_path)
        
        # Reshape the 1D context vector into a 2D array structure expected by scikit-learn
        X_current = np.array([current_context_vector])
        
        # decision_function() returns the raw anomaly score:
        # Negative values represent extreme anomalies, positive values indicate typical behavior
        raw_anomaly_score = model.decision_function(X_current)[0]
        
        # Normalize the raw score (typically between -0.5 and 0.5) to a standard 0 to 100 scale
        # Shifting and scaling guarantees compatibility with the Trust-HRABAC mathematical framework
        trust_score = int((raw_anomaly_score + 0.5) * 100)
        
        # Enforce strict ceiling and floor boundaries
        trust_score = max(0, min(100, trust_score))
        
        return trust_score


# === ASYNCHRONOUS BACKGROUND SIMULATION (CRON / WORKER SIMULATION) ===
if __name__ == "__main__":
    # Simulate an automated nightly background job (e.g., executing at 02:00 AM)
    trainer = AIModelTrainer()
    
    # Mock database pull: 50+ rows of genuine context entries for User #77
    # Feature Vector Structure: [Hour.Minutes, IP_Address_As_Long, Inactivity_Seconds]
    user_77_history = [
        [9.30, 2130706433, 120],  # 09:30 AM, Local IP, 2 mins idle
        [10.15, 2130706433, 45],   # 10:15 AM, Local IP, 45 secs idle
        [14.00, 2130706433, 3600], # 02:00 PM, Local IP, 1 hour idle
        [16.45, 2130706433, 10],   # 04:45 PM, Local IP, 10 secs idle
    ] * 15 # Multiplying array to pass the N_threshold limit for training stability
    
    # 1. Background Worker Thread: Train the profile and save the serialized .pkl artifact
    print("--- Starting Asynchronous Nightly Training Thread ---")
    trainer.train_and_save_user_model(user_id=77, historical_data=user_77_history)
    
    # 2. Real-Time Application Thread: Middleware requests instantaneous context evaluation
    print("\n--- Starting Real-Time In-Session Evaluation ---")
    
    # Scenario A: Completely normal request matching historical features
    typical_context = [11.20, 2130706433, 60]
    score_a = trainer.calculate_dynamic_trust_score(user_id=77, current_context_vector=typical_context)
    print(f"[Decision] Typical Request Context -> Calculated Trust Score: {score_a} (Expected: High / Safe)")
    
    # Scenario B: High Anomaly request mimicking Session Hijacking / Privilege Tampering
    # Action occurs at 03:15 AM from a completely unobserved IP subnet address
    anomalous_context = [3.15, 4294967295, 86400]
    score_b = trainer.calculate_dynamic_trust_score(user_id=77, current_context_vector=anomalous_context)
    print(f"[Decision] Anomalous Request Context -> Calculated Trust Score: {score_b} (Expected: Low / Triggers MFA)")
