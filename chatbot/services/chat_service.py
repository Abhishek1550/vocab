from chatbot.models import ChatMessage
from chatbot.providers.gemini import GeminiProvider
from chatbot.services.prompts import SYSTEM_PROMPT
from chatbot.services.tool_definitions import GEMINI_TOOLS
from chatbot.services.tool_executor import ToolExecutor


class ChatService:

    def __init__(self):
        self.provider = GeminiProvider()

    def get_recent_messages(
        self,
        user,
        limit=20,
    ):
        messages = (
            ChatMessage.objects
            .filter(user=user)
            .order_by("-created_at")[:limit]
        )

        return list(reversed(messages))

    def process_message(
        self,
        user,
        message,
    ):
        # Save user message
        ChatMessage.objects.create(
            user=user,
            role="user",
            content=message,
        )

        conversation = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]

        history = self.get_recent_messages(user)

        for msg in history:
            conversation.append(
                {
                    "role": msg.role,
                    "content": msg.content,
                }
            )

        #
        # FIRST GEMINI CALL
        #
        response = self.provider.chat(
            messages=conversation,
            tools=GEMINI_TOOLS,
        )

        #
        # TOOL CALL PATH
        #
        if response.tool_call:

            tool_result = ToolExecutor.execute(
                user=user,
                tool_name=response.tool_call.name,
                arguments=response.tool_call.arguments,
            )

            #
            # SECOND GEMINI CALL
            #
            followup_messages = conversation.copy()

            followup_messages.append(
                {
                    "role": "user",
                    "content": (
                        f"The tool "
                        f"'{response.tool_call.name}' "
                        f"returned:\n\n"
                        f"{tool_result}\n\n"
                        f"Answer the user's question "
                        f"using this data."
                    ),
                }
            )

            final_response = self.provider.chat(
                messages=followup_messages
            )

            reply = final_response.text

        #
        # NORMAL TEXT PATH
        #
        else:
            reply = response.text

        ChatMessage.objects.create(
            user=user,
            role="assistant",
            content=reply,
        )

        return reply