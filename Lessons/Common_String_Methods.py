my_str = 'hello world'

uppercase_my_str = my_str.upper()
print(uppercase_my_str) # HELLO WORLD

my_str2 = 'Hello World'

lowercase_my_str2 = my_str2.lower()
print(lowercase_my_str2) # hello world

my_str3 = '   hello world   '

trimmed_my_str3 = my_str3.strip()
print(trimmed_my_str3) # hello world

replaced_my_str = my_str.replace('hello', 'hi')
print(replaced_my_str) # hi world

split_words = my_str.split()
print(split_words) # ['hello', 'world']

starts_with_hello = my_str.startswith('hello')
print(starts_with_hello) # True

ends_with_world = my_str.endswith('world')
print(ends_with_world) # True

world_index = my_str.find('world')
print(world_index) # 6

o_count = my_str.count('o')
print(o_count) # 2

capitalized_my_str = my_str.capitalize()
print(capitalized_my_str) # Hello world

is_all_upper = my_str.isupper()
print(is_all_upper) # False

is_all_lower = my_str.islower()
print(is_all_lower) # True

title_case_my_str = my_str.title()
print(title_case_my_str) # Hello World