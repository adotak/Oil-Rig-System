from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from database import Base
import datetime

class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String, index=True) # e.g., 'Valve', 'Pump', 'Compressor'
    status = Column(String) # 'Operational', 'Warning', 'Critical', 'Offline'
    health_score = Column(Float)
    failure_probability = Column(Float)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)

class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    equipment_id = Column(String, index=True)
    metric = Column(String) # 'pressure', 'temperature', 'vibration', 'flow_rate'
    value = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(String, primary_key=True, index=True)
    severity = Column(String) # 'P1', 'P2', 'P3', 'P4'
    description = Column(String)
    equipment_id = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    resolved = Column(Boolean, default=False)
