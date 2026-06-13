import random
import datetime
from database import SessionLocal, engine
import models
import math

# Import legacy domain
from domain.valves import ButterflyValve, GateValve, CheckValve, PressureReliefValve
from domain.robotics import MovementArm, TaskArm
from domain.core import Position3D

# Ensure tables are created
models.Base.metadata.create_all(bind=engine)

# Use our new domain models
valve_v101 = ButterflyValve("V-101", "Sector A")
valve_p201 = GateValve("P-201", "Sector B")
valve_k102 = CheckValve("K-102", "Sector C")
valve_s441 = PressureReliefValve("S-441", "Sector D")
legacy_valves = [valve_v101, valve_p201, valve_k102, valve_s441]

arm_agv = MovementArm("AGV-1")
arm_drone = MovementArm("Drone-A")
arm_drone.position.x = 80
arm_drone.position.y = 20
arm_drone.status_text = "Patrol"
arm_insp = TaskArm("Insp-Bot")
arm_insp.position.x = 50
arm_insp.position.y = 90
legacy_arms = [arm_agv, arm_drone, arm_insp]

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
        for arm in legacy_arms:
            if arm.status_text in ["Idle", "Patrol"]:
                arm.target_pos = Position3D(target_x, target_y, 0)
                arm.status_text = "Dispatched"
                return arm.arm_id
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
                # Trigger legacy valve close
                for v in legacy_valves:
                    if v.config.id == eq_id:
                        v.close()
                eq = db.query(models.Equipment).filter(models.Equipment.id == eq_id).first()
                if eq:
                    eq.status = "Offline"
                    eq.health_score = 100.0  # Safe mode resets simulation health for this run
                    db.commit()

        # Move legacy robots
        robot_fleet_broadcast = []
        for arm in legacy_arms:
            if arm.status_text == "Dispatched" and hasattr(arm, 'target_pos'):
                arm.move_to(arm.target_pos)
                dx = arm.target_pos.x - arm.position.x
                dy = arm.target_pos.y - arm.position.y
                if math.hypot(dx, dy) < 2:
                    arm.status_text = "Inspecting"
            elif arm.status_text == "Inspecting":
                if random.random() < 0.2:
                    arm.status_text = "Idle"
            elif arm.status_text == "Patrol":
                arm.position.x = max(0, min(100, arm.position.x + random.uniform(-1, 1)))
                arm.position.y = max(0, min(100, arm.position.y + random.uniform(-1, 1)))

            # Append mapped status to broadcast
            robot_fleet_broadcast.append({
                "id": arm.arm_id,
                "type": arm.type_str,
                "status": arm.status_text,
                "x": arm.position.x,
                "y": arm.position.y,
                "battery": arm.battery_level
            })

        equipments = db.query(models.Equipment).all()
        for eq in equipments:
            if eq.status == "Offline":
                continue # Skip processing for offline equipment
                
            legacy_v = next((v for v in legacy_valves if v.config.id == eq.id), None)
            if legacy_v:
                legacy_v.monitor()
                metric = "pressure"
                value = legacy_v.current_pressure
                
                if legacy_v.state.value == "FAULT":
                    eq.health_score -= 15.0
                    eq.status = "Critical"
                    generated_events.append({"equipment_id": eq.id, "metric": "status", "value": "Critical"})
                elif legacy_v.state.value == "CLOSED":
                    eq.status = "Offline"
            else:
                # Fallback for non-mapped items
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
        
    return generated_events, robot_fleet_broadcast
