package com.oilrig.core;

public class FaultUtils {
    public static String faultToString(FaultType fault) {
        switch (fault) {
            case MOTOR_FAILURE: return "Motor Failure";
            case SENSOR_GLITCH: return "Sensor Glitch";
            default: return "No Fault";
        }
    }
}
