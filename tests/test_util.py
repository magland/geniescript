from geniescript.util import sha1


def test_sha1():
    """Test SHA1 hash of a simple string"""
    result = sha1("hello")
    assert len(result) == 40
    assert result == "aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d"
