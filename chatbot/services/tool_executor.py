from chatbot.services.tools import TOOLS


class ToolExecutor:

    @staticmethod
    def execute(
        user,
        tool_name,
        arguments,
    ):

        tool = TOOLS.get(tool_name)

        if not tool:
            return {
                "error": f"Unknown tool {tool_name}"
            }

        return tool(
            user=user,
            **arguments,
        )