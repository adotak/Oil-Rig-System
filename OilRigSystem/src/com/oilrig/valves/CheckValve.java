package com.oilrig.valves;

import com.oilrig.core.*;

public class CheckValve extends Valve {

    public CheckValve(ValveConfig config) {
        super(config);
    }

    @Override
    public void monitor() {
        super.monitor();
        if (currentPressure < 0 && state != ValveState.FAULT) {
            LogManager.log("Reverse flow detected in " + config.id);
            state = ValveState.FAULT;
        }
    }

    @Override
    public void open() {
        LogManager.log(config.id + " opens automatically based on flow.");
    }

    @Override
    public void close() {
        LogManager.log(config.id + " closes automatically based on flow.");
    }
}
