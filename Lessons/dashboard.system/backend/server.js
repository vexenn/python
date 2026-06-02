const express = require("express");
const cors = require("cors");
const crypto = require("crypto");
// Notice we are destructuring { runQuery } now instead of grabbing the whole module
const { runQuery } = require("./db");

const calculateGrade = require("../javascript/grade");
const validateAttendance = require("../javascript/attendance");
const calculatePerformance = require("../javascript/performance");

const app = express();
app.use(cors());
app.use(express.json());

app.post("/student", async (req, res) => {
    try {
        const { name, marks, attendance } = req.body;

        const grade = calculateGrade(marks);
        const result = calculatePerformance(marks, attendance);

        // Define your SQL statement clearly
        const sql = "INSERT INTO STUDENTS (NAME, MARKS, ATTENDANCE, GRADE, RESULT) VALUES (:name, :marks, :attendance, :grade, :result)";
        // Define your variables array matching the order of placeholders
        const binds = [name, marks, attendance, grade, result];

        // One single line handles the entire database transaction safely!
        await runQuery(sql, binds);
        
        res.json({ message: 'Student added successfully', grade, result });

    } catch (error) {
        console.error("Error processing request:", error);
        res.status(500).json({ 
            message: 'Error adding student', 
            errormessage: error.message 
        });
    }
});

// ====================================================================
// GET /students - Fetch all student records from the database
// ====================================================================
app.get("/students", async (req, res) => {
    try {
        const sql = "SELECT ID, NAME, MARKS, ATTENDANCE, GRADE, RESULT FROM STUDENTS ORDER BY ID DESC";
        const result = await runQuery(sql);

        // Map the structural matrix rows into clean, scannable JSON objects for the frontend
        const students = result.rows.map(row => ({
            id: row[0],
            name: row[1],
            marks: row[2],
            attendance: row[3],
            grade: row[4],
            result: row[5]
        }));

        res.json(students);
    } catch (error) {
        console.error("Error fetching students:", error);
        res.status(500).json({ message: "Error fetching student directory", error: error.message });
    }
});

// ====================================================================
// GET /student/:id - Fetch a single student record by their unique ID
// ====================================================================
app.get("/student/:id", async (req, res) => {
    try {
        const { id } = req.params;
        const sql = "SELECT ID, NAME, MARKS, ATTENDANCE, GRADE, RESULT FROM STUDENTS WHERE ID = :id";
        const result = await runQuery(sql, [id]);

        if (result.rows.length === 0) {
            return res.status(404).json({ message: "Student record not found" });
        }

        const row = result.rows[0];
        const student = {
            id: row[0],
            name: row[1],
            marks: row[2],
            attendance: row[3],
            grade: row[4],
            result: row[5]
        };

        res.json(student);
    } catch (error) {
        console.error("Error fetching student by ID:", error);
        res.status(500).json({ message: "Error retrieving student details", error: error.message });
    }
});

// ====================================================================
// GET /search - Search for students by name using query parameters (?name=...)
// ====================================================================
app.get("/search", async (req, res) => {
    try {
        const { name } = req.query;
        if (!name) {
            return res.status(400).json({ message: "Query parameter 'name' is required for scanning" });
        }

        // Use UPPER and LIKE to ensure the search parameter handles mixed casing gracefully
        const sql = "SELECT ID, NAME, MARKS, ATTENDANCE, GRADE, RESULT FROM STUDENTS WHERE UPPER(NAME) LIKE :name ORDER BY NAME ASC";
        const bindParam = `%${name.toUpperCase()}%`;
        const result = await runQuery(sql, [bindParam]);

        const matches = result.rows.map(row => ({
            id: row[0],
            name: row[1],
            marks: row[2],
            attendance: row[3],
            grade: row[4],
            result: row[5]
        }));

        res.json(matches);
    } catch (error) {
        console.error("Error running student search lookup:", error);
        res.status(500).json({ message: "Error processing search parameters", error: error.message });
    }
});

// ====================================================================
// PUT /student/:id - Update student data & recompute calculated fields
// ====================================================================
app.put("/student/:id", async (req, res) => {
    try {
        const { id } = req.params;
        const { name, marks, attendance } = req.body;

        // Re-evaluate calculation dependencies using utility modules since core inputs are shifting
        const grade = calculateGrade(marks);
        const result = calculatePerformance(marks, attendance);

        const sql = `
            UPDATE STUDENTS 
            SET NAME = :name, MARKS = :marks, ATTENDANCE = :attendance, GRADE = :grade, RESULT = :result 
            WHERE ID = :id
        `;
        const binds = [name, marks, attendance, grade, result, id];
        const updateResult = await runQuery(sql, binds);

        if (updateResult.rowsAffected === 0) {
            return res.status(404).json({ message: "Student record not found for updating" });
        }

        res.json({ message: "Student updated successfully", grade, result });
    } catch (error) {
        console.error("Error updating student details:", error);
        res.status(500).json({ message: "Error modifying student record", error: error.message });
    }
});

// ====================================================================
// DELETE /student/:id - Remove a student record from the database
// ====================================================================
app.delete("/student/:id", async (req, res) => {
    try {
        const { id } = req.params;
        const sql = "DELETE FROM STUDENTS WHERE ID = :id";
        
        const deleteResult = await runQuery(sql, [id]);

        if (deleteResult.rowsAffected === 0) {
            return res.status(404).json({ message: "Student record not found for removal" });
        }

        res.json({ message: "Student record permanently removed" });
    } catch (error) {
        console.error("Error deleting student record:", error);
        res.status(500).json({ message: "Error wiping record from database", error: error.message });
    }
});

