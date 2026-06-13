package com.oilrig.robotics;

import com.oilrig.core.*;

public class TaskArm extends BaseRobotArm {

    @Override
    public void moveTo(Position3D newPos) {
        if (!isOperational) {
            LogManager.log("TaskArm: Not operational.");
            return;
        }

        if (random.nextInt(20) == 0) {
            triggerFault("Random during movement");
            return;
        }

        position = newPos;
        consumeBattery(5);
        LogManager.log("TaskArm moved to (" + position.x + ", " + position.y + ", " + position.z + ")");
    }

    public void executeTask(TaskType task, Position3D target) {
        if (!isOperational) {
            LogManager.log("TaskArm: Cannot execute task — not operational.");
            return;
        }

        moveTo(target);
        if (!isOperational) return;

        String taskName = switch (task) {
            case WELD -> "Weld";
            case INSPECT -> "Inspect";
            case REPAIR -> "Repair";
            case CALIBRATE -> "Calibrate";
            default -> "Unknown";
        };

        consumeBattery(10);
        LogManager.log("TaskArm executed " + taskName + " at (" + target.x + ", " + target.y + ", " + target.z + ")");
    }
}
