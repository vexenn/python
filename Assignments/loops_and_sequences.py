cities = ['Los Angeles', 'London', 'Tokyo']
cities[0] # Los Angeles
print(cities[0])
cities[-1] # Tokyo
print(cities[-1])

developer = 'Jessica'
print(list(developer))
# Result: ['J', 'e', 's', 's', 'i', 'c', 'a']

numbers = [1, 2, 3, 4, 5]
len(numbers) # 5
print(len(numbers))

programming_languages = ['Python', 'Java', 'C++', 'Rust']
# programming_languages[0] = 'JavaScript'
print(programming_languages) # ['JavaScript', 'Java', 'C++', 'Rust']

# Index Out of Range Error: If you pass in an index (either positive or negative)
# That is out of bounds for the list, then you will receive an IndexError

programming_languages = ['Python', 'Java', 'C++', 'Rust']
# programming_languages[10] = 'JavaScript'

# """
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# IndexError: list assignment index out of range
# """

developer = ['Jane Doe', 23, 'Python Developer']
del developer[1]
print(developer) # ['Jane Doe', 'Python Developer']

# Checking if an Element Exists in a List: The in keyword can be used to check if an
# element exists in a list:

programming_languages = ['Python', 'Java', 'C++', 'Rust']

'Rust' in programming_languages # True
'JavaScript' in programming_languages # False

# Nesting Lists: Lists can be nested inside other lists:

developer = ['Alice', 25, ['Python', 'Rust', 'C++']]

#  To access the nested list, you will need to access it using index 2 since lists
#  are zero-based indexed.

developer = ['Alice', 25, ['Pythin', 'Rust', 'C++']]
developer[2] # ['Python', 'Rust', 'C++']

# To further access the second language from that nested list,
#  you will need to access it using index 1

developer = ['Alice', 25, ['Python', 'Rust', 'C++']]
developer[2][1] # Rust

# Unpacking Tuples: Items can be unpacked from a tuple like this:

developer = ('Alice', 34, 'Rust Developer')
name, age, job = developer

#  If you need to collect any remaining elements from a tuple,
#  you can use the asterisk * operator like this:

developer = ('Alice', 34, 'Rust Developer')
name, *rest = developer

#  Slicing Tuples: Slicing can be used to extract a portion of a tuple.
#  For example, the items pie and cookies can be sliced into a separate tuple:

desserts = ('cake', 'pie', 'cookies', 'ice cream')
desserts[1:3] # ('pie', 'cookies')

# Removing items from Tuples: Removing an item from a tuple will raise a
# TypeError as tuples are immutable:

developer = ('Jane Doe', 23, 'Python Developer')
# del developer[1]

# """
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# TypeError: "tuple" object doesn't support item deletion
# """

# When to use a Tuple vs a List?: If you need a dynamic collection of
# elements where you can add, remove, and update elements, then you should use a list.
# If you know what you are working with a fixed and immutable collection of data,
# then you should use a tuple.

# Common Tuple Methods
# count(): Used to determine how many times an item appears in a tuple.
# For example, you can check how many times the language 'Rust' appears in the tuple:

programming_languages = ('Rust', 'Java', 'Python', 'C++', 'Rust')
programming_languages.count('Rust') # 2

# if the specified item in the count() method is not present at all in the tuple,
#  then the return value will be 0:

programming_languages = ('Rust', 'Java', 'Python', 'C++', 'Rust')
programming_languages.count('JavaScript') # 0

# If no arguments are passed to the count() method, then Pythod will return a
# TypeError.

# index(): Used to find the index where a particular item is present in the tuple.
# Here is an example of using the index() method to find the index for the
# language 'Java':

programming_languages = ('Rust', 'Java', 'Python', 'C++', 'Rust')
programming_languages.index('Java') # 1

# If the specified item cannot be found, then Python will return a ValueError.
# You can pass an optional start index to the index() method to specify where
# to start searching for the item in the tuple:

programming_languages = ('Rust', 'Java', 'Python', 'C++', 'Rust', 'Python')
programming_languages.index('Python', 3) # 5

# You can also pass in an optional end index to the index() method to specify
# where to stop searching for the item in the tuple:

programming_languages = ('Rust', 'Java', 'Python', 'C++', 'Rust', 'Python')
programming_languages.index('Python', 2, 5) # 2

# sorted(): Used to sort the elements in any iterable and return a new sorted
# list. Here is an example of creating an new list of numbers using the sorted()
# function:

numbers = (13, 2, 78, 3, 45, 67, 18, 7)
sorted(numbers) # [2, 3, 7, 13, 18, 45, 67, 78]

