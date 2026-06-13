import { useEffect, useState, useRef } from 'react'
import './index.css'

interface Equipment {
  id: string
  name: string
  status: string
  health: number
}

interface CVAlert {
  value: string
  sector: string
}

interface RCAReport {
  target: string
  cause: string
  reason: string
  timestamp: string
}

interface Robot {
  id: string
  type: string
  status: string
  x: number
  y: number
  target_x: number
  target_y: number
}

interface TelemetryData {
  type: string
  equipment: Equipment[]
  robot_fleet?: Robot[]
  agent_logs?: string[]
  cv_alerts?: CVAlert[]
  rca_reports?: RCAReport[]
}

function App() {
  const [equipment, setEquipment] = useState<Equipment[]>([])
  const [robots, setRobots] = useState<Robot[]>([])
  const [logs, setLogs] = useState<string[]>([])
  const [cvAlerts, setCvAlerts] = useState<CVAlert[]>([])
  const [activeRca, setActiveRca] = useState<RCAReport | null>(null)
  
  const ws = useRef<WebSocket | null>(null)
  const logContainerRef = useRef<HTMLDivElement>(null)
  const cvContainerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    ws.current = new WebSocket('ws://localhost:8000/ws')

    ws.current.onmessage = (event) => {
      const data: TelemetryData = JSON.parse(event.data)
      if (data.type === 'telemetry') {
        setEquipment(data.equipment)
        if (data.robot_fleet) {
          setRobots(data.robot_fleet)
        }
        if (data.agent_logs) {
          setLogs(prev => [...prev, ...data.agent_logs!].slice(-50))
        }
        if (data.cv_alerts) {
          setCvAlerts(prev => [...prev, ...data.cv_alerts!].slice(-20))
        }
        if (data.rca_reports && data.rca_reports.length > 0) {
          // Just show the first one for the modal
          setActiveRca(data.rca_reports[0])
        }
      }
    }

    return () => {
      ws.current?.close()
    }
  }, [])

  useEffect(() => {
    if (logContainerRef.current) logContainerRef.current.scrollTop = logContainerRef.current.scrollHeight
    if (cvContainerRef.current) cvContainerRef.current.scrollTop = cvContainerRef.current.scrollHeight
  }, [logs, cvAlerts])

  const getStatusClass = (status: string) => {
    if (status === 'Operational') return 'status-ok'
    if (status === 'Warning') return 'status-warning'
    if (status === 'Critical') return 'status-critical'
    return 'status-offline'
  }

  const getLogClass = (log: string) => {
    if (log.includes('CRITICAL')) return 'log-entry critical'
    if (log.includes('ALERT') || log.includes('SAFETY VIOLATION')) return 'log-entry alert'
    return 'log-entry'
  }

  // Equipment status to Sector mapping
  const equipmentSectors: Record<string, string> = {
    'V-101': 'A',
    'P-201': 'B',
    'K-102': 'C',
    'S-441': 'D'
  }

  // Determine active alert sectors
  const activeAlertSectors: string[] = []
  equipment.forEach(eq => {
    if ((eq.status === 'Critical' || eq.status === 'Warning') && equipmentSectors[eq.id]) {
      activeAlertSectors.push(equipmentSectors[eq.id])
    }
  })
  cvAlerts.slice(-3).forEach(alert => {
    if (alert.sector && !activeAlertSectors.includes(alert.sector)) {
      activeAlertSectors.push(alert.sector)
    }
  })

  const handleDispatch = async (sector: string) => {
    await fetch('http://localhost:8000/api/dispatch', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ sector })
    })
  }

  const handleESD = async (equipment_id: string) => {
    await fetch('http://localhost:8000/api/esd', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ equipment_id })
    })
  }

  const handleResolveCV = async () => {
    await fetch('http://localhost:8000/api/resolve_cv', { method: 'POST' })
    setCvAlerts([])
  }

  return (
    <div className="app-container">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="logo">OilRigX AI</div>
        <div style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginTop: 'auto' }}>
          Autonomous Command Center<br/>
          Status: Active<br/>
          CV Subsystem: ONLINE<br/>
          Swarm Link: CONNECTED
        </div>
      </aside>

      {/* Main Content */}
      <main className="dashboard-content">
        <header style={{ marginBottom: '0.5rem' }}>
          <h1 style={{ fontSize: '1.8rem', fontWeight: '700' }}>Facility Digital Twin</h1>
          <p style={{ color: 'var(--text-secondary)' }}>Live telemetry, CV Intelligence & Robotics Swarm coordination</p>
        </header>

        {/* Equipment Grid */}
        <section className="grid-cards">
          {equipment.map(eq => (
            <div key={eq.id} className="glass-panel eq-card">
              <div className="eq-header">
                <div>
                  <div className="eq-title">{eq.id}</div>
                  <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>{eq.name}</div>
                </div>
                <span className={`status-badge ${getStatusClass(eq.status)}`}>
                  {eq.status}
                </span>
              </div>
              
              <div style={{ marginTop: '0.5rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem', fontSize: '0.875rem' }}>
                  <span>Health Score</span>
                  <span style={{ fontWeight: '600' }}>{eq.health.toFixed(1)}%</span>
                </div>
                <div className="progress-container">
                  <div 
                    className="progress-bar" 
                    style={{ 
                      width: `${Math.max(0, eq.health)}%`,
                      backgroundColor: eq.health > 80 ? 'var(--status-ok)' : eq.health > 60 ? 'var(--status-warning)' : 'var(--status-critical)'
                    }}
                  ></div>
                </div>
              </div>
            </div>
          ))}
        </section>

        {/* Command & Control Panel */}
        <section className="glass-panel" style={{ marginBottom: '1.5rem', display: 'flex', gap: '1.5rem', flexWrap: 'wrap' }}>
          <div style={{ flex: 1, minWidth: '250px' }}>
            <h2 style={{ fontSize: '1.1rem', marginBottom: '0.75rem', fontWeight: 600 }}>Manual Dispatch Override</h2>
            <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
              <button className="cmd-btn" onClick={() => handleDispatch('A')}>Sector A</button>
              <button className="cmd-btn" onClick={() => handleDispatch('B')}>Sector B</button>
              <button className="cmd-btn" onClick={() => handleDispatch('C')}>Sector C</button>
              <button className="cmd-btn" onClick={() => handleDispatch('D')}>Sector D</button>
            </div>
          </div>
          <div style={{ flex: 1, minWidth: '350px' }}>
            <h2 style={{ fontSize: '1.1rem', marginBottom: '0.75rem', color: 'var(--status-critical)', fontWeight: 600 }}>Emergency Shutdown (ESD)</h2>
            <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
              {equipment.map(eq => (
                <button key={`esd-${eq.id}`} className="cmd-btn critical-btn" onClick={() => handleESD(eq.id)}>ESD {eq.id}</button>
              ))}
            </div>
          </div>
          <div style={{ flex: 1, minWidth: '200px' }}>
            <h2 style={{ fontSize: '1.1rem', marginBottom: '0.75rem', fontWeight: 600 }}>CV Management</h2>
            <button className="cmd-btn warning-btn" onClick={handleResolveCV}>Acknowledge & Clear Alerts</button>
          </div>
        </section>

        {/* Facility Map Component */}
        <section className="glass-panel facility-map-panel">
          <h2 style={{ fontSize: '1.2rem', marginBottom: '0.25rem' }}>Autonomous Robotics Swarm Locator</h2>
          <div className="map-container">
            {/* Sectors */}
            <div className={`map-sector sector-a ${activeAlertSectors.includes('A') ? 'alert-flash' : ''}`}>
              <span className="sector-label">Sector A</span>
              <span className="sector-description">Valves & Piping Deck</span>
            </div>
            <div className={`map-sector sector-b ${activeAlertSectors.includes('B') ? 'alert-flash' : ''}`}>
              <span className="sector-label">Sector B</span>
              <span className="sector-description">Water Injection Deck</span>
            </div>
            <div className={`map-sector sector-c ${activeAlertSectors.includes('C') ? 'alert-flash' : ''}`}>
              <span className="sector-label">Sector C</span>
              <span className="sector-description">Compressor Deck</span>
            </div>
            <div className={`map-sector sector-d ${activeAlertSectors.includes('D') ? 'alert-flash' : ''}`}>
              <span className="sector-label">Sector D</span>
              <span className="sector-description">Sensor Array Deck</span>
            </div>

            {/* Static Equipment Dots mapped to locations */}
            {equipment.map(eq => {
              const coords = {
                'V-101': { x: 25, y: 25 },
                'P-201': { x: 75, y: 25 },
                'K-102': { x: 25, y: 75 },
                'S-441': { x: 75, y: 75 },
              }[eq.id] || { x: 50, y: 50 };
              
              const statusClass = eq.status === 'Critical' ? 'critical' : eq.status === 'Warning' ? 'warning' : '';
              return (
                <div key={`map-eq-${eq.id}`} className="map-equipment" style={{ left: `${coords.x}%`, top: `${coords.y}%` }}>
                  <div className={`equipment-dot ${statusClass}`}></div>
                  <span className="equipment-lbl">{eq.id}</span>
                </div>
              );
            })}

            {/* Live Robot Swarm Markers */}
            {robots.map(bot => {
              const botClass = bot.type === 'Air' ? 'air' : '';
              const statusClass = bot.status.toLowerCase();
              const icon = bot.type === 'Air' ? '🛸' : bot.id === 'Insp-Bot' ? '🤖' : '🚜';
              return (
                <div 
                  key={bot.id} 
                  className={`robot-marker ${botClass} ${statusClass}`} 
                  style={{ left: `${bot.x}%`, top: `${bot.y}%` }}
                >
                  <span className="robot-icon">{icon}</span>
                  <div className="robot-tooltip">
                    <strong>{bot.id}</strong> ({bot.type})<br/>
                    Status: {bot.status}<br/>
                    Pos: ({bot.x.toFixed(1)}, {bot.y.toFixed(1)})<br/>
                    Target: ({bot.target_x.toFixed(1)}, {bot.target_y.toFixed(1)})
                  </div>
                </div>
              );
            })}
          </div>
        </section>

        {/* Bottom Panels (Logs & CV) */}
        <section className="bottom-panels">
          <div>
            <h2 style={{ fontSize: '1.2rem', marginBottom: '1rem' }}>Multi-Agent Activity Log</h2>
            <div className="glass-panel agent-log-container" ref={logContainerRef}>
              {logs.length === 0 ? (
                <div style={{ color: 'var(--text-secondary)', textAlign: 'center', marginTop: '2rem' }}>Monitoring...</div>
              ) : (
                logs.map((log, index) => <div key={index} className={getLogClass(log)}>{log}</div>)
              )}
            </div>
          </div>
          
          <div>
            <h2 style={{ fontSize: '1.2rem', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <span style={{ color: 'var(--accent-cyan)' }}>●</span> Computer Vision Feed
            </h2>
            <div className="glass-panel cv-feed-container" ref={cvContainerRef}>
              {cvAlerts.length === 0 ? (
                <div style={{ color: 'var(--text-secondary)', textAlign: 'center', marginTop: '2rem' }}>No anomalies detected.</div>
              ) : (
                cvAlerts.map((alert, index) => (
                  <div key={index} className="cv-alert">
                    <span className="cv-icon">📷</span>
                    <div>
                      <div style={{ fontWeight: '600', color: 'var(--status-critical)' }}>{alert.value}</div>
                      <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>Location: Sector {alert.sector} | Target Locked</div>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </section>
      </main>

      {/* RCA Modal */}
      {activeRca && (
        <div className="modal-overlay">
          <div className="glass-panel rca-modal">
            <div className="rca-header">
              <h2 style={{ color: 'var(--status-critical)', margin: 0 }}>🚨 AI Root Cause Analysis</h2>
              <button className="close-btn" onClick={() => setActiveRca(null)}>&times;</button>
            </div>
            
            <p><strong>Incident Target:</strong> {activeRca.target} Critical Failure</p>
            <p style={{ marginTop: '1rem' }}>The Knowledge Graph has traced the propagation path of this failure. Traditional SCADA would only alert on {activeRca.target}, but OilRigX AI identifies the origin.</p>
            
            <div className="dependency-tree">
              {activeRca.cause} (Origin)<br/>
              &nbsp;│<br/>
              &nbsp;└──► {activeRca.target} (Failure Point)
            </div>
            
            <div style={{ background: 'rgba(255,255,255,0.05)', padding: '1rem', borderRadius: '8px', borderLeft: '3px solid var(--accent-cyan)' }}>
              <strong>AI Diagnosis:</strong><br/>
              {activeRca.reason}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default App