// ====================================================================
// GET /toppers - Fetch the top-performing students (Marks >= 90)
// ====================================================================
app.get("/toppers", async (req, res) => {
    try {
        // Query filters for elite tier marks sorted from highest to lowest
        const sql = "SELECT ID, NAME, MARKS, ATTENDANCE, GRADE, RESULT FROM STUDENTS WHERE MARKS >= 90 ORDER BY MARKS DESC";
        const result = await runQuery(sql);

        const toppers = result.rows.map(row => ({
            id: row[0],
            name: row[1],
            marks: row[2],
            attendance: row[3],
            grade: row[4],
            result: row[5]
        }));

        res.json(toppers);
    } catch (error) {
        console.error("Error fetching toppers list:", error);
        res.status(500).json({ message: "Error compiling honors roster", error: error.message });
    }
});

// ====================================================================
// GET /low-attendance - Fetch students at academic risk (Attendance < 75%)
// ====================================================================
app.get("/low-attendance", async (req, res) => {
    try {
        // Query tracks anyone dropping below the standard 75% graduation threshold
        const sql = "SELECT ID, NAME, MARKS, ATTENDANCE, GRADE, RESULT FROM STUDENTS WHERE ATTENDANCE < 75 ORDER BY ATTENDANCE ASC";
        const result = await runQuery(sql);

        const atRiskStudents = result.rows.map(row => ({
            id: row[0],
            name: row[1],
            marks: row[2],
            attendance: row[3],
            grade: row[4],
            result: row[5]
        }));

        res.json(atRiskStudents);
    } catch (error) {
        console.error("Error fetching low attendance logs:", error);
        res.status(500).json({ message: "Error compiling attendance risk registry", error: error.message });
    }
});

// ====================================================================
// POST /register - Securely create a new user account
// ====================================================================
app.post("/register", async (req, res) => {
    try {
        const { username, password } = req.body;
        if (!username || !password) {
            return res.status(400).json({ message: "Username and password are required" });
        }

        // Hash the plain text password using a SHA-256 cryptographic digest string
        const hashedPassword = crypto.createHash("sha256").update(password).digest("hex");

        const sql = "INSERT INTO LOGIN_USERS (USERNAME, PASSWORD) VALUES (:username, :password)";
        await runQuery(sql, [username, hashedPassword]);

        res.status(201).json({ message: "User registered successfully" });
    } catch (error) {
        console.error("Error during registration:", error);
        
        // Catch Oracle's ORA-00001 Unique Constraint Violation (Duplicate Username)
        if (error.code === "ORA-00001" || error.message.includes("ORA-00001")) {
            return res.status(400).json({ message: "Registration failed: Username is already taken" });
        }
        
        res.status(500).json({ message: "Error registering user account", error: error.message });
    }
});

// ====================================================================
// POST /login - Validate user account credentials
// ====================================================================
app.post("/login", async (req, res) => {
    try {
        const { username, password } = req.body;
        if (!username || !password) {
            return res.status(400).json({ message: "Username and password are required" });
        }

        // Hash the incoming password using the exact same algorithm to compare values
        const hashedIncomingPassword = crypto.createHash("sha256").update(password).digest("hex");

        const sql = "SELECT PASSWORD FROM LOGIN_USERS WHERE USERNAME = :username";
        const result = await runQuery(sql, [username]);

        // If no matching username row returns from Oracle
        if (result.rows.length === 0) {
            return res.status(401).json({ message: "Authentication failed: Invalid credentials" });
        }

        const storedHashedPassword = result.rows[0][0];

        // Safely check if the cryptographic strings align
        if (hashedIncomingPassword !== storedHashedPassword) {
            return res.status(401).json({ message: "Authentication failed: Invalid credentials" });
        }

        res.json({ message: "Login successful! Welcome to the dashboard" });
    } catch (error) {
        console.error("Error during login validation:", error);
        res.status(500).json({ message: "Error processing login request", error: error.message });
    }
});

// ====================================================================
// GET /analytics - Fetch statistical aggregates for dashboard charts
// ====================================================================
app.get("/analytics", async (req, res) => {
    try {
        // Compute total student metrics cleanly using conditional aggregation switches
        const sql = `
            SELECT 
                COUNT(*),
                NVL(SUM(CASE WHEN UPPER(RESULT) LIKE 'PASS%' THEN 1 ELSE 0 END), 0),
                NVL(SUM(CASE WHEN UPPER(RESULT) LIKE 'FAIL%' THEN 1 ELSE 0 END), 0),
                NVL(ROUND(AVG(MARKS), 2), 0)
            FROM STUDENTS
        `;
        const result = await runQuery(sql);
        const row = result.rows[0];

        // Format statistical findings into an easy-to-read object for frontend data graphs
        const analyticsData = {
            totalStudents: row[0],
            passCount: row[1],
            failCount: row[2],
            averageMarks: row[3]
        };

        res.json(analyticsData);
    } catch (error) {
        console.error("Error compiling dashboard analytics details:", error);
        res.status(500).json({ message: "Error parsing system metrics summary", error: error.message });
    }
});

if (require.main === module) {
    app.listen(3000, () => {
        console.log("✅ Server running on port 3000");
    });
}

module.exports = app;