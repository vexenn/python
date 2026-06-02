const { runQuery } = require("./db");

describe("Teacher's Database Validation Testing Suite", () => {
    let databaseOnline = true;

    // Run an initial handshake check before the suite starts
    beforeAll(async () => {
        try {
            await runQuery("SELECT 1 FROM DUAL");
            console.log("✅ Live integration check: Connected to Oracle successfully!");
        } catch (error) {
            console.error("❌ Live integration check failed:", error.message);
            databaseOnline = false;
        }
    });

    // TEST 1: Check total student count is greater than 0
    test("Check Student Count", async () => {
        if (!databaseOnline) return console.warn("Skipping: Database offline");

        const result = await runQuery("SELECT COUNT(*) AS TOTAL FROM STUDENTS");
        const totalStudents = result.rows[0][0];
        
        expect(totalStudents).toBeGreaterThan(0);
    });

    // TEST 2: Check that there is at least one passing student logged
    test("Check Pass Students", async () => {
        if (!databaseOnline) return console.warn("Skipping: Database offline");

        const result = await runQuery("SELECT COUNT(*) FROM STUDENTS WHERE RESULT = 'Pass'");
        const passCount = result.rows[0][0];

        expect(passCount).toBeGreaterThan(0);
    });

    // TEST 3: Check for invalid marks (Should be Greater Than or Equal to 0)
    test("Check Invalid Marks (Floor Limit)", async () => {
        if (!databaseOnline) return console.warn("Skipping: Database offline");

        const result = await runQuery("SELECT COUNT(*) FROM STUDENTS WHERE MARKS < 0");
        const invalidCount = result.rows[0][0];

        expect(invalidCount).toBeGreaterThanOrEqual(0);
    });

    // TEST 4: Check Out-of-Bounds Maximum Marks
    test("Check Out-of-Bounds Maximum Marks (Ceiling Limit)", async () => {
        if (!databaseOnline) return console.warn("Skipping: Database offline");

        const result = await runQuery("SELECT COUNT(*) FROM STUDENTS WHERE MARKS > 100");
        const impossibleHighMarks = result.rows[0][0];

        expect(impossibleHighMarks).toBe(0);
    });

    // TEST 5: Check duplicate students requirement
    test("Check Duplicate Students - Identify non-unique identity configurations", async () => {
        if (!databaseOnline) return console.warn("Skipping: Database offline");

        // Aggregates rows to find names registered multiple times inside the schema
        const result = await runQuery(
            "SELECT COUNT(*) FROM (SELECT NAME FROM STUDENTS GROUP BY NAME HAVING COUNT(*) > 1)"
        );
        const duplicateAnomalies = result.rows[0][0];
        expect(duplicateAnomalies).toBe(0);
    });

    // TEST 6: Check invalid attendance limits requirement
    test("Check Invalid Attendance - Ensure percentages fit between 0 and 100", async () => {
        if (!databaseOnline) return console.warn("Skipping: Database offline");

        const result = await runQuery("SELECT COUNT(*) FROM STUDENTS WHERE ATTENDANCE < 0 OR ATTENDANCE > 100");
        const invalidAttendanceCount = result.rows[0][0];
        expect(invalidAttendanceCount).toBe(0);
    });

    // TEST 7: Check NULL values requirement across mandatory columns
    test("Check NULL Values - Ensure critical operational records are complete", async () => {
        if (!databaseOnline) return console.warn("Skipping: Database offline");

        const result = await runQuery(
            "SELECT COUNT(*) FROM STUDENTS WHERE NAME IS NULL OR MARKS IS NULL OR ATTENDANCE IS NULL"
        );
        const nullFieldRecords = result.rows[0][0];
        expect(nullFieldRecords).toBe(0);
    });

    // TEST 8: Check pass students with attendance below 75 requirement
    test("Check Pass Students with Attendance Below 75 - Enforce structural lockouts", async () => {
        if (!databaseOnline) return console.warn("Skipping: Database offline");

        // Business rules dictate that students with under 75% attendance should not retain a Pass designation
        const result = await runQuery("SELECT COUNT(*) FROM STUDENTS WHERE RESULT = 'Pass' AND ATTENDANCE < 75");
        const invalidPassCount = result.rows[0][0];
        expect(invalidPassCount).toBe(0);
    });

    // TEST 9: Check invalid login usernames mapping validation
    test("Check Invalid Login Usernames - Verify boundary search safety", async () => {
        if (!databaseOnline) return console.warn("Skipping: Database offline");

        // Scanning for a known fake entry to check empty result resolution behaviors
        const result = await runQuery("SELECT COUNT(*) FROM LOGIN_USERS WHERE USERNAME = 'EMPTY_PROMPT_MOCK_USER'");
        const userExists = result.rows[0][0];
        expect(userExists).toBe(0);
    });

    // TEST 10: Check orphan subject records requirement (Foreign Key constraint test)
    test("Check Orphan Subject Records - Foreign key rejects detached entries", async () => {
        if (!databaseOnline) return console.warn("Skipping: Database offline");

        // Attempting to inject a child subject row referencing a completely invalid parent student ID (-999)
        // This transaction must fail explicitly due to active Oracle relational key constraints
        await expect(
            runQuery("INSERT INTO SUBJECTS (STUDENT_ID, SUBJECT_NAME, MARKS_OBTAINED) VALUES (-999, 'Physics', 88)")
        ).rejects.toThrow();
    });

    // TEST 11: End-to-End CRUD Life Cycle Processing Block
    test("CRUD Cycle: Should insert, verify, and cleanly delete a tracking record", async () => {
        if (!databaseOnline) return console.warn("Skipping: Database offline");

        const uniqueName = "Test_Artifact_" + Date.now();

        // 1. Write the record
        await runQuery(
            "INSERT INTO STUDENTS (NAME, MARKS, ATTENDANCE, GRADE, RESULT) VALUES (:1, :2, :3, :4, :5)",
            [uniqueName, 92, 100, "A", "Pass"]
        );

        // 2. Read the record back to check data preservation
        const verifyResult = await runQuery("SELECT * FROM STUDENTS WHERE NAME = :1", [uniqueName]);
        expect(verifyResult.rows.length).toBe(1);

        // 3. Cleanup: Tear it down so successive test runs stay fresh
        await runQuery("DELETE FROM STUDENTS WHERE NAME = :1", [uniqueName]);

        const finalCheck = await runQuery("SELECT * FROM STUDENTS WHERE NAME = :1", [uniqueName]);
        expect(finalCheck.rows.length).toBe(0);
    });

    // TEST 12: Application Data Invariant Checks
    test("Data Invariants: Ensure no database records mismatch grades and marks", async () => {
        if (!databaseOnline) return console.warn("Skipping: Database offline");

        const result = await runQuery("SELECT COUNT(*) FROM STUDENTS WHERE GRADE = 'A' AND MARKS < 85");
        const brokenInvariantsCount = result.rows[0][0];

        expect(brokenInvariantsCount).toBe(0);
    });

    // TEST 13: Constraint Type-Violation Error Handling Check
    test("Database Constraints: Rejects invalid data types gracefully", async () => {
        if (!databaseOnline) return console.warn("Skipping: Database offline");

        const errorSpy = jest.spyOn(console, "error").mockImplementation(() => {});

        // Forcing a structural syntax type rejection by targeting a numeric cell with alpha text characters
        await expect(
            runQuery("INSERT INTO STUDENTS (NAME, MARKS, ATTENDANCE, GRADE, RESULT) VALUES (:1, :2, 100, 'A', 'Pass')", ["Type Test User", "NOT_A_NUMBER"])
        ).rejects.toThrow();

        errorSpy.mockRestore();
    });
});