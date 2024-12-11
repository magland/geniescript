from unittest.mock import patch
from geniescript.run import (
    process_source_file,
    process_system_files,
    check_cache,
    generate_code,
    execute_script,
    run,
    remove_code_block_ticks,
)


def test_process_source_file(tmp_path):
    source_content = """// system test_system.md
// This is a comment
print('hello')
"""
    source_file = tmp_path / "test.genie"
    source_file.write_text(source_content)

    result, system_files, parent_dir = process_source_file(str(source_file))

    assert result.strip() == "print('hello')"
    assert len(system_files) == 1
    assert system_files[0].endswith("test_system.md")
    assert parent_dir == str(tmp_path)


def test_process_system_files(tmp_path):
    system_file = tmp_path / "test_system.md"
    system_file.write_text("System content")

    system_text, system_hash = process_system_files([str(system_file)])

    assert system_text.strip() == "System content"
    assert isinstance(system_hash, str)
    assert len(system_hash) > 0


def test_check_cache(tmp_path):
    py_file = tmp_path / "test.py"
    instructions = "test instructions"

    # Test when file doesn't exist
    assert check_cache(str(py_file), instructions) is False

    # Test when file exists with different instructions
    py_file.write_text('"""\nother instructions\n"""\n')
    assert check_cache(str(py_file), instructions) is False

    # Test when file exists with same instructions
    py_file.write_text('"""\ntest instructions\n"""\n')
    assert check_cache(str(py_file), instructions) is True


@patch("geniescript.run.do_completion")
def test_generate_code(mock_completion):
    mock_completion.return_value = "```python\nprint('test')\n```"

    result = generate_code("system text", "source text")

    assert result == "print('test')"
    mock_completion.assert_called_once()


@patch("os.system")
def test_execute_script(mock_system):
    execute_script("test.py", ["arg1", "arg2"])
    mock_system.assert_called_once_with("python test.py arg1 arg2")


@patch("geniescript.run.generate_code")
@patch("geniescript.run.execute_script")
@patch("geniescript.run.process_system_files")
def test_run(mock_system_files, mock_execute, mock_generate, tmp_path):
    # Create test files
    source_file = tmp_path / "test.genie"
    source_file.write_text("print('test')")

    mock_generate.return_value = "print('generated')"
    mock_system_files.return_value = ("", "abc")  # Empty system text, hash 'abc'

    # Test normal execution
    run(str(source_file))

    assert mock_generate.called
    assert mock_execute.called

    # Test no-execute mode
    mock_execute.reset_mock()
    run(str(source_file), execute=False)
    assert not mock_execute.called

    # Test cache hit with no-execute
    mock_execute.reset_mock()
    mock_generate.reset_mock()
    py_file = tmp_path / "test.genie.py"
    py_file.write_text('"""\nsystem hash: abc\nprint(\'test\')\n"""\n')
    run(str(source_file), execute=False)
    assert not mock_execute.called
    assert not mock_generate.called


def test_remove_code_block_ticks():
    # Test with code blocks
    input_text = "```python\nprint('test')\n```"
    assert remove_code_block_ticks(input_text) == "print('test')"

    # Test without code blocks
    input_text = "print('test')"
    assert remove_code_block_ticks(input_text) == "print('test')"

    # Test with empty code block
    input_text = "```python\n```"
    result = remove_code_block_ticks(input_text)
    assert result == "```python\n```", "Empty code blocks should be returned as-is"
