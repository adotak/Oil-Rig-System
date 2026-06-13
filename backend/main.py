from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
from database import engine, Base, SessionLocal
import models, simulation, agents, auth
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

app = FastAPI(title="OilRigX AI Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
auth.seed_users()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                pass

manager = ConnectionManager()

@app.on_event("startup")
async def startup_event():
    # Start the unified simulation and broadcast loop
    asyncio.create_task(simulation_and_broadcast_loop())

async def simulation_and_broadcast_loop():
    while True:
        try:
            # 1. Step the simulation and gather special events (CV/Critical failures) and robot positions
            special_events, robot_fleet = simulation.step_simulation()
            
            # 2. Prepare payload
            db = SessionLocal()
            equipments = db.query(models.Equipment).all()
            
            data_to_send = {
                "type": "telemetry",
                "equipment": [{"id": eq.id, "name": eq.name, "status": eq.status, "health": eq.health_score} for eq in equipments],
                "robot_fleet": robot_fleet
            }
            
            agent_actions = []
            cv_alerts = []
            rca_reports = []
            
            # 3. Process special events through agents
            for event in special_events:
                if event.get("metric") == "cv_safety_violation":
                    # Direct CV alert to frontend
                    cv_alerts.append(event)
                
                # Pass to supervisor
                actions = agents.supervisor.analyze_telemetry(event)
                for action in actions:
                    if isinstance(action, dict) and action.get("type") == "rca_report":
                        rca_reports.append(action)
                    else:
                        agent_actions.append(action)
            
            # 4. Process recent standard telemetry readings
            readings = db.query(models.SensorReading).order_by(models.SensorReading.timestamp.desc()).limit(10).all()
            for r in readings:
                actions = agents.supervisor.analyze_telemetry({
                    "equipment_id": r.equipment_id,
                    "metric": r.metric,
                    "value": r.value
                })
                for action in actions:
                    if isinstance(action, dict) and action.get("type") == "rca_report":
                        rca_reports.append(action)
                    else:
                        agent_actions.append(action)
            
            if agent_actions:
                data_to_send["agent_logs"] = [a["message"] for a in agent_actions if isinstance(a, dict) and "message" in a]
            
            if cv_alerts:
                data_to_send["cv_alerts"] = cv_alerts
                
            if rca_reports:
                data_to_send["rca_reports"] = rca_reports

            await manager.broadcast(json.dumps(data_to_send))
            db.close()
        except Exception as e:
            print(f"Loop error: {e}")
            
        await asyncio.sleep(2)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/api/equipment")
def get_equipment():
    db = SessionLocal()
    eq = db.query(models.Equipment).all()
    db.close()
    return eq

from pydantic import BaseModel

class DispatchRequest(BaseModel):
    sector: str

class ESDRequest(BaseModel):
    equipment_id: str

class ChatRequest(BaseModel):
    message: str

@app.post("/api/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(auth.get_db)):
    user = auth.get_user(db, form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer", "role": user.role}

@app.post("/api/dispatch")
def api_dispatch(req: DispatchRequest, current_user: models.User = Depends(auth.get_current_user)):
    simulation.dispatch_robot(req.sector)
    return {"status": "dispatched", "message": f"Robot dispatched to {req.sector} by {current_user.username}"}

@app.post("/api/esd")
def api_esd(req: ESDRequest, current_admin: models.User = Depends(auth.get_current_admin_user)):
    simulation.inject_override({"action": "esd", "equipment_id": req.equipment_id})
    return {"status": "esd_triggered", "message": f"ESD triggered for {req.equipment_id} by {current_admin.username}"}

@app.post("/api/resolve_cv")
def api_resolve_cv(current_user: models.User = Depends(auth.get_current_user)):
    return {"status": "resolved", "message": "CV anomalies dismissed"}

@app.get("/api/history/{equipment_id}")
def get_history(equipment_id: str, db: Session = Depends(auth.get_db)):
    readings = db.query(models.SensorReading).filter(models.SensorReading.equipment_id == equipment_id).order_by(models.SensorReading.timestamp.desc()).limit(30).all()
    # Return ascending for the chart
    return list(reversed(readings))

@app.post("/api/chat")
def api_chat(req: ChatRequest, current_user: models.User = Depends(auth.get_current_user)):
    response = agents.nlp_agent.chat(req.message)
    return {"reply": response}
