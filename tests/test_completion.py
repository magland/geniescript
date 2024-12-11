import os
import pytest
from unittest.mock import patch, MagicMock
from geniescript.completion import do_completion


@pytest.fixture
def mock_openai_client():
    with patch("openai.Client") as mock_client:
        yield mock_client


def test_missing_api_key():
    """Test that an exception is raised when OPENAI_API_KEY is not set"""
    with patch.dict(os.environ, clear=True):
        with pytest.raises(Exception) as exc_info:
            do_completion([{"role": "user", "content": "test"}])
        assert str(exc_info.value) == "OPENAI_API_KEY environment variable not set."


def test_successful_completion(mock_openai_client):
    """Test successful completion with mocked OpenAI response"""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Test response"
    mock_client_instance = mock_openai_client.return_value
    mock_client_instance.chat.completions.create.return_value = mock_response

    # Set mock API key
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        result = do_completion([{"role": "user", "content": "test"}])

    # Verify the result
    assert result == "Test response"
    mock_client_instance.chat.completions.create.assert_called_once_with(
        model="gpt-4o", messages=[{"role": "user", "content": "test"}]
    )


def test_failed_completion(mock_openai_client):
    """Test handling of failed completion where response is None"""
    # Setup mock response with None content
    mock_response = MagicMock()
    mock_response.choices[0].message.content = None
    mock_client_instance = mock_openai_client.return_value
    mock_client_instance.chat.completions.create.return_value = mock_response

    # Set mock API key
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        with pytest.raises(Exception) as exc_info:
            do_completion([{"role": "user", "content": "test"}])
        assert str(exc_info.value) == "Failed to generate response: received None."
