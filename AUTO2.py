import time

Seconds_input = int(input("Enter a number of seconds to count down "))

print("Starting countdown...")
for i in range(Seconds_input, 0, -1):
    print(f"Time remaining: {i} seconds")
    time.sleep(1)

print("Countdown finished!")
