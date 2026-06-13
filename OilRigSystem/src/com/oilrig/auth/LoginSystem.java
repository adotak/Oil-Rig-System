package com.oilrig.auth;

import com.oilrig.core.User;
import com.oilrig.core.LogManager;

import java.io.*;
import java.util.ArrayList;
import java.util.List;

public class LoginSystem {

    private static final int MAX_USERS = 100;
    private static final String USERS_FILE = "users.dat";
    private final List<User> users;
    private String currentUserRole = "none";
    private final String adminKey = "255693";

    public LoginSystem() {
        this.users = new ArrayList<>();
        loadUsers();  // Will load users.dat or create default users
    }

    public String getCurrentUserRole() {
        return currentUserRole;
    }

    public String getAdminKey() {
        return adminKey;
    }

    public boolean addUser(String username, String password, String role) {
        if (users.size() >= MAX_USERS) return false;

        for (User user : users) {
            if (user.username.equalsIgnoreCase(username)) return false;
        }

        if (!role.equalsIgnoreCase("admin") && !role.equalsIgnoreCase("user")) return false;

        users.add(new User(username, password, role.toLowerCase()));
        saveUsers();
        return true;
    }

    public String login(String username, String password) {
        for (User user : users) {
            if (user.username.equalsIgnoreCase(username) && user.password.equals(password)) {
                currentUserRole = user.role;
                LogManager.log("Login successful. Role: " + currentUserRole);
                return "Login successful. Role: " + currentUserRole;
            }
        }
        currentUserRole = "none";
        return "Invalid username or password.";
    }

    private void loadUsers() {
        File file = new File(USERS_FILE);
        if (!file.exists()) {
            LogManager.log("users.dat not found. Generating default users.");
            // Default user creation
            users.add(new User("admin", "admin123", "admin"));
            users.add(new User("Zarrar", "2024683", "admin"));
            users.add(new User("Azlan", "2024363", "user"));
            users.add(new User("Sania", "2024562", "user"));
            users.add(new User("Maryam", "2024283", "user"));
            saveUsers();  // Create the file
            return;
        }

        try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
            String line;
            while ((line = reader.readLine()) != null && users.size() < MAX_USERS) {
                String[] parts = line.trim().split(" ");
                if (parts.length == 3) {
                    users.add(new User(parts[0], parts[1], parts[2]));
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void saveUsers() {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(USERS_FILE))) {
            for (User user : users) {
                writer.write(user.username + " " + user.password + " " + user.role);
                writer.newLine();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
