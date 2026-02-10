colors = ('red', 'blue', 'green')
print('Print first color and last color:',colors[0], colors[2])
print('Check if "blue" is in colors:', 'blue' in colors)

numbers = {1, 2, 3, 4 , 5}
numbers.add(6)
numbers.remove(3)
print('min number:', min(numbers), 'max number:', max(numbers))
popped_number = numbers.pop()
print('Popped Number:', popped_number)
print('Number popped. Current Numbers set:', numbers)
print('Check if 4 is in numbers:', 4 in numbers)