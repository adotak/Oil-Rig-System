# OilRigX AI: Autonomous Digital Twin & Multi-Agent Command Center

Welcome to the **OilRigX AI Platform**. This project is a production-grade, containerized digital twin of an offshore oil rig. It features live telemetry simulation, full-stack visualization, secure role-based access, and a foundation built for advanced Artificial Intelligence (AI), Machine Learning (ML), and Natural Language Processing (NLP) pipelines.

This document serves as the **Ultimate System Blueprint**. It is intentionally exhaustive so that any developer—or AI assistant—can instantly understand the architecture, the technology stack, and the massive potential for future ML/DL integration.

---

## 🚀 The Tech Stack (Exhaustive Breakdown)

This system is built using modern, industry-standard technologies. Below is every major technology used, why it's used, and where to learn more about it.

### 1. Backend API & Simulation Layer
- **Language:** Python 3.11+
- **Framework:** [FastAPI](https://fastapi.tiangolo.com/) - A high-performance async web framework used to build the REST API and handle WebSockets.
- **Server:** [Uvicorn](https://www.uvicorn.org/) - An ASGI web server implementation for Python.
- **Real-Time Comm:** FastAPI WebSockets (`starlette.websockets`) - Pushes live telemetry (valves, pumps, robots) to the frontend at 2-second intervals.
- **Security / Auth:** 
  - `passlib[bcrypt]` (< 4.0) - For hashing passwords.
  - `python-jose` - For generating and verifying JSON Web Tokens (JWT).
  - `python-multipart` - For OAuth2 `application/x-www-form-urlencoded` login forms.

### 2. Database & ORM
- **Database:** [PostgreSQL 15](https://www.postgresql.org/) - A powerful, open-source object-relational database system. (Falls back to SQLite `oilrig.db` during local dev if Postgres is unavailable).
- **ORM:** [SQLAlchemy 2.0](https://www.sqlalchemy.org/) - The Python SQL toolkit and Object Relational Mapper. Used to map Python classes (like `Equipment`, `User`, `SensorReading`) to database tables.
- **Driver:** `psycopg2-binary` - PostgreSQL database adapter for Python.

### 3. Frontend & Visualization
- **Framework:** [React 19](https://react.dev/) with [TypeScript](https://www.typescriptlang.org/) - Provides a robust, type-safe UI component architecture.
- **Build Tool:** [Vite 8](https://vitejs.dev/) - Extremely fast frontend tooling and bundler.
- **Styling:** Vanilla CSS3 - Uses modern CSS variables, Flexbox/Grid, and glassmorphism UI design principles (blur backdrops, dark mode neon accents).
- **Charting / Analytics:** [Recharts 3](https://recharts.org/) - A composable charting library built on React components, used for rendering the live historical telemetry graphs.

### 4. Containerization & DevOps
- **Container Engine:** [Docker](https://www.docker.com/) - Packages the application and its dependencies into standardized units.
- **Orchestration:** [Docker Compose](https://docs.docker.com/compose/) (`docker-compose.yml`) - Orchestrates the multi-container setup (Postgres DB, FastAPI Backend, React Frontend).
- **Web Server:** [Nginx](https://www.nginx.com/) (Alpine) - Serves the compiled static React files in the frontend Docker container and exposes port 80.
- **Testing:** [Pytest](https://docs.pytest.org/) - The Python testing framework used to validate the domain logic (`test_domain.py`) and API routes (`test_api.py`).

---

## 🧠 Major AI / ML / DL Pipelines (Future Roadmap)

This platform is intentionally architected as a sandbox for advanced AI implementation. Here are the major AI pipelines that can (and should) be built on top of this foundation:

### 1. Predictive Maintenance (Time-Series Machine Learning)
Currently, the system simulates telemetry and triggers faults based on static logic/randomness. 
- **The Pipeline:** We can collect the historical data (`models.SensorReading`) and train an **LSTM (Long Short-Term Memory)** or **GRU** Recurrent Neural Network (RNN) using `TensorFlow` or `PyTorch`. 
- **The Goal:** The model will predict equipment failure *before* it happens by analyzing the vibration and pressure degradation curves, shifting the platform from *reactive* ESDs to *proactive* maintenance.

### 2. Computer Vision (Deep Learning)
The frontend currently shows mocked "CV Anomalies" (e.g., Missing Helmet, Oil Leak).
- **The Pipeline:** We can integrate actual RTSP camera feeds into the dashboard. Using a **YOLOv8 (You Only Look Once)** model or a **Mask R-CNN**, we can perform real-time object detection and instance segmentation on the video feed.
- **The Goal:** Automatically detect rogue sparks, un-helmeted workers, or pipeline cracks in real-time, instantly dispatching the robotic swarm to the exact coordinates of the bounding box.

### 3. Natural Language Processing (NLP) & RAG
The platform features an "ORION Supervisor" that outputs static text logs.
- **The Pipeline:** Integrate an LLM (like Llama-3, GPT-4, or Mistral) using `LangChain` or `LlamaIndex`. Implement **Retrieval-Augmented Generation (RAG)** by feeding the LLM thousands of pages of PDF Oil Rig safety manuals and the live Postgres telemetry data.
- **The Goal:** Operators can type into a chatbox: *"Why did V-101 shut down, and what does the safety manual recommend?"* The NLP agent will parse the database history, retrieve the exact manual paragraph, and reply with a conversational, cited response.

### 4. Reinforcement Learning (RL) Swarm Optimization
Currently, ground robots and drones move using basic simulated pathing.
- **The Pipeline:** Use **Stable Baselines3** or **Ray RLlib** to train a Deep Q-Network (DQN) or Proximal Policy Optimization (PPO) agent.
- **The Goal:** The robots learn to navigate the 2D facility grid autonomously, optimizing their battery life, avoiding dynamic obstacles, and coordinating with other drones to cover maximum inspection surface area.

---

## 📂 Project Structure

```text
├── backend/
│   ├── Dockerfile             # Builds the FastAPI container
│   ├── main.py                # FastAPI endpoints, WebSockets, API logic
│   ├── models.py              # SQLAlchemy schemas (Equipment, Users, History)
│   ├── database.py            # Postgres connection pooling
│   ├── auth.py                # JWT Bearer Token & Password Hashing logic
│   ├── simulation.py          # Legacy Java physics/telemetry generator
│   ├── agents.py              # Multi-Agent logic (CV, RCA, Supervisor)
│   ├── domain/                # Ported legacy Java Object-Oriented code
│   │   ├── core.py            # Enums, Position3D
│   │   ├── robotics.py        # MovementArm, TaskArm battery math
│   │   └── valves.py          # Butterfly, Gate, Check valve logic
│   └── tests/                 # Pytest integration & unit tests
├── frontend/
│   ├── Dockerfile             # Multi-stage Nginx + Node.js 20 build
│   ├── package.json           # React, Vite, Recharts dependencies
│   ├── src/
│   │   ├── main.tsx           # React DOM root
│   │   ├── App.tsx            # Main Command & Control Dashboard
│   │   ├── Login.tsx          # JWT Auth Screen
│   │   ├── AnalyticsPanel.tsx # Recharts Historical Telemetry visualization
│   │   └── index.css          # Glassmorphism & UI variables
├── docker-compose.yml         # Container Orchestration
└── .gitignore                 # Excludes cache, node_modules, venv
```

---

## ⚙️ How to Run the Platform

### Production Run (Fully Automated via Docker)
The easiest way to run the entire stack (Database + API + React UI) is via Docker Compose.
1. Ensure Docker Desktop is running.
2. Open your terminal in the root directory.
3. Run the orchestrator:
   ```bash
   docker compose up --build -d
   ```
4. Open your browser to **`http://localhost`**.
5. **Login Credentials:**
   - Admin (Full ESD Control): `admin` / `password123`
   - Viewer (Read-only): `viewer` / `password123`

### Development Run (Manual / Local)
If you wish to edit the code and see live-reloading:
1. **Backend:**
   ```bash
   cd backend
   python -m venv venv
   source venv/Scripts/activate  # (Or venv/bin/activate on Mac/Linux)
   pip install fastapi uvicorn sqlalchemy psycopg2-binary websockets pydantic requests "passlib[bcrypt]" python-jose httpx python-multipart "bcrypt<4.0"
   pytest tests/  # Run the test suite
   python -m uvicorn main:app --port 8000 --reload
   ```
2. **Frontend:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   *Access via `http://localhost:5173`.*

---
*End of Blueprint. OilRigX is primed for AI dominance.*
