package com.oilrig.core;

public class ValveConfig {
    public String id;
    public double maxPressure;
    public double nominalPressure;
    public String location;
    public ValveType type;

    public ValveConfig(String id, double maxPressure, double nominalPressure, String location, ValveType type) {
        this.id = id;
        this.maxPressure = maxPressure;
        this.nominalPressure = nominalPressure;
        this.location = location;
        this.type = type;
    }
}
