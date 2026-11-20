import os
import asyncio
import sys
from pathlib import Path

from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, ModelSettings
from agents.mcp import MCPServerStdio
from openai import AsyncOpenAI

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SYSTEM_SERVER_FILE = PROJECT_ROOT / "src" / "mcp_servers" / "system" / "server.py"
SEARCH_SERVER_FILE = PROJECT_ROOT / "src" / "mcp_servers" / "web_search" / "server.py"


async def main():
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY تنظیم نشده است.")

    client = AsyncOpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
    )

    set_tracing_disabled(True)

    model = OpenAIChatCompletionsModel(
        model="nvidia/nemotron-3-ultra-550b-a55b:free",
        openai_client=client,
    )

    async with (
        MCPServerStdio(
            name="System MCP",
            params={
                "command": sys.executable,
                "args": [str(SYSTEM_SERVER_FILE)],
                "cwd": str(PROJECT_ROOT),
            },
        ) as system_server,
        MCPServerStdio(
            name="Web Search MCP",
            params={
                "command": sys.executable,
                "args": [str(SEARCH_SERVER_FILE)],
                "cwd": str(PROJECT_ROOT),
            },
        ) as search_server,
    ):
        agent = Agent(
            name="Desktop & Web Assistant",
            instructions=(
                "You are a helpful assistant with access to both system information tools "
                "and internet web search tools. "
                "Use the web search tools whenever the user asks for current events, "
                "online information, or topics you need to look up. "
                "Use system tools when asked about the local computer. "
                "Do not invent tool results and always cite URLs when summarizing web results. "
                "Answer in fluent Persian language."
            ),
            model=model,
            model_settings=ModelSettings(max_tokens=4000),
            mcp_servers=[system_server, search_server],
        )

        # تست ترکیبی: هم سیستم را چک می‌کند و هم در اینترنت سرچ می‌کند
        prompt = (
            "اول چک کن سیستم‌عامل من چیه و چه نسخه پایتونی نصبه، "
            "بعد در اینترنت درباره آخرین اخبار هوش مصنوعی در هفته اخیر جست‌وجو کن و 3 مورد مهمش رو با لینک برام خلاصه کن. همچنین ببین اخرین پردازش های سیستم من ویروسی نیسن با سرچ"
        )

        print("در حال پردازش درخواست و فراخوانی ابزارها...\n")
        result = await Runner.run(agent, prompt)
        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())