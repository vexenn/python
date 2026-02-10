def check_even_odd(number):
    if number % 2 == 0:
        return f"{number} is Even"
    else:
        return f"{number} is Odd"
    
def find_max(*args):
    if not args:
        return "No numbers provided"
    
    current_max = args[0]
    for num in args:
        if num > current_max:
            current_max = num
    return current_max

def recursive_sum(n):
    if n <= 1: # Base case: if n is 1, the sum is just 1
        return n
    # Recursive case: n + sum of (n-1)
    else:
        return n + recursive_sum(n - 1)
    
print(find_max(3, 5 , 2, 8 , 1))
print(check_even_odd(10))
print(recursive_sum(5))

def store_employee_details(**kwargs):
    print("--- Employee Profile ---")
    for key, value in kwargs.items():
        print(f"{key.capitalize()}: {value}")
        return kwargs

justin_profile = store_employee_details(name="Justin", age=28, department="IT", role="Developer")

print(justin_profile)