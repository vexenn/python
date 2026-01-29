# variable <operator>= value

# variable = variable <operator> value

my_var = 10
my_var += 5 # Equivalent to: my_var = my_var + 5
print(my_var) # 15

my_var2 = 10
my_var2 = my_var2 + 5

print(my_var2) # 15

count = 14
count -= 3 # Equivalent to: count = count - 3
print(count) # 11

product = 65
product *= 7 # Equivalent to: product = product * 7
print(product) # 455

price = 100
price /= 4
print(price) # 25.0

# The floor division operator (//=) floor‑divides the 
# left variable by the right and stores the result back in the left variable

total_pages = 327
total_pages //= 5
print(total_pages) # 4

# The modulus assignment operator %= computes the remainder
# of left variable divided by the right and stores it back in the left variable


bits = 35
bits %= 2
print(bits) # 1

#The exponentiation assignment operator **= raises the left variable to
# the power of the right and stores the result back in the left variable

power = 2
power **= 3
print(power) # 8

greet = 'Hello'
greet += ' World'

print(greet) # Hello World

greet *= 3
print(greet) # Hello WorldHello WorldHello World

# greet -= ' World'
# This will raise an error because the subtraction operator is not defined
# for strings in Python

# greet /= 'World'
# This will also raise an error because the division operator is not defined
# for strings in Python

my_var3 = 5

print(+my_var3) # 5
print(++my_var3) # 5
print(+++my_var3) # 5

my_var3 += 1
print(my_var3) # 6