# Modifying Sorting Behavior: You can customize the sorting behavior for an
# iterable using the optional reverse and key arguments. Here is an example of
# using the key arguments to sort items in a tuple by length:

programming_languages = ('Rust', 'Java', 'Python', 'C++', 'Rust', 'Python')
sorted(programming_languages, key=len)

# Result
# ['C++', 'Rust', 'Java', 'Rust', 'Python', 'Python']

# You can create a new list of values in reverse order, using the reverse
# argument like this:

programming_languages = ('Rust', 'Java', 'Python', 'C++', 'Rust', 'Python')
print(sorted(programming_languages, reverse=True))

# Result
# ['Rust', 'Rust', 'Python', 'Python', 'Java', 'C++']

# Loops in Python
# Definition: Loops are used to repeat a block of code for a set number of times.
# for loop: Used to iterate over a sequence (like a list, tuple or string) and
# execute a block of code for each item in that sequence. Here is an example of
# using a for loop to iterate through a list and print each language to the console:

programming_languages = ['Rust', 'Java', 'Python', 'C++']

for language in programming_languages:
    print(language)

# """
# Result 

# Rust
# Java
# Python
# C++
# """

# Here is an example of using a for loop to loop through the string code and
# print out each character:

for char in 'code':
    print(char)

# """
# Result 

# c
# o
# d
# e
# """

# for loops can be nested. Here is an example of using a nested for loop:

categories = ['Fruit', 'Vegetable']
foods = ['Apple', 'Carrot', 'Banana']

for category in categories:
    for food in foods:
        print(category, food)

# """
# Result

# Fruit Apple
# Fruit Carrot
# Fruit Banana
# Vegetable Apple
# Vegetable Carrot
# Vegetable Banana
# """

# while loop: Repeats a block of code until the condition is False. Here is an
# example of using a while loop for a guessing game:

secret_number = 3
guess = 0

while guess != secret_number:
    guess = int(input('Guess the number (1-5): '))
    if guess != secret_number:
        print('Wrong! Try again.')

print('You got it!')

# """
# Result

# Guess the number (1-5): 2
# Wrong! Try again.
# Guess the number (1-5): 1
# Wrong! Try again.
# Guess the number (1-5): 3
# You got it!
# """

# break and continue statements: Used in loops to modify the execution of a loop.
# The break statement is used to exit the loop immediately when a certain condition
# is met. Here is an example of using the break statement for a list of
# developer_names:

developer_names = ['Jess', 'Naomi', 'Tom']

for developer in developer_names:
    if developer == 'Naomi':
        break
    print(developer)

# The continue statement is used to skip that current iteration and move onto
# the next iteration of the loop. Here is an example to use the continue statement
# instead of a break statement:

developer_names = ['Jess', 'Naomi', 'Tom']

for developer in developer_names:
    if developer == 'Naomi':
        continue
    print(developer)

# Both for and while loops can be combined with an else clause, which is executed
# only when the loop was not terminated by break:

words = ['sky', 'apple', 'rhythm', 'fly', 'orange']

for word in words:
    for letter in word:
        if letter.lower() in 'aeiou':
            print(f"'{word}' contains the vowel '{letter}'")
            break
    else:
        print(f"'{word}' has no vowels")

# Ranges and Their Use in Loops
# The range() function: Used to generate a sequence of integers.

# range(start,stop, step)

# The required stop argument is an integer(non-inclusive) that represents the
# end point for the sequence of numbers being generated. Here is an example of
# using the range() function:

for num in range(3):
    print(num)

# If a start argument is not specified, then the default will be 0.
# By default the sequence of integers will increment by 1. You can use the optional
# step argument to change the default increment value. Here is an example of
# generating a sequence of even integers from 2 up to but not including 11.
# (i.e., includes 10)

for num in range(2, 11, 2):
    print(num)

# if you don't provide any arguments to the range() function, then you will get a
# TypeError.
# The range() function only accepts integers for arguments and not floats.
# Using floats will also result in a TypeError:

# ERROR!
# Traceback (most recent call last):
#   File "<main.py>", line 1, in <module>
# TypeError: 'float' object cannot be interpreted as an integer

# You can use a negative integer for the step argument to generate a sequence
# of integers in decrementing order:

for num in range(40, 0, -10):
    print(num)

# The range() function can also be used to create a list of integers by using it
# with the list constructor. The list constructor is used to convert an iterable
# into a list. Here is an example of generating a list of even integers
# between 2 and 10 inclusive:

numbers = list(range(2, 11, 2))
print(numbers) # [2, 4, 6, 8 , 10]

# If you don't provide any arguments to the range() function, then you will get a
# TypeError.
# The range() function only accepts integers for arguments and not floats.
# Using floats will also result in a TypeError:

