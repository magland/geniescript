#!/usr/bin/env python3
import re
import toml

def update_init_file(new_version):
    init_path = 'geniescript/__init__.py'
    with open(init_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update version while preserving formatting
    new_content = re.sub(
        r'__version__\s*=\s*"[^"]*"',
        f'__version__ = "{new_version}"',
        content
    )

    with open(init_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

def bump_patch_version():
    # Read the current pyproject.toml
    with open('pyproject.toml', 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse the TOML content
    data = toml.loads(content)

    # Get current version
    current_version = data['tool']['poetry']['version']

    # Split version into major, minor, patch
    major, minor, patch = map(int, current_version.split('.'))

    # Increment patch version
    patch += 1

    # Create new version string
    new_version = f"{major}.{minor}.{patch}"

    # Update version in the TOML data
    data['tool']['poetry']['version'] = new_version

    # Write back to pyproject.toml
    # We use regex to replace just the version to maintain file formatting
    new_content = re.sub(
        r'version\s*=\s*"[^"]*"',
        f'version = "{new_version}"',
        content
    )

    with open('pyproject.toml', 'w', encoding='utf-8') as f:
        f.write(new_content)

    # Update version in __init__.py
    update_init_file(new_version)

    print(f"Version bumped from {current_version} to {new_version}")
    print("Updated version in both pyproject.toml and geniescript/__init__.py")

if __name__ == '__main__':
    bump_patch_version()
