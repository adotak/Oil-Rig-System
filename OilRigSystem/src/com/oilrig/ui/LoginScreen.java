package com.oilrig.ui;

import com.oilrig.auth.LoginSystem;
import com.oilrig.core.*;
import com.oilrig.robotics.*;
import com.oilrig.valves.*;

import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

import java.util.ArrayList;
import java.util.List;

public class LoginScreen {

    private final Stage primaryStage;
    private final LoginSystem loginSystem;
    private final List<Valve> valves = new ArrayList<>();
    private final MovementArm movementArm = new MovementArm();
    private final TaskArm taskArm = new TaskArm();

    public LoginScreen(Stage stage) {
        this.primaryStage = stage;
        this.loginSystem = new LoginSystem();

        // Sample valves
        valves.add(new GateValve(new ValveConfig("GV-101", 150.0, 100.0, "Main Pipe", ValveType.GATE)));
        valves.add(new PressureReliefValve(new ValveConfig("PRV-201", 200.0, 180.0, "Tank", ValveType.PRESSURE_RELIEF)));
        valves.add(new CheckValve(new ValveConfig("CV-301", 100.0, 80.0, "Inlet", ValveType.CHECK)));
    }

    public void show() {
        Label title = new Label("Oil Rig Control - Login");
        TextField usernameField = new TextField();
        usernameField.setPromptText("Username");

        PasswordField passwordField = new PasswordField();
        passwordField.setPromptText("Password");

        Label statusLabel = new Label();
        Button loginButton = new Button("Login");

        VBox layout = new VBox(10, title, usernameField, passwordField, loginButton, statusLabel);
        layout.setAlignment(Pos.CENTER);
        layout.setStyle("-fx-background-color: #1e1e1e; -fx-padding: 30;");
        title.setStyle("-fx-font-size: 20px; -fx-text-fill: white;");
        statusLabel.setStyle("-fx-text-fill: yellow;");
        usernameField.setMaxWidth(200);
        passwordField.setMaxWidth(200);

        loginButton.setOnAction(e -> {
            String username = usernameField.getText().trim();
            String password = passwordField.getText().trim();

            String result = loginSystem.login(username, password);
            statusLabel.setText(result);

            if (result.startsWith("Login successful")) {
                showMainMenu();
            }
        });

        Scene scene = new Scene(layout, 400, 300);
        primaryStage.setTitle("Login");
        primaryStage.setScene(scene);
        primaryStage.show();
    }

    private void showMainMenu() {
        Label welcomeLabel = new Label("Main Menu");
        welcomeLabel.setStyle("-fx-font-size: 18px; -fx-text-fill: white;");

        Button valveSystemBtn = new Button("Manage Valves");
        Button roboticArmBtn = new Button("Control Robotic Arms");
        Button logoutBtn = new Button("Logout");

        VBox layout = new VBox(15, welcomeLabel, valveSystemBtn, roboticArmBtn, logoutBtn);
        layout.setAlignment(Pos.CENTER);
        layout.setStyle("-fx-background-color: #2a2a2a; -fx-padding: 30;");
        valveSystemBtn.setPrefWidth(200);
        roboticArmBtn.setPrefWidth(200);
        logoutBtn.setPrefWidth(200);

        valveSystemBtn.setOnAction(e -> showValveMenu());
        roboticArmBtn.setOnAction(e -> showRoboticMenu());
        logoutBtn.setOnAction(e -> show());

        Scene scene = new Scene(layout, 400, 300);
        primaryStage.setScene(scene);
    }

