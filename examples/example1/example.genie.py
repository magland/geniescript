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

def fibonacci(n: int) -> list[int]:
    """Generate Fibonacci sequence up to n terms.
    
    Args:
        n (int): The number of terms in the Fibonacci sequence to generate.
        
    Returns:
        list[int]: A list containing the Fibonacci sequence up to n terms.
        
    Raises:
        ValueError: If n is not a positive integer.
        
    Example:
        >>> fibonacci(5)
        [0, 1, 1, 2, 3]
    """
    if n <= 0:
        raise ValueError("Number of terms must be a positive integer.")
    
    sequence = [0, 1]  # Initializing the first two Fibonacci numbers

    # Generate the Fibonacci sequence iteratively
    for i in range(2, n):
        next_number = sequence[i - 1] + sequence[i - 2]
        sequence.append(next_number)
    
    return sequence[:n]


def main():
    """Main function to execute Fibonacci sequence generation from command line arguments."""
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <n>")
        sys.exit(1)
    
    try:
        n = int(sys.argv[1])
    except ValueError:
        print("Please enter a valid positive integer for n.")
        sys.exit(1)
        
    if n <= 0:
        print("Please enter a positive integer.")
        sys.exit(1)
    
    # Generate the Fibonacci sequence and print each element
    try:
        fib_sequence = fibonacci(n)
        for num in fib_sequence:
            print(num)
    except ValueError as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()