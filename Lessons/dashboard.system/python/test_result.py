import pytest
from result import calculate_result

def test_successful_pass():
    # Provide numeric marks and attendance:
    # 80 marks -> Grade B | 85 attendance -> Eligible for exam
    assert calculate_result(80, 85) == "Pass - Grade: B"

def test_failed_due_to_attendance():
    # High Marks (95) but Low Attendance (50) -> Fail (Low Attendance)
    assert calculate_result(95, 50) == "Fail (Low Attendance)"

def test_failed_due_to_grade():
    # Low Marks (40) but High Attendance (90) -> Fail (Low Marks)
    assert calculate_result(40, 90) == "Fail (Low Marks)"

def test_disqualified_input():
    # Negative marks (-5) or out-of-bounds inputs -> Invalid Input
    assert calculate_result(-5, 80) == "Invalid Input"