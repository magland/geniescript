"""Module for handling instruction comments in Python files.

This module provides functionality to extract and insert instruction comments
from/to Python files. Instructions are stored as docstrings at the beginning
of the files.
"""


def get_instructions_from_py_file(py_fname: str) -> str:
    """Extract instructions from a Python file's docstring.

    Args:
        py_fname: Path to the Python file to extract instructions from.

    Returns:
        str: The extracted instructions from the file's docstring.
             Returns empty string if no valid docstring is found.
    """
    with open(py_fname, "r", encoding="utf-8") as f:
        code = f.read()
    lines = code.split("\n")
    if len(lines) == 0:
        return ""
    if lines[0] != '"""':
        return ""
    instructions = []
    for line in lines[1:]:
        if line == '"""':
            break
        instructions.append(line)
    return "\n".join(instructions)


def insert_instructions_to_py_file(response: str, instructions: str) -> str:
    """Insert instructions into a Python file as a docstring.

    Args:
        response: The Python code to wrap with instructions.
        instructions: The instructions to insert as a docstring.

    Returns:
        str: The combined content with instructions as a docstring
             followed by the Python code.
    """
    return f'"""\n{instructions}\n"""\n\n{response}'
