#!/usr/bin/env python3
"""Main module for processing and executing genie scripts."""

import os
import shlex
from typing import List, Optional, cast
from .completion import do_completion, ChatMessage
from .instructions import get_instructions_from_py_file, insert_instructions_to_py_file
from .util import sha1


def run(
    source_file_name: str, execute: bool = True, script_args: Optional[List[str]] = None
) -> None:
    """
    Main function that processes a source file to generate and execute Python code.

    Args:
        source_file_name: Path to the source file to process
        execute: Whether to execute the generated Python file
        script_args: Optional list of arguments to pass to the script
    """
    # Get the directory containing the source file
    parent_dir = os.path.dirname(source_file_name)
    # Generate output Python filename by appending .py
    py_fname = source_file_name + ".py"

    # Read the source file content
    with open(source_file_name, "r", encoding="utf-8") as f:
        source_text = f.read()

    # List to store paths of system-related source files
    system_source_files: List[str] = []

    # Process source file lines
    source_lines = source_text.split("\n")
    source_lines_to_use = []
    for line in source_lines:
        if line.startswith("//"):
            # Handle special system file directives
            if line.startswith("// system"):
                system_source_file = line.split(" ")[2]
                system_source_file = os.path.join(parent_dir, system_source_file)
                system_source_files.append(system_source_file)
            continue
        source_lines_to_use.append(line)

    # Combine content from all system files
    system_text = ""
    for system_file in system_source_files:
        print("Using system file:", system_file)
        with open(system_file, "r", encoding="utf-8") as f:
            system_text += f.read()
            system_text += "\n"

    # Generate hash of system content for caching
    system_hash = sha1(system_text)
    instructions = f"system hash: {system_hash}\n{source_text}"

    # Check if output file exists and if content has changed
    if os.path.exists(py_fname):
        instructions_to_compare = get_instructions_from_py_file(py_fname)
        if instructions_to_compare == instructions:
            print("Instructions have not changed. Skipping code generation.")
            if execute:
                print("Executing code...")
                cmd = f"python {shlex.quote(py_fname)}"
                if script_args:
                    cmd += " " + " ".join(shlex.quote(arg) for arg in script_args)
                os.system(cmd)
                print("Done!")
            else:
                print(f"Python file already exists at {py_fname}")
            return

    # Define the system prompt for code generation
    system_prompt = f"""
You are a coding assitant that returns Python code based on the user's input.
You should return a completely self-contained script that can be executed directly.
You should not return anything other than the script, because your output will be excecuted directly.

{system_text}
"""

    # Prepare messages for the completion model
    messages: List[ChatMessage] = [
        cast(ChatMessage, {"role": "system", "content": system_prompt}),
        cast(ChatMessage, {"role": "user", "content": "\n".join(source_lines_to_use)}),
    ]

    # Generate code using the completion model
    print("Generating code...")
    response = do_completion(messages)
    response = remove_code_block_ticks(response)

    # Insert instructions into the generated code
    code = insert_instructions_to_py_file(response, instructions)

    # Write the generated code to file
    with open(py_fname, "w", encoding="utf-8") as f:
        print("Writing code to", py_fname)
        f.write(code)

    if execute:
        # Execute the generated code
        print("Executing code...")
        cmd = f"python {shlex.quote(py_fname)}"
        if script_args:
            cmd += " " + " ".join(shlex.quote(arg) for arg in script_args)
        os.system(cmd)
        print("Done!")
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
