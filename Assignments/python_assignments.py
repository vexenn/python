# Assignment 1: HELLO WORLD & Basic User information app
# Objective: Understand Python syntax, comments, input/output, variables, constants,
# strings, type conversion, and basic data structures.

#Problem statement: You are tasked to create a simple Python application that interacts
# with the user and displays formatted information.

#Tasks:
# 1. Display a welcome message using print()
# 2. Accept the following inputs from the user:
# - Name (string)
# - Age (integer)
# - City (string)
# 3. Store the details in:
# - indiviual variables
# - a dictionary named user_details
# 4. Use type conversion to ensure age is treated as an integer
# 5. Display a greeting message using string formatting
# 6. Add comments explaining each major step

# Expected Output (Example):
# Welcome to Python Programming
# Enter your name: Rahul
# Enter your age: 22
# Enter your city: Kolkata
# User Details:
# Name: Rahul
# Age: 22
# City: Kolkata
# Hello Rahul! You are 22 years old and live in Kolkata.

# Created a welcome message and printed it

welcome_message = 'Welcome to Python Programming'
print(welcome_message)

# Defines a function to get user details (name, age, city)
# input functions allow users to type in details
# age = int converts string into integer

def get_user_details():
    name = input("Enter your name: ")
    age = int(input("Enter your age: "))
    city = input("Enter your city: ")

    return name, age, city

# Stores user inputs in individual variables

users_name, users_age, users_city = get_user_details()

# Stores details in a dictionary named user_details 

user_details = {
    'Name': users_name,
    'Age': users_age,
    'City': users_city
}

# Displays user's details

print("\nUser Details:")
print(f"Name: {user_details['Name']}")
print(f"Age: {user_details['Age']}")
print(f"City: {user_details['City']}")

# Displays a greeting message using string formatting

greeting_message = f"Hello {users_name}! You are {users_age} years old and live in {users_city}."
print(greeting_message)

# ASSIGNMENT 2: STUDENT DATA MANAGEMENT SYSTEM
# (COMPLETE PYTHON BASICS)
# Objective:
# Apply Python concepts including variables, constants, type conversion, operators, strings,
# comments, list, tuple, set, dictionary, loops, and functions.
# Problem Statement:
# A training institute wants a Python-based system to manage student academic information and
# display results.
# Tasks:
# 1. Accept student name and roll number as input
# 2. Accept 5 subject names and store them in a set (no duplicates allowed)
# 3. Accept marks for each subject using a loop and store them in a list
# 4. Convert the list of marks into a tuple
# 5. Create a dictionary to store complete student details using roll number as key
# 6. Write a function to calculate:
# o Total marks
# o Average marks
# 7. Use conditional operators to decide Pass or Fail (average &gt;= 40)
# 8. Display all student details in a structured format
# Expected Output (Example):
# Enter Student Name: Ananya
# Enter Roll Number: 102
# Enter Subjects: Maths, Science, English, History, Computer
# Enter Marks:
# Maths: 70
# Science: 65
# English: 60
# History: 55
# Computer: 75
# Student Academic Report
# Name: Ananya

# Roll Number: 102
# Subjects: {&#39;Maths&#39;, &#39;Science&#39;, &#39;English&#39;, &#39;History&#39;, &#39;Computer&#39;}
# Marks: (70, 65, 60, 55, 75)
# Total Marks: 325
# Average Marks: 65.0
# Result: Pass


# Function to get student name and roll number

def get_student_details():
    student_name = input('Enter Student Name: ')
    roll_number = int(input('Enter Roll number: '))

    return student_name, roll_number

# Function to get subjects

def get_subjects():
    subjects = set()
    print('Enter 5 subjects (separated by commas): ', end='')
    subject_input = input()
    subject_list = [subject.strip() for subject in subject_input.split(',')]
    for subject in subject_list[:5]: # Take only first 5
        subjects.add(subject)
    return subjects
    
# Function to get marks for each subject
    
def get_marks(subjects):
    marks_list = []
    print('Enter Marks:')
    for subject in subjects:
        mark = float(input(f'{subject}: '))
        marks_list.append(mark)
    return marks_list

# Function to calculate total and average marks

def calculate_results(marks_tuple):
    total_marks = sum(marks_tuple)
    average_marks = total_marks / len(marks_tuple)
    return total_marks, average_marks

# Function to determine pass or fail
def get_result(average_marks):
    return 'Pass' if average_marks >= 40 else 'Fail'

# Main program

student_name, student_roll_number = get_student_details()

# Get subjects (stored in a set)

subjects = get_subjects()

# Get marks (stored in a list)

marks_list = get_marks(subjects)

# Convert marks list to tuple

marks_tuple = tuple(marks_list)

# Calculate total and average

total_marks, average_marks = calculate_results(marks_tuple)

# Determine result

result = get_result(average_marks)

student_details = {
    student_roll_number: {

        'name': student_name,
        'roll number': student_roll_number,
        'subjects': subjects,
        'marks': marks_tuple,
        'total_marks': total_marks,
        'average_marks': average_marks,
        'result': result
}
}

# Display student academic report

print('\n--- Student Academic Report ---')
print(f'Name: {student_name}')
print(f'Roll Number: {student_roll_number}')
print(f'Subjects: {subjects}')
print(f'Marks: {marks_tuple}')
print(f'Total Marks: {int(total_marks)}')
print(f'Average Marks: {average_marks}')
print(f'Result: {result}')
