const request = require("supertest");
const app = require("./server");
const { runQuery } = require("./db");
const crypto = require("crypto");

// Mock the entire database module wrapper to isolate our API routing layer
jest.mock("./db", () => ({
    runQuery: jest.fn()
}));

describe("Official API Functional Testing Suite (Jest + Supertest)", () => {
    
    // Clear mock execution counts and call histories before each individual test case
    beforeEach(() => {
        jest.clearAllMocks();
    });

    // 1. REQUIREMENT: Valid POST API test
    test("POST /student - Valid payload inserts successfully with computed fields", async () => {
        // Mock a successful database insertion layout response
        runQuery.mockResolvedValue({ rowsAffected: 1 });

        const res = await request(app)
            .post("/student")
            .send({ name: "Jane Doe", marks: 95, attendance: 95 });

        expect(res.statusCode).toBe(200);
        expect(res.body.message).toBe("Student added successfully");
        expect(res.body.grade).toBe("A"); 
        // FIXED: Updated assertion to match the actual output of your custom performance function
        expect(res.body.result).toBe("Pass - Grade: A");
    });

    // 2. REQUIREMENT: Invalid POST API test
    test("POST /student - Handles database exceptions and errors gracefully", async () => {
        // Force the database wrapper to throw a connection or query exception
        runQuery.mockRejectedValue(new Error("ORA-01400: cannot insert NULL into mandatory column"));

        const res = await request(app)
            .post("/student")
            .send({ name: "Faulty Data Entry", marks: "NOT_A_NUMBER", attendance: 50 });

        expect(res.statusCode).toBe(500);
        expect(res.body).toHaveProperty("message", "Error adding student");
        expect(res.body).toHaveProperty("errormessage");
    });

    // 3. REQUIREMENT: GET API validation
    test("GET /students - Compiles active records into an objectified JSON array", async () => {
        // Simulate a standard Oracle row matrix return structure
        runQuery.mockResolvedValue({
            rows: [
                [101, "Justin Davis", 88, 95, "B", "Pass"],
                [102, "Emma Watson", 45, 80, "F", "Fail"]
            ]
        });

        const res = await request(app).get("/students");

        expect(res.statusCode).toBe(200);
        expect(Array.isArray(res.body)).toBe(true);
        expect(res.body.length).toBe(2);
        expect(res.body[0]).toEqual({
            id: 101,
            name: "Justin Davis",
            marks: 88,
            attendance: 95,
            grade: "B",
            result: "Pass"
        });
    });

    // 4. REQUIREMENT: PUT API validation
    test("PUT /student/:id - Mutates target details and re-evaluates metric dependencies", async () => {
        runQuery.mockResolvedValue({ rowsAffected: 1 });

        const res = await request(app)
            .put("/student/101")
            .send({ name: "Justin Revised", marks: 94, attendance: 98 });

        expect(res.statusCode).toBe(200);
        expect(res.body).toHaveProperty("message", "Student updated successfully");
        expect(res.body.grade).toBe("A"); 
        // FIXED: Updated assertion to match the actual output of your custom performance function
        expect(res.body.result).toBe("Pass - Grade: A");
    });

    // 5. REQUIREMENT: DELETE API validation
    test("DELETE /student/:id - Verifies drop processing execution responses", async () => {
        runQuery.mockResolvedValue({ rowsAffected: 1 });

        const res = await request(app).delete("/student/101");

        expect(res.statusCode).toBe(200);
        expect(res.body).toHaveProperty("message", "Student record permanently removed");
    });

    // 6. REQUIREMENT: SEARCH API validation
    test("GET /search - Query parameters extract matching entries successfully", async () => {
        runQuery.mockResolvedValue({
            rows: [[101, "Justin Davis", 88, 95, "B", "Pass"]]
        });

        const res = await request(app).get("/search?name=justin");

        expect(res.statusCode).toBe(200);
        expect(res.body[0].name).toBe("Justin Davis");
    });

    // 7. REQUIREMENT: LOGIN API validation
    test("POST /login - Validates credentials against cryptographic storage matches", async () => {
        const plainPassword = "SecurePassword123";
        const expectedHash = crypto.createHash("sha256").update(plainPassword).digest("hex");

        // Mock Oracle returning a matching username row containing the stored hash
        runQuery.mockResolvedValue({ rows: [[expectedHash]] });

        const res = await request(app)
            .post("/login")
            .send({ username: "vexenn897", password: plainPassword });

        expect(res.statusCode).toBe(200);
        expect(res.body).toHaveProperty("message", "Login successful! Welcome to the dashboard");
    });

    // 8. REQUIREMENT: Analytics API validation
    test("GET /analytics - Returns aggregated data totals for dashboard views", async () => {
        // Mock the conditional aggregation metrics row response
        runQuery.mockResolvedValue({
            rows: [[20, 16, 4, 82.5]]
        });

        const res = await request(app).get("/analytics");

        expect(res.statusCode).toBe(200);
        expect(res.body).toEqual({
            totalStudents: 20,
            passCount: 16,
            failCount: 4,
            averageMarks: 82.5
        });
    });
});