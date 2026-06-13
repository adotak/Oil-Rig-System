package com.oilrig.robotics;

import com.oilrig.core.*;

public class MovementArm extends BaseRobotArm {

    @Override
    public void moveTo(Position3D newPos) {
        if (!isOperational) {
            LogManager.log("MovementArm: Not operational.");
            return;
        }

        if (random.nextInt(20) == 0) {
            triggerFault("Random during movement");
            return;
        }

        position = newPos;
        consumeBattery(5);
        LogManager.log("MovementArm moved to (" + position.x + ", " + position.y + ", " + position.z + ")");
    }
}
