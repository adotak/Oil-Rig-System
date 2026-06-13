import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

interface AnalyticsPanelProps {
  token: string;
}

export const AnalyticsPanel: React.FC<AnalyticsPanelProps> = ({ token }) => {
  const [data, setData] = useState<any[]>([]);
  const [selectedEq, setSelectedEq] = useState('V-101');

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await fetch(`http://localhost:8000/api/history/${selectedEq}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) {
          const raw = await res.json();
          // Format data for Recharts
          if (Array.isArray(raw)) {
            const formatted = raw.map((r: any) => ({
              time: new Date(r.timestamp).toLocaleTimeString(),
              value: r.value
            }));
            setData(formatted);
          }
        }
      } catch (err) {
        console.error("Failed to fetch history");
      }
    };
    
    fetchHistory();
    const interval = setInterval(fetchHistory, 5000);
    return () => clearInterval(interval);
  }, [selectedEq, token]);

  return (
    <div className="chart-container">
      <div className="chart-header">
        <h3>Historical Analytics</h3>
        <select value={selectedEq} onChange={e => setSelectedEq(e.target.value)}>
          <option value="V-101">V-101 (Butterfly Valve)</option>
          <option value="P-201">P-201 (Gate Valve)</option>
          <option value="K-102">K-102 (Check Valve)</option>
          <option value="S-441">S-441 (Relief Valve)</option>
        </select>
      </div>
      <div style={{ height: '300px', width: '100%' }}>
        <ResponsiveContainer>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#2c2e3b" />
            <XAxis dataKey="time" stroke="#a0aabf" />
            <YAxis stroke="#a0aabf" />
            <Tooltip contentStyle={{ backgroundColor: '#1a1c23', border: 'none' }} />
            <Line type="monotone" dataKey="value" stroke="#3b82f6" strokeWidth={2} dot={false} isAnimationActive={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
