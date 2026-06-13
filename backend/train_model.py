import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
from database import SessionLocal
import models

def train():
    print("Connecting to database to extract telemetry...")
    db = SessionLocal()
    
    # Query all pressure readings
    readings = db.query(models.SensorReading).filter(models.SensorReading.metric == "pressure").all()
    
    if len(readings) < 50:
        print("Not enough data to train. Generating 1000 synthetic pressure records for ML training...")
        import random, datetime
        base_time = datetime.datetime.utcnow() - datetime.timedelta(hours=24)
        for i in range(1000):
            # Normal pressure 950-1050
            val = random.uniform(950, 1050)
            # Inject 5% anomalies (pressure drop to 800-850 or spike to 1200)
            if random.random() < 0.05:
                val = random.choice([random.uniform(800, 850), random.uniform(1150, 1250)])
            new_r = models.SensorReading(equipment_id="V-101", metric="pressure", value=val, timestamp=base_time + datetime.timedelta(minutes=i))
            db.add(new_r)
        db.commit()
        readings = db.query(models.SensorReading).filter(models.SensorReading.metric == "pressure").all()

    # Extract pressure values
    data = []
    for r in readings:
        data.append({"equipment_id": r.equipment_id, "pressure": r.value, "timestamp": r.timestamp})
        
    df = pd.DataFrame(data)
    print(f"Extracted {len(df)} telemetry records.")
    
    # We will train an Isolation Forest on the pressure data
    # An Isolation Forest isolates anomalies (outliers) from the normal distribution
    X = df[['pressure']]
    
    print("Training Isolation Forest ML model...")
    # contamination = 0.05 implies we expect 5% of data to be anomalies (faults)
    model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    model.fit(X)
    
    # Save the trained model to disk
    model_path = "anomaly_model.joblib"
    joblib.dump(model, model_path)
    
    print(f"ML Model successfully trained and exported to {model_path}!")
    db.close()

if __name__ == "__main__":
    train()
