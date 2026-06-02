-- ====================================================================
-- Official Assignment Database Validation Script File
-- ====================================================================

-- 1. Check Duplicate Students Anomaly Query
SELECT NAME, COUNT(*) FROM STUDENTS GROUP BY NAME HAVING COUNT(*) > 1;

-- 2. Check Invalid Marks (Out of logical system boundaries)
SELECT * FROM STUDENTS WHERE MARKS < 0 OR MARKS > 100;

-- 3. Check Invalid Attendance (Out of logical percentage boundaries)
SELECT * FROM STUDENTS WHERE ATTENDANCE < 0 OR ATTENDANCE > 100;

-- 4. Check NULL Values inside Mandatory Profile Cells
SELECT * FROM STUDENTS WHERE NAME IS NULL OR MARKS IS NULL OR ATTENDANCE IS NULL;

-- 5. Check Orphan Subject Records (Relational Foreign Key Integrity Verification)
SELECT s.* FROM SUBJECTS s LEFT JOIN STUDENTS st ON s.STUDENT_ID = st.ID WHERE st.ID IS NULL;

-- 6. Check Invalid Login Usernames
SELECT * FROM LOGIN_USERS WHERE USERNAME IS NULL;

-- 7. Check Pass Students with Attendance Below 75% Anomaly Filter
SELECT * FROM STUDENTS WHERE RESULT LIKE 'Pass%' AND ATTENDANCE < 75;