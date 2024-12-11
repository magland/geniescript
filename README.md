# geniescript

![Test](https://github.com/magland/geniescript/actions/workflows/test.yml/badge.svg)

A Python CLI tool that helps scientists and researchers generate and execute data processing scripts using AI language models. This tool simplifies the process of creating Python scripts for data analysis, transformation, and visualization tasks.

## Installation

```bash
pip install geniescript
```

## Usage

1. Set your OpenAI API key:
```bash
export OPENAI_API_KEY=your_api_key_here
```

2. Create a source file (e.g., `analysis.genie`) with instructions describing your data processing task.

3. Run the script:

```bash
geniescript run analysis.genie
```

The tool will:
- Generate a Python script based on your data processing instructions using AI
- Save the generated code to `analysis.genie.py`
- Execute the generated Python script

If you run the command again with the same instructions, it will skip the generation step and directly execute the existing Python script.

### Command Options

`--no-execute`: Generate the Python file without executing it. This is useful when you want to review or modify the generated code before processing your data.
```bash
geniescript run analysis.genie --no-execute
```

`--script-args`: Pass command line arguments to the generated Python script, such as input file paths or processing parameters. These arguments will be accessible via sys.argv in the generated script.
```bash
geniescript run analysis.genie --script-args="input_data.csv output_results.csv"
```

### Examples

1. Basic command output example:
```bash
# Create a script that uses system commands
echo "Create a Python script that prints the first 10 prime numbers" > analysis.genie

# Run it
geniescript run analysis.genie
```

2. CSV processing with command-line arguments:
```bash
# Create a script to analyze data
echo "Create a Python script that processes CSV data. The script should:
- Read the input CSV file from the first command-line argument (sys.argv[1])
- Calculate basic statistics (mean, median, std) for each numeric column
- Save results to the output CSV file specified in the second argument (sys.argv[2])" > analyze.genie

# Run it with input/output file paths
geniescript run analyze.genie --script-args="experiment_data.csv stats_results.csv"
```

### System Files

You can include system files in your instructions using the special comment syntax:
```
// system path/to/system/file.txt
```

These files will be included in the system prompt for the AI model. This is useful for providing additional context about your data format, analysis requirements, or processing parameters. System files are also an excellent way to teach the AI about specific packages that are installed in your environment and how to use them effectively.
