grades = {"Alice": 85, "Bob": 90, "Charlie": 78} #Original grades dictionary
print(grades)

grades.update({"David": 92, "Alice": 88}) #Updating grades for David and Alice
print(grades)

ex_student = "Charlie" #Storing the name of the student to be removed

student_removed = grades.pop("ex_student", "Not Found") #Attempting to remove a student using a variable
grades.pop("Charlie", "Not Found") #Removing Charlie from the grades dictionary
print(f"Removed student: {student_removed}") #This will print "Not Found" because "ex_student" is not a key in the dictionary
print(grades)

print(grades.keys(), grades.values(), grades.items()) #Printing keys, values, and items of the grades dictionary
print(grades.get("Eve", "No Record Found")) #Trying to get the grade for a student not in the dictionary

grades_copy = grades.copy() #Creating a copy of the grades dictionary
print("Grades Copy:", grades_copy)
grades.clear() #Clearing all entries in the original grades dictionary
print("Cleared Grades:", grades) #Should print an empty dictionary

print("Backup copy of grades:",grades_copy.copy()) #Printing the backup copy of grades
print("Ex Students:",ex_student)


