"""
Basic usage example for profiler-viz
"""

from profiler_viz import func_profile


@func_profile()
def calculate_pi(n_terms):
    """Calculate Pi using Leibniz formula"""
    pi = 0
    for i in range(n_terms):
        pi += ((-1) ** i) / (2 * i + 1)
    return 4 * pi


@func_profile(dest="./profile_output")
def fibonacci(n):
    """Calculate Fibonacci number recursively"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)


@func_profile()
def process_list(size):
    """Process a large list"""
    data = list(range(size))

    # Various operations
    squared = [x**2 for x in data]
    filtered = [x for x in squared if x % 2 == 0]
    total = sum(filtered)

    return total


if __name__ == "__main__":
    print("Example 1: Calculate Pi")
    pi_value = calculate_pi(1000000)
    print(f"Pi ≈ {pi_value}\n")

    print("Example 2: Fibonacci")
    fib_value = fibonacci(15)
    print(f"Fibonacci(15) = {fib_value}\n")

    print("Example 3: Process List")
    result = process_list(1000000)
    print(f"Result = {result}\n")

    print("Done! Check the generated HTML files for detailed performance analysis.")
