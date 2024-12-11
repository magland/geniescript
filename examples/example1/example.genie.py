"""
system hash: 5d933f9c4b2916e71a4950ec6d368ee9005e8f74

Create a function that calculates the Fibonacci sequence up to n terms.
Then create a main section that:
1. Gets n as a command line argument
2. Validates that n is a positive integer
3. Calls the function to generate the sequence
4. Prints each number in the sequence on a new line

"""

import sys

def calculate_fibonacci(n: int) -> list[int]:
    """Calculate the Fibonacci sequence up to n terms.

    Args:
        n (int): The number of terms in the Fibonacci sequence to generate.

    Returns:
        list: A list of integers representing the Fibonacci sequence.

    Raises:
        ValueError: If n is less than or equal to zero.

    Example:
        >>> calculate_fibonacci(5)
        [0, 1, 1, 2, 3]
    """
    if n <= 0:
        raise ValueError("Number of terms must be a positive integer.")
    
    if n == 1:
        return [0]

    fibonacci_sequence = [0, 1]  # Starting values for the sequence

    # Generate Fibonacci sequence
    for i in range(2, n):
        next_value = fibonacci_sequence[-1] + fibonacci_sequence[-2]
        fibonacci_sequence.append(next_value)

    return fibonacci_sequence


def main() -> None:
    """Main function to get number of terms from command line and print the Fibonacci sequence."""
    # Check command line arguments
    if len(sys.argv) != 2:
        print("Usage: python script.py <number_of_terms>")
        sys.exit(1)

    try:
        n = int(sys.argv[1])
    except ValueError:
        print("Error: The number of terms must be an integer.")
        sys.exit(1)

    if n <= 0:
        print("Error: The number of terms must be a positive integer.")
        sys.exit(1)

    # Calculate and print the Fibonacci sequence
    try:
        fibonacci_sequence = calculate_fibonacci(n)
        for number in fibonacci_sequence:
            print(number)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()