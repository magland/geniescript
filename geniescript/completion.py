"""Module for handling OpenAI API completions and chat interactions."""

import os
from typing import Literal, TypedDict
import openai
from openai.types.chat import ChatCompletionMessageParam


class ChatMessage(TypedDict):
    """Type definition for chat message format."""

    role: Literal["system", "user", "assistant"]
    content: str


def do_completion(messages: list[ChatMessage]) -> str:
    """Generate a completion response using OpenAI's chat API.

    Args:
        messages: List of message dictionaries containing the conversation history.
                 Each message should have 'role' and 'content' keys.

    Returns:
        str: The generated response text.

    Raises:
        ValueError: If OPENAI_API_KEY environment variable is not set.
        openai.OpenAIError: If the API request fails or returns invalid response.
    """
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = openai.Client(
        api_key=openai_api_key,
    )

    # Convert messages to OpenAI's expected format
    api_messages: list[ChatCompletionMessageParam] = [
        {"role": msg["role"], "content": msg["content"]} for msg in messages
    ]

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=api_messages,
    )
    resp = completion.choices[0].message.content
    if resp is None:
        raise openai.OpenAIError("Failed to generate response: received None.")

    return resp
