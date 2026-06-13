import random
import math
from .core import Position3D, FaultType, TaskType

class BaseRobotArm:
    def __init__(self, arm_id: str, type_str: str):
        self.arm_id = arm_id
        self.type_str = type_str
        self.position = Position3D()
        self.is_operational = True
        self.fault_status = FaultType.NO_FAULT
        self.battery_level = 100
        self.fault_history = []
        self.status_text = "Idle"

    def move_to(self, new_pos: Position3D):
        raise NotImplementedError

    def consume_battery(self, amount: int):
        if not self.is_operational:
            return
        self.battery_level -= amount
        if self.battery_level <= 0:
            self.trigger_fault("Battery Depleted")

    def trigger_fault(self, cause: str):
        self.is_operational = False
        self.fault_status = random.choice([FaultType.MOTOR_FAILURE, FaultType.SENSOR_GLITCH])
        self.fault_history.append(f"{self.fault_status.value} due to {cause}")
        self.status_text = "FAULT"

    def recover(self):
        if self.fault_status != FaultType.NO_FAULT:
            self.is_operational = True
            self.fault_status = FaultType.NO_FAULT
            self.battery_level = max(self.battery_level, 30)
            self.status_text = "Idle"

class MovementArm(BaseRobotArm):
    def __init__(self, arm_id: str):
        super().__init__(arm_id, "Movement")

    def move_to(self, new_pos: Position3D):
        if not self.is_operational:
            return

        if random.randint(0, 19) == 0:
            self.trigger_fault("Random during movement")
            return

        # Simple stepping towards target
        dx = new_pos.x - self.position.x
        dy = new_pos.y - self.position.y
        dist = math.hypot(dx, dy)
        if dist > 0:
            self.position.x += (dx/dist) * 2
            self.position.y += (dy/dist) * 2

        self.consume_battery(5)

class TaskArm(BaseRobotArm):
    def __init__(self, arm_id: str):
        super().__init__(arm_id, "Task")

    def move_to(self, new_pos: Position3D):
        if not self.is_operational:
            return

        if random.randint(0, 19) == 0:
            self.trigger_fault("Random during movement")
            return

        dx = new_pos.x - self.position.x
        dy = new_pos.y - self.position.y
        dist = math.hypot(dx, dy)
        if dist > 0:
            self.position.x += (dx/dist) * 4
            self.position.y += (dy/dist) * 4

        self.consume_battery(5)

    def execute_task(self, task: TaskType, target: Position3D):
        if not self.is_operational:
            return

        self.move_to(target)
        if not self.is_operational:
            return

        self.consume_battery(10)
