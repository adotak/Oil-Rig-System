package com.oilrig.core;

import java.text.SimpleDateFormat;
import java.util.*;

public class LogManager {
    private static final List<String> logBuffer = new ArrayList<>();
    private static final int MAX_LOGS = 10;

    public static void log(String message) {
        String timestamp = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(new Date());
        String entry = "[" + timestamp + "] " + message;
        logBuffer.add(entry);
        if (logBuffer.size() > MAX_LOGS) {
            logBuffer.remove(0);
        }
        System.out.println(entry);
    }

    public static String getLogs() {
        return String.join("\n", logBuffer);
    }
}