    private void showValveMenu() {
        Label title = new Label("Valve Control Menu");
        title.setStyle("-fx-font-size: 18px; -fx-text-fill: white;");

        Button monitorBtn = new Button("Monitor All Valves");
        Button openBtn = new Button("Open Valve");
        Button closeBtn = new Button("Close Valve");
        Button maintBtn = new Button("Maintenance");

        TextField valveIdInput = new TextField();
        valveIdInput.setPromptText("Enter Valve ID");

        TextArea output = new TextArea();
        output.setEditable(false);
        output.setStyle("-fx-control-inner-background: black; -fx-text-fill: lime;");
        output.setPrefHeight(150);

        Button backBtn = new Button("Back");

        monitorBtn.setOnAction(e -> {
            StringBuilder sb = new StringBuilder();
            for (Valve v : valves) {
                v.monitor();
                sb.append(v.getStatus()).append("\n");
            }
            output.setText(sb.toString());
        });

        openBtn.setOnAction(e -> {
            Valve v = findValve(valveIdInput.getText().trim());
            if (v != null) {
                v.open();
                output.setText(v.getStatus());
            } else {
                output.setText("Valve not found.");
            }
        });

        closeBtn.setOnAction(e -> {
            Valve v = findValve(valveIdInput.getText().trim());
            if (v != null) {
                v.close();
                output.setText(v.getStatus());
            } else {
                output.setText("Valve not found.");
            }
        });

        maintBtn.setOnAction(e -> {
            Valve v = findValve(valveIdInput.getText().trim());
            if (v != null) {
                v.performMaintenance();
                output.setText(v.getStatus());
            } else {
                output.setText("Valve not found.");
            }
        });

        backBtn.setOnAction(e -> showMainMenu());

        VBox layout = new VBox(10, title, monitorBtn, openBtn, closeBtn, maintBtn, valveIdInput, output, backBtn);
        layout.setAlignment(Pos.CENTER);
        layout.setStyle("-fx-background-color: #1e1e1e; -fx-padding: 20;");
        layout.setPrefWidth(500);

        Scene scene = new Scene(layout, 600, 500);
        primaryStage.setScene(scene);
    }

    private void showRoboticMenu() {
        Label title = new Label("Robotic Arm Control");
        title.setStyle("-fx-font-size: 18px; -fx-text-fill: white;");

        TextField xField = new TextField();
        TextField yField = new TextField();
        TextField zField = new TextField();
        xField.setPromptText("X");
        yField.setPromptText("Y");
        zField.setPromptText("Z");

        HBox coordBox = new HBox(10, xField, yField, zField);
        coordBox.setAlignment(Pos.CENTER);

        ChoiceBox<TaskType> taskChoice = new ChoiceBox<>();
        taskChoice.getItems().addAll(TaskType.WELD, TaskType.INSPECT, TaskType.REPAIR, TaskType.CALIBRATE);
        taskChoice.setValue(TaskType.WELD);

        TextArea output = new TextArea();
        output.setEditable(false);
        output.setStyle("-fx-control-inner-background: black; -fx-text-fill: cyan;");
        output.setPrefHeight(180);

        Button moveBtn = new Button("Move Arm");
        Button taskBtn = new Button("Execute Task");
        Button statusBtn = new Button("Status");
        Button recoverBtn = new Button("Recover");
        Button backBtn = new Button("Back");

        moveBtn.setOnAction(e -> {
            try {
                float x = Float.parseFloat(xField.getText().trim());
                float y = Float.parseFloat(yField.getText().trim());
                float z = Float.parseFloat(zField.getText().trim());
                movementArm.moveTo(new Position3D(x, y, z));
                output.setText(movementArm.getStatus());
            } catch (Exception ex) {
                output.setText("Invalid coordinates.");
            }
        });

        taskBtn.setOnAction(e -> {
            try {
                float x = Float.parseFloat(xField.getText().trim());
                float y = Float.parseFloat(yField.getText().trim());
                float z = Float.parseFloat(zField.getText().trim());
                TaskType task = taskChoice.getValue();
                taskArm.executeTask(task, new Position3D(x, y, z));
                output.setText(taskArm.getStatus());
            } catch (Exception ex) {
                output.setText("Invalid coordinates or task.");
            }
        });

        statusBtn.setOnAction(e -> {
            String status = "=== Movement Arm ===\n" + movementArm.getStatus() +
                    "\n\n=== Task Arm ===\n" + taskArm.getStatus();
            output.setText(status);
        });

        recoverBtn.setOnAction(e -> {
            movementArm.recover();
            taskArm.recover();
            output.setText("Recovery executed.\n" + movementArm.getStatus() + "\n" + taskArm.getStatus());
        });

        backBtn.setOnAction(e -> showMainMenu());

        VBox layout = new VBox(10, title, coordBox, taskChoice, moveBtn, taskBtn, statusBtn, recoverBtn, output, backBtn);
        layout.setAlignment(Pos.CENTER);
        layout.setStyle("-fx-background-color: #222; -fx-padding: 20;");

        Scene scene = new Scene(layout, 600, 500);
        primaryStage.setScene(scene);
    }

    private Valve findValve(String id) {
        for (Valve v : valves) {
            if (v.getId().equalsIgnoreCase(id)) {
                return v;
            }
        }
        return null;
    }
}