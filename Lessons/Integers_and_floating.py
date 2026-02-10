my_int_1 = 56
my_int_2 = -4

print(type(my_int_1)) # <class 'int'>
print(type(my_int_2)) # <class 'int'>

sum_ints = my_int_1 + my_int_2
print('Integer Addition:', sum_ints) # Integer Addition: 68

# Subtraction

diff_ints = my_int_1 - my_int_2
print('Integer Subtraction:', diff_ints) # Integer Subtraction: 60

# Multiplication
produce_ints = my_int_1 * my_int_2
print('Integer Multiplication:', produce_ints) # Integer Multiplication: -224

# Division
div_ints = my_int_1 / my_int_2
print('Integer Division:', div_ints) # Integer Division: -14.0

my_float_1 = -12.0
my_float_2 = 4.9

print(type(my_float_1)) # <class 'float'>
print(type(my_float_2)) # <class 'float'>

float_addition = my_float_1 + my_float_2
print('Float Addition:', float_addition) # Float Addition: -7.1

float_subtraction = my_float_1 - my_float_2
print('Float Subtraction:', float_subtraction) # Float Subtraction: -16.9

float_multiplication = my_float_1 * my_float_2
print('Float Multiplication:', float_multiplication) # Float Multiplication: -58.8

float_division = my_float_2 / my_float_1
print('Float Division:', float_division) # Float Division: -0.4083333333333333

sum_int_and_float = my_int_1 + my_float_2
print(sum_int_and_float) # 60.9
print(type(sum_int_and_float)) # <class 'float'>

mod_ints = my_int_1 % my_int_2
mod_floats = my_float_2 % my_float_1
print('Integer Modulus:', mod_ints) # Integer Modulus: 0
print('Float Modulus:', mod_floats) # Float Modulus: -7.1

floor_div_ints = my_int_1 // my_int_2
floor_div_floats = my_float_2 // my_float_1
print('Integer Floor Division:', floor_div_ints) # Integer Floor Division: -14
print('Float Floor Division:', floor_div_floats) # Float Floor Division: -1

exp_ints = my_int_1 ** my_int_2
exp_floats = my_float_1 ** my_float_2
print('Integer Exponentiation:', exp_ints) # Integer Exponentiation: 1.0168289254477302e-07
print('Float Exponentiation:', exp_floats) # Float Exponentiation: (-184584.1607052842+59975.02942576666j)

my_float_3 = float(my_int_1)

print(my_float_3) # 56.0
print(type(my_float_3)) # <class 'float'>

my_int3 = int(my_float_2)

print(my_int3) # 4
print(type(my_int3)) # <class 'int'>

my_str_int = '45'
my_str_float = '7.8'

converted_int = int(my_str_int)
converted_float = float(my_str_float)

print(converted_int, type(converted_int)) # 45 <class 'int'>
print(converted_float, type(converted_float)) # 7.8 <class 'float'>

my_int_4 = 4.798
my_int_5 = 4.253

rounded_int_4 = round(my_int_4)
rounded_int_5 = round(my_int_5, 1)

print(rounded_int_4) # 5
print(rounded_int_5) # 4.3

num = -15

absolute_value = abs(num)
print(absolute_value) # 15

result_1 = pow(2, 3) # Equivalent to 2 ** 3
print(result_1) # 8

result_2 = pow(2, 3, 5) # Equivalent to (2 ** 3) % 5
print(result_2) # 3