-- Ensure tables are cleared out before seeding data rows
TRUNCATE TABLE SUBJECTS;
DELETE FROM LOGIN_USERS;
DELETE FROM STUDENTS;

-- Insert the 10 core student tracking profiles with synchronized calculated metrics
INSERT INTO STUDENTS (NAME, MARKS, ATTENDANCE, GRADE, RESULT) VALUES ('James', 95, 90, 'A', 'Pass - Grade: A');
INSERT INTO STUDENTS (NAME, MARKS, ATTENDANCE, GRADE, RESULT) VALUES ('Michael', 85, 80, 'B', 'Pass - Grade: B');
INSERT INTO STUDENTS (NAME, MARKS, ATTENDANCE, GRADE, RESULT) VALUES ('William', 60, 78, 'C', 'Pass - Grade: C');
INSERT INTO STUDENTS (NAME, MARKS, ATTENDANCE, GRADE, RESULT) VALUES ('John', 40, 85, 'Fail', 'Fail (Low Marks)');
INSERT INTO STUDENTS (NAME, MARKS, ATTENDANCE, GRADE, RESULT) VALUES ('David', 88, 60, 'B', 'Fail (Low Attendance)');
INSERT INTO STUDENTS (NAME, MARKS, ATTENDANCE, GRADE, RESULT) VALUES ('Emily', 35, 50, 'Fail', 'Fail (Low Marks & Low Attendance)');
INSERT INTO STUDENTS (NAME, MARKS, ATTENDANCE, GRADE, RESULT) VALUES ('Sophia', 91, 95, 'A', 'Pass - Grade: A');
INSERT INTO STUDENTS (NAME, MARKS, ATTENDANCE, GRADE, RESULT) VALUES ('Daniel', 55, 76, 'C', 'Pass - Grade: C');
INSERT INTO STUDENTS (NAME, MARKS, ATTENDANCE, GRADE, RESULT) VALUES ('Olivia', 70, 45, 'C', 'Fail (Low Attendance)');
INSERT INTO STUDENTS (NAME, MARKS, ATTENDANCE, GRADE, RESULT) VALUES ('Ethan', 20, 30, 'Fail', 'Fail (Low Marks & Low Attendance)');

-- Disable variable substitution prompts for standard scripts
SET DEFINE OFF;

-- Lock the database state in permanently
COMMIT;