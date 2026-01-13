import os
from typing import Literal

import anthropic
import openai


def get_completion(
    prompt: str,
    system_prompt: str = "",
    provider: Literal["anthropic", "openai"] = "anthropic",
    max_tokens: int = 4096,
) -> str:
    if provider == "anthropic":
        return _get_anthropic_completion(prompt, system_prompt, max_tokens)
    elif provider == "openai":
        return _get_openai_completion(prompt, system_prompt, max_tokens)
    else:
        raise ValueError(f"Unknown provider: {provider}")


def _get_anthropic_completion(prompt: str, system_prompt: str, max_tokens: int) -> str:
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=max_tokens,
        system=system_prompt if system_prompt else None,
        messages=[{"role": "user", "content": prompt}],
    )

    return message.content[0].text


def _get_openai_completion(prompt: str, system_prompt: str, max_tokens: int) -> str:
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        max_tokens=max_tokens,
        messages=messages,
    )

    return response.choices[0].message.content
