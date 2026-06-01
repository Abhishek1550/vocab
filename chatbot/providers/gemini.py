from django.conf import settings
from google import genai
from google.genai import types

from chatbot.providers.types import (
    ChatResponse,
    ToolCall,
)
from .base import LLMProvider


class GeminiProvider(LLMProvider):

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

    def chat(
        self,
        messages,
        tools=None,
    ):
        prompt = "\n".join(
            f"{message['role']}: {message['content']}"
            for message in messages
        )

        config = None

        if tools:
            function_declarations = []

            for tool in tools:
                function_declarations.append(
                    types.FunctionDeclaration(
                        name=tool["name"],
                        description=tool["description"],
                        parameters=tool["parameters"],
                    )
                )

            config = types.GenerateContentConfig(
                tools=[
                    types.Tool(
                        function_declarations=function_declarations
                    )
                ]
            )

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=config,
        )

        print("\n=== GEMINI RESPONSE ===")
        print(response)

        candidate = response.candidates[0]

        for part in candidate.content.parts:

            if hasattr(part, "function_call") and part.function_call:

                return ChatResponse(
                    tool_call=ToolCall(
                        name=part.function_call.name,
                        arguments=dict(part.function_call.args),
                    )
                )

        return ChatResponse(
            text=response.text
        )