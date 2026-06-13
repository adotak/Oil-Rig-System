# Oil Rig Digital Twin & Autonomous Command Center

A next-generation, web-based digital twin and autonomous command center designed for offshore oil rig management. The system simulates live telemetry from heavy machinery, analyzes it using a multi-agent AI system, and provides real-time visualization and interactive Command & Control capabilities.

## Key Features

- **Live Digital Twin Simulation:** Real-time generation of sensor data (pressure, flow rate, vibration) for industrial equipment (Valves, Pumps, Compressors).
- **Multi-Agent AI Diagnostics:** A coordinated swarm of AI agents (Supervisor, Maintenance, Emergency, Safety) that monitors telemetry, generates dynamic root-cause analysis narratives for failures, and can automatically execute Emergency Shutdowns (ESD) to prevent catastrophic cascades.
- **Autonomous Robotics Swarm:** Visual tracking and automated/manual dispatching of inspection drones and ground AGVs to different sectors of the rig in response to computer vision (CV) safety anomalies or equipment failures.
- **Interactive Command & Control:** A modern React dashboard connected via WebSockets that allows operators to manually override the AI, dispatch robots, trigger ESDs, and acknowledge safety alerts.

## Tech Stack

### Backend
- **Framework:** FastAPI (Python)
- **Data Streaming:** WebSockets for real-time telemetry broadcast
- **Database:** SQLAlchemy with SQLite (Configured to easily drop-in PostgreSQL via Docker)

### Frontend
- **Framework:** React + TypeScript (Vite)
- **Styling:** Vanilla CSS with a glassmorphism, dark-mode aesthetic

## Project Structure

```
├── backend/
│   ├── main.py          # FastAPI application, WebSocket manager, and C&C API routes
│   ├── simulation.py    # Core simulation loop, equipment state, and manual overrides
│   ├── agents.py        # Multi-Agent system (ORION Supervisor, RCA Engine, Sub-agents)
│   ├── models.py        # SQLAlchemy database models
│   └── database.py      # Database connection configuration
├── frontend/
│   ├── src/
│   │   ├── App.tsx      # Main React dashboard component (Equipment Grid, Map, C&C)
│   │   ├── index.css    # Global styling and animations
│   │   └── main.tsx     # React entry point
│   └── package.json     # Node dependencies
├── docker-compose.yml   # Optional PostgreSQL database container setup
└── README.md
```

## How to Run

### 1. Start the Backend (FastAPI)
Navigate to the `backend/` directory, activate your virtual environment, and run the server:
```bash
cd backend
python -m uvicorn main:app --port 8000
```
*The backend runs on `http://127.0.0.1:8000`.*

### 2. Start the Frontend (React)
Open a new terminal, navigate to the `frontend/` directory, install dependencies, and start the Vite dev server:
```bash
cd frontend
npm install
npm run dev
```
*The frontend runs on `http://localhost:5173`.*

### 3. Database Persistence (Optional)
The system defaults to a local SQLite database (`oilrig.db`). If you have Docker Desktop installed, you can spin up a production-grade PostgreSQL instance:
```bash
docker compose up -d
```
The FastAPI backend will automatically detect the Postgres connection and use it instead.
