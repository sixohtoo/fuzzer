import time

def log_vuln(start_time,end_time,mutated_text):
    print(f"Found vulnerability at {end_time - start_time}s")
    print(f"The mutated input that caused the program to crash is:")
    print(mutated_text)
    print("--------------------------------------------------------")


def update_log(dict,cov_dict,start_time, end_time):
    iterations = find_iterations(dict)
    print(" =================== UPDATE LOG ==========================")
    print(f"iteration: {iterations}")
    print(f"time: {(end_time - start_time)}s")
    for crash in dict:
        print(f"{dict[crash]} crashes were caused from {crash}() method")
    # fuzzer based code coverage
    print(f"---")
    for mutation in cov_dict:
        print(f"{cov_dict[mutation]} times was mutation stratgey: {mutation} called")

def find_iterations(dict):
    iterations = 0
    for crash in dict:
        iterations += dict[crash]
    return iterations

if __name__ == "__main__":
    update_log({"flip_bits":1,"a":2,"c":4,"d":100},time.time(),time.time())