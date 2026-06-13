package com.oilrig.valves;

import com.oilrig.core.*;

public class ButterflyValve extends Valve {
    private double position;

    public ButterflyValve(ValveConfig config) {
        super(config);
        this.position = 0.0;
    }

    public void setPosition(double pos) {
        if (state == ValveState.FAULT) return;
        position = Math.max(0.0, Math.min(1.0, pos));
        if (position > 0.05) open();
        else close();
        LogManager.log(config.id + " set to " + (int)(position * 100) + "% open.");
    }

    @Override
    public String getStatus() {
        return super.getStatus() + " | Position: " + (int)(position * 100) + "%";
    }
}
