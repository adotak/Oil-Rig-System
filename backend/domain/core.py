import enum

class ValveState(enum.Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    FAULT = "FAULT"

class ValveType(enum.Enum):
    BUTTERFLY = "BUTTERFLY"
    GATE = "GATE"
    PRESSURE_RELIEF = "PRESSURE_RELIEF"
    CHECK = "CHECK"

class FaultType(enum.Enum):
    NO_FAULT = "NO_FAULT"
    MOTOR_FAILURE = "MOTOR_FAILURE"
    SENSOR_GLITCH = "SENSOR_GLITCH"

class TaskType(enum.Enum):
    WELD = "WELD"
    INSPECT = "INSPECT"
    REPAIR = "REPAIR"
    CALIBRATE = "CALIBRATE"

class Position3D:
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.x = x
        self.y = y
        self.z = z

class ValveConfig:
    def __init__(self, id: str, max_pressure: float, nominal_pressure: float, location: str, type: ValveType):
        self.id = id
        self.max_pressure = max_pressure
        self.nominal_pressure = nominal_pressure
        self.location = location
        self.type = type
