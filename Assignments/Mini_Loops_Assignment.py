# 1. Print Numbers from 1 to 5
for num in range(1, 6):
    print(num)
# 2. Print 5 stars in one line
for _ in range(1):
    print('*' * 5, end=' ')
    print()
# 3. Print star pattern (triangle)
for i in range(1, 4):
    for j in range(i):
        print('*', end='')
    print()
# 4. Print number pattern
for i in range(1, 4):
    for j in range(1, i + 1,):
        print(j, end='')
    print()
# 5. Print even numbers from 2 to 10
for num in range(2, 11, 2):
    if num == 10:
        print(num)
    else:
        print(num, end=' ')
# 6. Print numbers from 1 to 5, but skip 3
for num in range(1, 6):
    if num == 3:
        continue
    print(num, end=' ')