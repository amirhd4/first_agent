import os
import asyncio
import sys
from pathlib import Path

from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, ModelSettings
from agents.mcp import MCPServerStdio
from openai import AsyncOpenAI

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SERVER_FILE = (
    PROJECT_ROOT / "src" / "mcp_servers"
    / "system" / "server.py"
)


async def main():
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY تنظیم نشده است.")

    client = AsyncOpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
    )

    # استفاده از OpenRouter به‌جای OpenAI
    set_tracing_disabled(True)

    model = OpenAIChatCompletionsModel(
        model="nvidia/nemotron-3-ultra-550b-a55b:free",
        openai_client=client,
    )

    async with MCPServerStdio(
        name="System MCP",
        params={
            "command": sys.executable,
            "args": [str(SERVER_FILE)],
            "cwd": str(PROJECT_ROOT),
        }
    ) as server:

        agent = Agent(
            name="Desktop Assistant",
            instructions=(
                "Use the system MCP tools to answer questions "
                "about the computer. Do not invent tool results."
            ),
            model=model,
            model_settings=ModelSettings(max_tokens=100),
            mcp_servers=[server],
        )
        result = await Runner.run(
            agent,
            "با ابزار های MCP داده های سیستم عامل "
            "مسیر کاری فعلی را بررسی کن."
        )

        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())