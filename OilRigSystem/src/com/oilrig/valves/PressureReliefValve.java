package com.oilrig.valves;

import com.oilrig.core.*;

public class PressureReliefValve extends Valve {

    public PressureReliefValve(ValveConfig config) {
        super(config);
    }

    @Override
    public void monitor() {
        if (currentPressure > config.maxPressure * 0.8) {
            currentPressure *= 0.7; // relief
            LogManager.log(config.id + " relieved pressure. New: " +
                    String.format("%.2f", currentPressure));
        }
        super.monitor();
    }

    @Override
    public void open() {
        LogManager.log(config.id + " is automatic. Cannot open manually.");
    }

    @Override
    public void close() {
        LogManager.log(config.id + " is automatic. Cannot close manually.");
    }
}
