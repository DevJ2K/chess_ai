from typing import TypedDict, Literal


class ChatMessage(TypedDict):
    role: Literal["assistant", "user", "system"]
    content: str
