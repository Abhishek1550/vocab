from dataclasses import dataclass
from typing import Optional


@dataclass
class ToolCall:
    name: str
    arguments: dict


@dataclass
class ChatResponse:
    text: Optional[str] = None
    tool_call: Optional[ToolCall] = None