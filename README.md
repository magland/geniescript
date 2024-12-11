# geniescript

A Python CLI tool for generating and executing Python code using GPT-4.

## Installation

```bash
pip install geniescript
```

## Usage

1. Set your OpenAI API key:
```bash
export OPENAI_API_KEY=your_api_key_here
```

2. Create a source file (e.g., `script.genie`) with instructions for what you want the script to do.

3. Run the script:

```bash
geniescript script.genie
```

The tool will:
- Generate a Python script based on your instructions using GPT-4
- Save the generated code to `script.genie.py`
- Execute the generated Python script

If you run the command again with the same instructions, it will skip the generation step and directly execute the existing Python script.

### Command Options

`--no-execute`: Generate the Python file without executing it. This is useful when you want to review or modify the generated code before running it.
```bash
geniescript script.genie --no-execute
```

`--script-args`: Pass command line arguments to the generated Python script. These arguments will be accessible via sys.argv in the generated script.
```bash
geniescript script.genie --script-args="arg1 arg2 arg3"
```

For example, if you have a script that processes command line arguments:
```bash
# Create a script to handle arguments
echo "Create a Python script that prints out all command line arguments that were passed to it." > args.genie

# Run it with arguments
geniescript args.genie --script-args="hello world"
# Output:
# Argument 1: hello
# Argument 2: world
```

### System Files

You can include system files in your instructions using the special comment syntax:
```
// system path/to/system/file.txt
```

These files will be included in the system prompt for the GPT-4 model.
