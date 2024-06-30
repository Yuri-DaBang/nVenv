import os

while True:
    try:
        other = input(">> ")
        if other.strip().lower() == "exit":
            break  # Exit the loop and terminate the script
        elif other.strip().lower() == "":
            continue  # Exit the loop and terminate the script
        os.system(f"python nvenv.py {other}")
    except KeyboardInterrupt:
        print("<return> <CTRL+C>")
    except Exception as e:
        print(f"<return> <Error::{e}>")
