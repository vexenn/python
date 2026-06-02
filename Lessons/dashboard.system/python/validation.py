def validate_attendance(attendance):

    if attendance is None:
        return "Invalid"

    if not isinstance(attendance, (int, float)):
        return "Invalid"

    if attendance < 0 or attendance > 100:
        return "Invalid"

    if attendance >= 75:
        return "Eligible for exam"

    return "Not eligible for exam"