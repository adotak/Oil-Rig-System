package com.oilrig.valves;

import com.oilrig.core.*;

public class GateValve extends Valve {

    public GateValve(ValveConfig config) {
        super(config);
    }

    @Override
    public void monitor() {
        super.monitor();
        if (state == ValveState.OPEN && currentPressure > config.maxPressure * 0.9) {
            LogManager.log(config.id + " pressure critical: initiating emergency close");
            close();
            state = ValveState.FAULT;
        }
    }
}
