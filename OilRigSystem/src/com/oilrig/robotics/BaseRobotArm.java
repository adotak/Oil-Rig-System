package com.oilrig.robotics;

import com.oilrig.core.*;

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Random;

public abstract class BaseRobotArm {

    protected Position3D position;
    protected boolean isOperational;
    protected FaultType faultStatus;
    protected int batteryLevel;
    protected StringBuilder faultHistory;
    protected Random random;

    public BaseRobotArm() {
        this.position = new Position3D();
        this.isOperational = true;
        this.faultStatus = FaultType.NO_FAULT;
        this.batteryLevel = 100;
        this.faultHistory = new StringBuilder();
        this.random = new Random();
    }

    public abstract void moveTo(Position3D newPos);

    protected void consumeBattery(int amount) {
        if (!isOperational) return;
        batteryLevel -= amount;
        if (batteryLevel <= 0) {
            triggerFault("Battery Depleted");
        }
    }

    protected void triggerFault(String cause) {
        isOperational = false;
        faultStatus = random.nextBoolean() ? FaultType.MOTOR_FAILURE : FaultType.SENSOR_GLITCH;
        faultHistory.append("- ").append(FaultUtils.faultToString(faultStatus)).append(" due to ").append(cause).append("\n");

        // Log fault
        LogManager.log("FAULT: " + FaultUtils.faultToString(faultStatus) +
                " at (" + position.x + ", " + position.y + ", " + position.z + ")");

        try (PrintWriter out = new PrintWriter(new FileWriter("fault_log.txt", true))) {
            out.println("[" + cause + "] " + FaultUtils.faultToString(faultStatus) +
                    " at (" + position.x + ", " + position.y + ", " + position.z + ")");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void recover() {
        if (faultStatus != FaultType.NO_FAULT) {
            isOperational = true;
            faultStatus = FaultType.NO_FAULT;
            batteryLevel = Math.max(batteryLevel, 30);
            LogManager.log("Recovery: Arm at (" + position.x + ", " + position.y + ", " + position.z + ")");
        }
    }

    public String getStatus() {
        return "--- ROBOT ARM ---\n" +
               "Position: (" + position.x + ", " + position.y + ", " + position.z + ")\n" +
               "Operational: " + (isOperational ? "Yes" : "No") + "\n" +
               "Battery: " + batteryLevel + "%\n" +
               "Fault: " + FaultUtils.faultToString(faultStatus) + "\n" +
               "History:\n" + (faultHistory.length() == 0 ? "No faults\n" : faultHistory);
    }
}
