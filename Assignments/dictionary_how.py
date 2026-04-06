# dictionary = {
#     key1: value1,
#     key2: value2
# }

pizza = {
    'name': 'Margherita Pizza',
    'price': 8.9,
    'calories_per_slice': 250,
    'toppings': ['mozzarella', 'basil']
}

pizza = dict([('name', 'Margherita Pizza'), ('price', 8.9), ('toppings', ['mozzerella', 'basil'])])

print(pizza['name']) # Margherita Pizza

print(pizza.get('price', []))

print(pizza.keys())

print(pizza.values())

# The .items() method returns a view object with all the key-value pairs in the
# dictionary, including both the keys and the values:

print(pizza.items())

# The .clear() method removes all the key-value pairs from the dictionary:

print(pizza.clear()) # None