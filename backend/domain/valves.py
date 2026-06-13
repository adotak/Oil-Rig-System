import random
from .core import ValveState, ValveConfig, ValveType

class Valve:
    def __init__(self, config: ValveConfig):
        self.config = config
        self.state = ValveState.CLOSED
        self.current_pressure = config.nominal_pressure
        self.sensor_fault = False

    def open(self):
        if self.state == ValveState.FAULT:
            return
        self.state = ValveState.OPEN

    def close(self):
        if self.state == ValveState.FAULT:
            return
        self.state = ValveState.CLOSED

    def monitor(self):
        if self.state == ValveState.FAULT:
            return

        fluctuation = (random.random() * 2 - 1) * 5
        self.current_pressure += fluctuation
        if self.current_pressure < 0:
            self.current_pressure = 0

        if random.random() < 0.05:
            self.sensor_fault = True
            self.state = ValveState.FAULT

    def perform_maintenance(self):
        self.sensor_fault = False
        self.state = ValveState.CLOSED
        self.current_pressure = self.config.nominal_pressure

class ButterflyValve(Valve):
    def __init__(self, id: str, location: str):
        super().__init__(ValveConfig(id, 1500.0, 1100.0, location, ValveType.BUTTERFLY))

class GateValve(Valve):
    def __init__(self, id: str, location: str):
        super().__init__(ValveConfig(id, 2000.0, 1500.0, location, ValveType.GATE))
        
class CheckValve(Valve):
    def __init__(self, id: str, location: str):
        super().__init__(ValveConfig(id, 2500.0, 1800.0, location, ValveType.CHECK))

class PressureReliefValve(Valve):
    def __init__(self, id: str, location: str):
        super().__init__(ValveConfig(id, 3000.0, 2500.0, location, ValveType.PRESSURE_RELIEF))
