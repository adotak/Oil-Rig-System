package com.oilrig.valves;

import com.oilrig.core.*;

import java.util.Random;

public abstract class Valve {
    protected ValveConfig config;
    protected ValveState state;
    protected double currentPressure;
    protected boolean sensorFault;
    protected Random random;

    public Valve(ValveConfig config) {
        this.config = config;
        this.state = ValveState.CLOSED;
        this.currentPressure = 0.0;
        this.sensorFault = false;
        this.random = new Random();
    }

    public void open() {
        if (state == ValveState.FAULT) {
            LogManager.log(config.id + " cannot be opened: FAULT state");
            return;
        }
        state = ValveState.OPEN;
        LogManager.log(config.id + " opened.");
    }

    public void close() {
        if (state == ValveState.FAULT) {
            LogManager.log(config.id + " cannot be closed: FAULT state");
            return;
        }
        state = ValveState.CLOSED;
        LogManager.log(config.id + " closed.");
    }

    public void monitor() {
        if (state == ValveState.FAULT) return;

        double fluctuation = (random.nextDouble() * 2 - 1) * 5; // -5 to +5
        currentPressure += fluctuation;
        if (currentPressure < 0) currentPressure = 0;

        if (currentPressure > config.maxPressure) {
            LogManager.log("WARNING: " + config.id + " exceeds max pressure!");
        }

        if (random.nextInt(100) < 5) {
            sensorFault = true;
            state = ValveState.FAULT;
            LogManager.log("FAULT: Sensor error in " + config.id);
        }
    }

    public void performMaintenance() {
        sensorFault = false;
        state = ValveState.CLOSED;
        currentPressure = 0.0;
        LogManager.log(config.id + " maintenance complete. Reset to CLOSED.");
    }

    public String getId() {
        return config.id;
    }

    public ValveType getType() {
        return config.type;
    }

    public ValveState getState() {
        return state;
    }

    public String getStatus() {
        return config.id + " | Type: " + config.type + " | State: " + state +
                " | Pressure: " + String.format("%.2f", currentPressure) +
                " | Sensor: " + (sensorFault ? "FAULTY" : "OK");
    }
}
