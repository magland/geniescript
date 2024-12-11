"""Utility functions for the geniescript package."""

import hashlib


def sha1(text):
    """
    Generate SHA1 hash of input text.

    Args:
        text (str): Input text to hash

    Returns:
        str: SHA1 hash of the input text
    """
    return hashlib.sha1(text.encode()).hexdigest()
