from validation import validate_attendance
import math


def calculate_grade(marks):

    if marks is None:
        return "Invalid"

    if not isinstance(marks, (int, float)):
        return "Invalid"

    if marks < 0 or marks > 100:
        return "Invalid"

    if marks >= 90:
        return "A"

    if marks >= 75:
        return "B"

    if marks >= 50:
        return "C"

    return "Fail"


def calculate_result(marks, attendance):

    grade = calculate_grade(marks)
    status = validate_attendance(attendance)

    # INVALID CASES
    if (
        grade == "Invalid"
        or status == "Invalid"
        or marks is None
        or attendance is None
        or not isinstance(marks, (int, float))
        or not isinstance(attendance, (int, float))
        or math.isnan(marks)
        or math.isnan(attendance)
    ):
        return "Invalid Input"

    # FAIL BOTH
    if grade == "Fail" and status == "Not eligible for exam":
        return "Fail (Low Marks & Low Attendance)"

    # FAIL MARKS
    if grade == "Fail":
        return "Fail (Low Marks)"

    # FAIL ATTENDANCE
    if status == "Not eligible for exam":
        return "Fail (Low Attendance)"

    # PASS CASE
    return f"Pass - Grade: {grade}"