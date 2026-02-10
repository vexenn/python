# Python Basics Revision Program
# Topics covered:
# syntax, input/output, variables, type conversion,
# operators, strings, comments, list, tuple, set,
# dictionary, loops, functions

print("Welcome to Python Programming")

# Input from user
name = input("Enter your name: ")
age = input("Enter your age: ")
city = input("Enter your city: ")

# Type conversion
age = int(age)

# List (mutable, ordered)
marks_list = [70, 65, 80]

# Tuple (immutable)
marks_tuple = tuple(marks_list)

# Set (unique values only)
subjects_set = {"Maths", "Science", "English", "Maths"}

# Dictionary (key-value pair)
user_details = {
    "Name": name,
    "Age": age,
    "City": city,
    "Marks": marks_tuple,
    "Subjects": subjects_set
}

# Function
def calculate_average(marks):
    total = sum(marks)
    average = total / len(marks)
    return total, average

# Function call
total_marks, avg_marks = calculate_average(marks_tuple)

# Conditional logic
if avg_marks >= 40:
    result = "Pass"
else:
    result = "Fail"

# Output using loop and formatting
print("\n--- Student Details ---")
for key, value in user_details.items():
    print(f"{key}: {value}")

print(f"\nTotal Marks: {total_marks}")
print(f"Average Marks: {avg_marks}")
print(f"Result: {result}")