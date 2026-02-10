# For loop from 1 to 10
for i in range(1, 11):
    if i == 5:
        continue # Skip the rest of the loop when i is 5
    if i == 8:
        break # Stop the loop at 8
    print(i)
else: print("Loop Finished")
print("-" * 20)
# While loop counting down from 10 to 1    
count = 10
while count >= 1:
    print(count)
    count -= 1 # Decrement to avoid an infinite loop
       