# ERROR!
# Traceback (most recent call last):
#   File "<main.py>", line 1, in <module>
# TypeError: 'float' object cannot be interpreted as an integer

# You can use a negative integer for the step argument to generate a sequence of
# integers in decrementing order:

for num in range(40, 0, -10):
    print(num)

# The range() function can also be used to create a list of integers by using it
# with the list constructor. The list constructor is used to convert an iterable
# into a list. Here is an example of generating a list of even integers between
# 2 and 10 inclusive:

numbers = list(range(2, 11, 2))
print(numbers) # [2, 4, 6, 8, 10]

# enumerate() and zip() functions in Python
# enumerate(): used to iterate over a sequence and keep track of the index for
# each item in that sequence. The enumerate() function takes an iterable as an
# argument and returns an enumerate object that consists of the index and value
# of each item in the iterable.

languages = ['Spanish', 'English', 'Russion', 'Chinese']

for index, language in enumerate(languages):
    print(f'Index {index} and language {language}')

# Result
# Index 0 and language Spanish
# Index 1 and language English
# Index 2 and language Russion
# Index 3 and language Chinese

# The enumerate() function can also be used outside of a for loop:

languages = ['Spanish', 'English', 'Russian', 'Chinese']

print(list(enumerate(languages)))

# Result:
# [(0, 'Spanish'), (1, 'English'), (2, 'Russian'), (3, 'Chinese')]

# The enumerate() function also accepts an optional start argument that
# specifies the starting value for the count. If this argument is omitted, then the 
# count will begin at 0.

# zip(): Used to iterate over multiple iterables in parallel. Here's an example
# using the zip() function to iterate over developers and ids:

developers = ['Naomi', 'Dario', 'Jessica', 'Tom']
ids = [1, 2, 3, 4]

for name, id in zip(developers, ids):
    print(f'Name: {name}')
    print(f'ID: {id}')

# Result
# Name: Naomi
# ID: 1
# Name: Dario
# ID: 2
# Name: Jessica
# ID: 3
# Name: Tom
# ID: 4

# List comprehensions in Python
# Definition: List comprehension allows you to create a new list in a single line
# by combining the loop and the condition directly within square brackets. This
# makes the code shorter and often easier to read.

even_numbers = [num for num in range(21) if num % 2 == 0]
print(even_numbers)

# Iterable methods
# filter(): Used to filter elements from an iterable based on a condition.
# It returns an iterator that contains only the elements that satisfy the condition.
# Here is an example of creating a new list of just words longer than four characters:

words = ['tree', 'sky', 'mountain', 'river', 'cloud', 'sun']

def is_long_word(word):
    return len(word) > 4

long_words = list(filter(is_long_word, words))
print(long_words) # ['mountain', 'river', 'cloud']

# map(): Used to apply a function to each item in an iterable and returns a new
# iterable with the results. Here is an example of using the map() function to
# covert a list of celsius temperatures to fahrenheit:

celsius = [0, 10, 20, 30, 40]

def to_farenheit(temp):
    return (temp * 9/5) + 32

farenheit = list(map(to_farenheit, celsius))
print(farenheit) # [32.0, 50.0, 68.0, 86.0, 104.0]

# sum(): Used to get the sum from an iterable like a list or tuple. Here is an
# example of using the sum() function:

numbers = [5, 10, 15, 20]
total = sum(numbers)
print(total) # Result: 50

# You can also pass in an optional start argument which sets the initial value
# for the summation. Here is an updated example using the start argument as a 
# positional argument:

numbers = [5, 10, 15, 20]
total = sum(numbers, 10) # positional argument
print(total) # 60

# You can also choose to use the start argument as a keyword argument like this:

numbers = [5, 10, 15, 20]
total = sum(numbers, start=10) # keyword argument
print(total) # 60

# Lambda functions
# Definition: A lambda function in Python is a concise way to create a function
# without a name (an anonymous function).

# Lambda functions are often used as an argument to another function. Here is an
# example of a lambda function:

numbers = [1, 2, 3, 4, 5]

even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(even_numbers) # [2, 4]

# Best practices for using lambda functions include not assigning them to a variable,
# keeping them simple and readable, and using them for short, one-off functions.

numbers = [1 ,2 ,3, 4 ,5, 5, 5]
numbers.remove(5)

print(numbers)

developer = ['Jane Doe', 23, 'Python Developer']
del developer[1]
print(developer) # ['Jane Doe', 'Python Developer']

programming_languages = ('Rust', 'Java', 'Python', 'C++', 'Rust', 'Python')
programming_languages.index('Python', 3)

print(programming_languages.index('Python', 3))

num1 = (133 / 521)
print(num1)