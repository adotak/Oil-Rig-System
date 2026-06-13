import random

class BaseAgent:
    def __init__(self, name):
        self.name = name

    def process_event(self, event_data):
        raise NotImplementedError

class MaintenanceAgent(BaseAgent):
    def __init__(self):
        super().__init__("Maintenance Agent")

    def process_event(self, event_data):
        if event_data.get("metric") == "vibration" and event_data.get("value", 0) > 4.0:
            return {"type": "log", "level": "alert", "message": f"[{self.name}] ALERT: High vibration detected on {event_data['equipment_id']}. Initiating predictive maintenance protocol. RUL estimated at 48 hours."}
        return None

class EmergencyAgent(BaseAgent):
    def __init__(self):
        super().__init__("Emergency Agent")

    def process_event(self, event_data):
        if event_data.get("metric") == "pressure" and event_data.get("value", 0) < 900:
             return {"type": "log", "level": "critical", "message": f"[{self.name}] CRITICAL: Pressure drop detected on {event_data['equipment_id']}. Potential leak. Initiating Emergency Shutdown (ESD) evaluation."}
        return None

class SafetyAgent(BaseAgent):
    def __init__(self):
        super().__init__("Safety Agent")

    def process_event(self, event_data):
        if event_data.get("metric") == "cv_safety_violation":
             return {"type": "log", "level": "warning", "message": f"[{self.name}] SAFETY VIOLATION: {event_data['value']} detected in Sector {event_data.get('sector', 'Unknown')}. Alerting supervisor."}
        return None

class RootCauseAnalysisEngine:
    def __init__(self):
        # Mock dependency graph: target_equipment -> (cause_equipment, reason)
        self.knowledge_graph = {
            "V-101": ("P-201", "Abnormal flow rate caused pressure surge damaging valve seal"),
            "K-102": ("SW-1", "Cooling loop failure led to overheating of thrust bearings")
        }

    def analyze_failure(self, equipment_id):
        # Dynamic narrative generation
        causes = ["P-201", "SW-1", "K-102", "V-101"]
        if equipment_id in causes:
            causes.remove(equipment_id)
        cause_id = random.choice(causes) if causes else "Unknown Origin"
        
        reasons = [
            f"Cascading vibration from {cause_id} induced micro-fractures in {equipment_id} housing.",
            f"Pressure surge upstream at {cause_id} bypassed safety regulators, overwhelming {equipment_id}.",
            f"Thermal runaway detected originating from {cause_id} cooling loop, spreading to {equipment_id}.",
            f"CV subsystem anomaly flagged structural misalignment near {cause_id}, propagating stress to {equipment_id}."
        ]
        
        return {
            "type": "rca_report",
            "target": equipment_id,
            "cause": cause_id,
            "reason": random.choice(reasons),
            "timestamp": "Real-time AI Analysis"
        }

class RoboticsAgent(BaseAgent):
    def __init__(self):
        super().__init__("Robotics Swarm Controller")
        self.equipment_sectors = {
            "V-101": "A",
            "P-201": "B",
            "K-102": "C",
            "S-441": "D"
        }

    def process_event(self, event_data):
        from simulation import dispatch_robot
        sector = event_data.get("sector")
        eq_id = event_data.get("equipment_id")
        
        # If safety violation, dispatch to sector
        if event_data.get("metric") == "cv_safety_violation" and sector:
            bot_id = dispatch_robot(sector)
            if bot_id:
                return {
                    "type": "robot_dispatch",
                    "robot_id": bot_id,
                    "sector": sector,
                    "message": f"[{self.name}] Safety violation in Sector {sector}: Dispatching {bot_id} for visual inspection."
                }
        
        # If critical status on equipment, resolve sector and dispatch
        elif event_data.get("metric") == "status" and event_data.get("value") == "Critical" and eq_id:
            sec = self.equipment_sectors.get(eq_id)
            if sec:
                bot_id = dispatch_robot(sec)
                if bot_id:
                    return {
                        "type": "robot_dispatch",
                        "robot_id": bot_id,
                        "sector": sec,
                        "message": f"[{self.name}] Equipment failure on {eq_id} in Sector {sec}: Dispatching {bot_id} for diagnosis."
                    }
        return None

class SupervisorAgent(BaseAgent):
    def __init__(self):
        super().__init__("Supervisor Agent (ORION)")
        self.sub_agents = [MaintenanceAgent(), EmergencyAgent(), SafetyAgent(), RoboticsAgent()]
        self.rca_engine = RootCauseAnalysisEngine()

    def analyze_telemetry(self, telemetry_reading):
        actions = []
        for agent in self.sub_agents:
            result = agent.process_event(telemetry_reading)
            if result:
                actions.append(result)
                
        # Trigger RCA if a critical failure occurs
        if telemetry_reading.get("metric") == "status" and telemetry_reading.get("value") == "Critical":
            eq_id = telemetry_reading.get("equipment_id")
            rca_result = self.rca_engine.analyze_failure(eq_id)
            if rca_result:
                actions.append(rca_result)
                
            # Auto-ESD Trigger
            from simulation import inject_override
            inject_override({"action": "esd", "equipment_id": eq_id})
            actions.append({
                "type": "log", 
                "level": "critical", 
                "message": f"[{self.name}] OVERRIDE: Automatically executing Emergency Shutdown (ESD) on {eq_id} to prevent catastrophic cascade."
            })
                
        return actions

supervisor = SupervisorAgent()
