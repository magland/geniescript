"""Tests for the instructions module."""

from geniescript.instructions import (
    get_instructions_from_py_file,
    insert_instructions_to_py_file,
)


def test_get_instructions_empty_file(tmp_path):
    """Test getting instructions from an empty file."""
    py_file = tmp_path / "empty.py"
    py_file.write_text("")
    assert get_instructions_from_py_file(str(py_file)) == ""


def test_get_instructions_no_docstring(tmp_path):
    """Test getting instructions from a file without a docstring."""
    py_file = tmp_path / "no_docstring.py"
    py_file.write_text("print('hello')")
    assert get_instructions_from_py_file(str(py_file)) == ""


def test_get_instructions_with_docstring(tmp_path):
    """Test getting instructions from a file with a docstring."""
    py_file = tmp_path / "with_docstring.py"
    py_file.write_text('"""\ntest instructions\n"""\nprint("hello")')
    assert get_instructions_from_py_file(str(py_file)) == "test instructions"


def test_get_instructions_multiline_docstring(tmp_path):
    """Test getting instructions from a file with a multiline docstring."""
    py_file = tmp_path / "multiline.py"
    py_file.write_text('"""\nline1\nline2\nline3\n"""\nprint("hello")')
    assert get_instructions_from_py_file(str(py_file)) == "line1\nline2\nline3"


def test_insert_instructions():
    """Test inserting instructions into Python code."""
    response = "print('hello')"
    instructions = "test instructions"
    expected = '"""\ntest instructions\n"""\n\nprint(\'hello\')'
    assert insert_instructions_to_py_file(response, instructions) == expected


def test_insert_multiline_instructions():
    """Test inserting multiline instructions into Python code."""
    response = "print('hello')"
    instructions = "line1\nline2\nline3"
    expected = '"""\nline1\nline2\nline3\n"""\n\nprint(\'hello\')'
    assert insert_instructions_to_py_file(response, instructions) == expected
