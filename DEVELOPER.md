# Developer Guide

## Installation for Development

1. Clone the repository
```bash
git clone https://github.com/your-username/geniescript.git
cd geniescript
```

2. Install poetry if you haven't already
```bash
pip install poetry
```

3. Install dependencies in editable/development mode
```bash
poetry install  # This automatically installs in editable mode
```

The editable installation means any changes you make to the source code will be immediately reflected without needing to reinstall.

## Running Tests

Run all tests:
```bash
poetry run pytest
```

Run tests with coverage:
```bash
poetry run pytest --cov=geniescript
```

Run specific test file:
```bash
poetry run pytest tests/test_util.py
