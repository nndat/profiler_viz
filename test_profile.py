from func_profiler import func_profile
import time


# Test 1: No destination (save to current directory)
@func_profile()
def calculate_fibonacci(n):
    """Calculate fibonacci number"""
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)


# Test 2: With custom destination
@func_profile(dest="./profile_results")
def process_data():
    """Process some data"""
    result = 0
    for i in range(1000000):
        result += i ** 2
    return result


if __name__ == "__main__":
    print("Testing func_profile decorator...\n")

    print("Test 1: calculate_fibonacci(20)")
    result1 = calculate_fibonacci(20)
    print(f"Result: {result1}\n")

    print("Test 2: process_data()")
    result2 = process_data()
    print(f"Result: {result2}\n")

    print("All tests completed!")
