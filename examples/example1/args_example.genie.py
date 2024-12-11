"""
system hash: da39a3ee5e6b4b0d3255bfef95601890afd80709
Create a Python script that prints out all command line arguments that were passed to it.

The script should:
1. Import sys to access command line arguments
2. Print each argument on a new line with its index
3. Handle the case where no arguments were passed

"""

import sys


def main():
    if len(sys.argv) > 1:
        for index, arg in enumerate(sys.argv[1:], start=1):
            print(f"Argument {index}: {arg}")
    else:
        print("No command line arguments were passed.")


if __name__ == "__main__":
    main()
