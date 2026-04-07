from typing import List

from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool


def create_platform_agent(
    name: str, instructions: str, tools: List[FunctionTool]
) -> LlmAgent:
    """Factory para criar agentes com tools baseadas em FunctionTool."""
    return LlmAgent(
        model="gemini-1.5-flash",
        name=name,
        instruction=instructions,
        tools=tools,
    )
