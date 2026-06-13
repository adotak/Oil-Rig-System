from domain.valves import ButterflyValve
from domain.robotics import MovementArm
from domain.core import ValveState, Position3D, FaultType

def test_valve_lifecycle():
    valve = ButterflyValve("TEST-V", "Sector A")
    assert valve.state == ValveState.CLOSED
    valve.open()
    assert valve.state == ValveState.OPEN
    
    # Force a fault
    valve.state = ValveState.FAULT
    valve.close() # Should ignore
    assert valve.state == ValveState.FAULT
    
    valve.perform_maintenance()
    assert valve.state == ValveState.CLOSED
    assert not valve.sensor_fault

def test_robot_battery_drain():
    arm = MovementArm("AGV-TEST")
    assert arm.battery_level == 100
    assert arm.is_operational
    
    arm.move_to(Position3D(10, 10, 0))
    # It might trigger a random fault (1/20 chance) or move
    if arm.is_operational:
        assert arm.battery_level == 95
        
    arm.consume_battery(100)
    assert not arm.is_operational
    assert arm.fault_status in [FaultType.MOTOR_FAILURE, FaultType.SENSOR_GLITCH]
