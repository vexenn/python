# list creation
subjects = ['Math', 'Science', 'English', 'Computer']
#printing the first and last subjects
print("First subject:", subjects[0])
print("Last subject:", subjects[-1])
#adding AI to the list
subjects.append("AI")
print(subjects)
# inserting History at index 1
subjects.insert(1, "History")
print(subjects)
# Removing science from the list and printing the length
subjects.remove("Science")
print("Total number of subjects:", len(subjects))
# Popping the last subject, storing it in a variable and printing it
removed_item = subjects.pop()
print(removed_item)
# Sorting the subjects in alphabetical order
# and reversing the list
subjects.sort()
print("Sorted list:", subjects)
subjects.reverse()
print("Reversed list:", subjects)