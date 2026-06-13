import random
import datetime
from database import SessionLocal, engine
import models
import math

# Ensure tables are created
models.Base.metadata.create_all(bind=engine)

# In-memory robot fleet state
robot_fleet = [
    {"id": "AGV-1", "type": "Ground", "status": "Idle", "x": 10, "y": 10, "target_x": 10, "target_y": 10},
    {"id": "Drone-A", "type": "Air", "status": "Patrol", "x": 80, "y": 20, "target_x": 80, "target_y": 20},
    {"id": "Insp-Bot", "type": "Ground", "status": "Idle", "x": 50, "y": 90, "target_x": 50, "target_y": 90},
]

# Manual override queue for frontend commands
manual_overrides = []

def inject_override(action: dict):
    manual_overrides.append(action)


# Sector map for rough coordinate translation
sectors = {
    "A": (20, 20),
    "B": (80, 20),
    "C": (20, 80),
    "D": (80, 80)
}

def seed_equipment():
    db = SessionLocal()
    if db.query(models.Equipment).count() == 0:
        equipment = [
            models.Equipment(id="V-101", name="Main Inlet Valve", type="Valve", status="Operational", health_score=98.5, failure_probability=0.01),
            models.Equipment(id="P-201", name="Water Injection Pump", type="Pump", status="Operational", health_score=95.0, failure_probability=0.05),
            models.Equipment(id="K-102", name="High-Pressure Compressor", type="Compressor", status="Operational", health_score=90.0, failure_probability=0.10),
            models.Equipment(id="S-441", name="H2S Sensor Array", type="Sensor", status="Operational", health_score=100.0, failure_probability=0.00),
        ]
        db.add_all(equipment)
        db.commit()
    db.close()

def dispatch_robot(sector):
    """External hook for the RoboticsAgent to dispatch a robot"""
    if sector in sectors:
        target_x, target_y = sectors[sector]
        # Find an idle robot
        for bot in robot_fleet:
            if bot["status"] in ["Idle", "Patrol"]:
                bot["target_x"] = target_x
                bot["target_y"] = target_y
                bot["status"] = "Dispatched"
                return bot["id"]
    return None

def step_simulation():
    seed_equipment()
    db = SessionLocal()
    generated_events = []
    
    global manual_overrides
    current_overrides = manual_overrides[:]
    manual_overrides.clear()
    
    try:
        # Apply manual ESD commands
        for override in current_overrides:
            if override.get("action") == "esd":
                eq_id = override.get("equipment_id")
                eq = db.query(models.Equipment).filter(models.Equipment.id == eq_id).first()
                if eq:
                    eq.status = "Offline"
                    eq.health_score = 100.0  # Safe mode resets simulation health for this run
                    db.commit()

        # Move robots
        for bot in robot_fleet:
            if bot["status"] == "Dispatched":
                dx = bot["target_x"] - bot["x"]
                dy = bot["target_y"] - bot["y"]
                distance = math.hypot(dx, dy)
                
                if distance < 2:
                    bot["status"] = "Inspecting"
                    bot["x"] = bot["target_x"]
                    bot["y"] = bot["target_y"]
                else:
                    speed = 4 if bot["type"] == "Air" else 2
                    bot["x"] += (dx / distance) * speed
                    bot["y"] += (dy / distance) * speed
            elif bot["status"] == "Inspecting":
                # Finish inspection randomly
                if random.random() < 0.2:
                    bot["status"] = "Idle"
            elif bot["status"] == "Patrol":
                # Wander slightly
                bot["x"] = max(0, min(100, bot["x"] + random.uniform(-1, 1)))
                bot["y"] = max(0, min(100, bot["y"] + random.uniform(-1, 1)))

        equipments = db.query(models.Equipment).all()
        for eq in equipments:
            if eq.status == "Offline":
                continue # Skip processing for offline equipment
                
            if eq.type == "Valve":
                metric = "pressure"
                value = random.uniform(1100, 1200)
            elif eq.type == "Pump":
                metric = "flow_rate"
                value = random.uniform(80, 100)
            elif eq.type == "Compressor":
                metric = "vibration"
                value = random.uniform(1.0, 3.5)
                
                if random.random() < 0.10: 
                    value += random.uniform(2.0, 5.0)
                    eq.health_score -= 5.0
                    if eq.health_score < 40:
                        eq.status = "Critical"
                        generated_events.append({"equipment_id": eq.id, "metric": "status", "value": "Critical"})
                    elif eq.health_score < 80:
                        eq.status = "Warning"
            else:
                metric = "status"
                value = 1.0

            reading = models.SensorReading(equipment_id=eq.id, metric=metric, value=value)
            db.add(reading)
        
        # Simulate Computer Vision Event
        if random.random() < 0.15: 
            violations = ["Missing Helmet", "Unauthorized Zone Access", "Oil Leak (Minor)", "Corrosion Detected"]
            generated_events.append({
                "equipment_id": "CV_CAM_01",
                "metric": "cv_safety_violation",
                "value": random.choice(violations),
                "sector": random.choice(["A", "B", "C", "D"])
            })
        
        db.commit()
    except Exception as e:
        print(f"Simulation Error: {e}")
    finally:
        db.close()
        
    return generated_events, robot_fleet
