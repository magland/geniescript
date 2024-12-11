#!/usr/bin/env python3
"""Main module for processing and executing genie scripts."""

import os
import shlex
from typing import List, Optional, Tuple, cast
from .completion import do_completion, ChatMessage
from .instructions import get_instructions_from_py_file, insert_instructions_to_py_file
from .util import sha1


def process_source_file(source_file_name: str) -> Tuple[str, List[str], str]:
    """
    Process the source file and extract system files.

    Args:
        source_file_name: Path to the source file to process

    Returns:
        Tuple containing source text, system source files, and parent directory
    """
    parent_dir = os.path.dirname(source_file_name)

    with open(source_file_name, "r", encoding="utf-8") as f:
        source_text = f.read()

    system_source_files: List[str] = []
    source_lines = source_text.split("\n")
    source_lines_to_use = []

    for line in source_lines:
        if line.startswith("//"):
            if line.startswith("// system"):
                system_source_file = line.split(" ")[2]
                system_source_file = os.path.join(parent_dir, system_source_file)
                system_source_files.append(system_source_file)
            continue
        source_lines_to_use.append(line)

    return "\n".join(source_lines_to_use), system_source_files, parent_dir


def process_system_files(system_source_files: List[str]) -> Tuple[str, str]:
    """
    Process system files and generate system text and hash.

    Args:
        system_source_files: List of system source file paths

    Returns:
        Tuple containing system text and its hash
    """
    system_text = ""
    for system_file in system_source_files:
        print("Using system file:", system_file)
        with open(system_file, "r", encoding="utf-8") as f:
            system_text += f.read()
            system_text += "\n"

    return system_text, sha1(system_text)


def check_cache(py_fname: str, instructions: str) -> bool:
    """
    Check if cached version exists and is valid.

    Args:
        py_fname: Path to the Python output file
        instructions: Instructions to compare against cached version

    Returns:
        True if cache is valid, False otherwise
    """
    if os.path.exists(py_fname):
        instructions_to_compare = get_instructions_from_py_file(py_fname)
        return instructions_to_compare == instructions
    return False


def generate_code(system_text: str, source_text: str) -> str:
    """
    Generate Python code using the completion model.

    Args:
        system_text: System context for code generation
        source_text: Source text to generate code from

    Returns:
        Generated Python code
    """
    system_prompt = f"""
You are a coding assitant that returns Python code based on the user's input.
You should return a completely self-contained script that can be executed directly.
You should not return anything other than the script, because your output will be excecuted directly.

{system_text}
"""

    messages: List[ChatMessage] = [
        cast(ChatMessage, {"role": "system", "content": system_prompt}),
        cast(ChatMessage, {"role": "user", "content": source_text}),
    ]

    print("Generating code...")
    response = do_completion(messages)
    return remove_code_block_ticks(response)


def execute_script(py_fname: str, script_args: Optional[List[str]] = None) -> None:
    """
    Execute the generated Python script.

    Args:
        py_fname: Path to the Python file to execute
        script_args: Optional list of arguments to pass to the script
    """
    print("Executing code...")
    cmd = f"python {shlex.quote(py_fname)}"
    if script_args:
        cmd += " " + " ".join(shlex.quote(arg) for arg in script_args)
    os.system(cmd)


def run(
    source_file_name: str,
    execute: bool = True,
    script_args: Optional[List[str]] = None,
    force_regenerate: bool = False,
) -> None:
    """
    Main function that processes a source file to generate and execute Python code.

    Args:
        source_file_name: Path to the source file to process
        execute: Whether to execute the generated Python file
        script_args: Optional list of arguments to pass to the script
        force_regenerate: Whether to force regeneration of the Python file regardless of changes
    """
    py_fname = source_file_name + ".py"

    # Process source and system files
    source_text, system_source_files, _ = process_source_file(source_file_name)
    system_text, system_hash = process_system_files(system_source_files)

    # Generate instructions with system hash
    instructions = f"system hash: {system_hash}\n{source_text}"

    # Check cache unless force regeneration is requested
    if not force_regenerate and check_cache(py_fname, instructions):
        print("Instructions have not changed. Skipping code generation.")
        if execute:
            execute_script(py_fname, script_args)
        else:
            print(f"Python file already exists at {py_fname}")
        return

    # Generate and save new code
    response = generate_code(system_text, source_text)
    code = insert_instructions_to_py_file(response, instructions)

    with open(py_fname, "w", encoding="utf-8") as f:
        print("Writing code to", py_fname)
        f.write(code)

    if execute:
        execute_script(py_fname, script_args)
    else:
        print(f"Python file generated at {py_fname}")


def remove_code_block_ticks(response: str) -> str:
    """
    Remove markdown code block markers from the response text.

    Args:
        response: The response text potentially containing markdown code blocks

    Returns:
        Cleaned response with code block markers removed
    """
    lines = response.split("\n")
    in_code_block = False
    new_lines = []
    for line in lines:
        if line.startswith("```"):
            in_code_block = not in_code_block
        else:
            if in_code_block:
                new_lines.append(line)
            else:
                pass
    if len(new_lines) == 0:
        new_lines = lines
    return "\n".join(new_lines)
