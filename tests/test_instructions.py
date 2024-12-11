import pytest
import tempfile
import os
from geniescript.instructions import (
    get_instructions_from_py_file,
    insert_instructions_to_py_file,
)


@pytest.fixture
def temp_py_file():
    """Fixture to create a temporary Python file for testing"""
    fd, path = tempfile.mkstemp(suffix=".py")
    os.close(fd)
    yield path
    os.unlink(path)


def test_get_instructions_from_empty_file(temp_py_file):
    """Test getting instructions from an empty file"""
    with open(temp_py_file, "w") as f:
        f.write("")
    assert get_instructions_from_py_file(temp_py_file) == ""


def test_get_instructions_from_file_without_docstring(temp_py_file):
    """Test getting instructions from a file without docstring"""
    with open(temp_py_file, "w") as f:
        f.write('print("Hello")\n')
    assert get_instructions_from_py_file(temp_py_file) == ""


def test_get_instructions_from_file_with_docstring(temp_py_file):
    """Test getting instructions from a file with docstring"""
    content = '"""\nThis is a test instruction\nMultiple lines\n"""\n\nprint("Hello")'
    with open(temp_py_file, "w") as f:
        f.write(content)
    expected = "This is a test instruction\nMultiple lines"
    assert get_instructions_from_py_file(temp_py_file) == expected


def test_get_instructions_from_file_with_empty_docstring(temp_py_file):
    """Test getting instructions from a file with empty docstring"""
    content = '"""\n"""\n\nprint("Hello")'
    with open(temp_py_file, "w") as f:
        f.write(content)
    assert get_instructions_from_py_file(temp_py_file) == ""


def test_insert_instructions():
    """Test inserting instructions into Python code"""
    instructions = "Test instruction\nMultiple lines"
    code = "print('Hello')"
    expected = '"""\nTest instruction\nMultiple lines\n"""\n\nprint(\'Hello\')'
    assert insert_instructions_to_py_file(code, instructions) == expected


def test_insert_empty_instructions():
    """Test inserting empty instructions"""
    instructions = ""
    code = "print('Hello')"
    expected = '"""\n\n"""\n\nprint(\'Hello\')'
    assert insert_instructions_to_py_file(code, instructions) == expected
