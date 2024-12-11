"""
system hash: 5d933f9c4b2916e71a4950ec6d368ee9005e8f74
// system system.md

Create a function that calculates the Fibonacci sequence up to n terms.
Then create a main section that:
1. Gets n as a command line argument
2. Validates that n is a positive integer
3. Calls the function to generate the sequence
4. Prints each number in the sequence on a new line

"""

import sys


def fibonacci_sequence(n: int) -> list[int]:
    """Calculate the Fibonacci sequence up to n terms.

    Args:
        n (int): The number of terms in the Fibonacci sequence to generate.

    Returns:
        list[int]: A list containing the Fibonacci sequence.

    Raises:
        ValueError: If n is not a positive integer.

    Example:
        >>> fibonacci_sequence(5)
        [0, 1, 1, 2, 3]
    """
    if n <= 0:
        raise ValueError("The number of terms must be a positive integer.")

    sequence = [0, 1]
    for _ in range(2, n):
        # Calculate the next term by adding the last two terms
        next_value = sequence[-1] + sequence[-2]
        sequence.append(next_value)

    return sequence[:n]


def main():
    """Main function to execute the Fibonacci sequence generation.

    Gets the number of terms from the command line arguments, validates it, and
    prints each number in the Fibonacci sequence on a new line.

    Example:
        $ python fibonacci.py 5
        0
        1
        1
        2
        3
    """
    if len(sys.argv) != 2:
        print("Usage: python fibonacci.py <number_of_terms>")
        sys.exit(1)

    try:
        n = int(sys.argv[1])
        fibonacci = fibonacci_sequence(n)
        for number in fibonacci:
            print(number)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
