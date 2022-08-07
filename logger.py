import time

def log_vuln(start_time,end_time,mutated_text):
    print(f"Found vulnerability: {end_time - start_time}s")
    print(f"The mutated input that caused the program to crash is:")
    print(mutated_text)
    print("--------------------------------------------------------")