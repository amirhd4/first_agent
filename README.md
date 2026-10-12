# First MCP Project

A Python project demonstrating how to build a Model Context Protocol (MCP) server and connect it to an AI agent using the OpenAI Agents SDK and OpenRouter.

The project provides system information tools that allow an AI agent to retrieve basic operating system details, inspect the current working directory, and list running processes.

## Features

- **System Information:** Retrieve the operating system, OS version, computer name, and Python version.
- **Current Directory:** Get the current working directory of the MCP server process.
- **Process Listing:** Retrieve up to 10 running processes with their process IDs (PIDs) and names.
- **MCP Integration:** Expose Python functions as tools through an MCP server.
- **AI Agent Integration:** Connect the MCP server to an AI agent using the OpenAI Agents SDK.
- **OpenRouter Support:** Use models available through OpenRouter with an OpenAI-compatible API.

## Tech Stack

- Python 3.12+
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [OpenAI Agents SDK](https://github.com/openai/openai-agents-python)
- [OpenRouter](https://openrouter.ai/)
- [psutil](https://github.com/giampaolo/psutil)
- [uv](https://docs.astral.sh/uv/)

## Project Structure

```text
first_mcp_project/
├── src/
│   ├── agent/
│   │   └── runner.py
│   └── mcp_servers/
│       └── system/
│           └── server.py
├── pyproject.toml
├── uv.lock
└── README.md
```

## Requirements

- Python 3.12 or newer
- uv package manager
- An OpenRouter API key to run the AI agent
- Internet access for API requests

## Installation

### 1. Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd first_mcp_project
```

Replace `<YOUR_REPOSITORY_URL>` with your repository URL.

### 2. Install Dependencies

```bash
uv sync
```

If you are setting up the project from scratch, you can install the required dependencies with:

```bash
uv add "mcp[cli]==2.3.0" "openai-agents>=0.23.1" "psutil>=7.2.2"
```

## Running the MCP Server

From the project root, run:

```bash
uv run python src/mcp_servers/system/server.py
```

The server exposes the following tools:

| Tool | Description |
|---|---|
| `get_system_info` | Returns operating system and Python information. |
| `get_current_directory` | Returns the current working directory. |
| `list_processes` | Returns up to 10 running processes with their PIDs and names. |

The server uses standard input/output (stdio) for communication when running in stdio mode.

## Testing with MCP Inspector

MCP Inspector can be used to inspect the server, discover its tools, and execute them interactively.

Start the development inspector with:

```bash
uv run mcp dev src/mcp_servers/system/server.py
```

In the Inspector interface:

1. Connect to the server.
2. Open the Tools section.
3. Run `get_system_info`.
4. Run `get_current_directory`.
5. Run `list_processes`.
6. Verify the returned results.

**Note:** The current working directory depends on how the server process is launched. It is not necessarily the directory containing `server.py`.

## Configuring OpenRouter

The AI agent uses OpenRouter to access a compatible language model.

Set your API key as an environment variable.

### Windows PowerShell

```powershell
$env:OPENROUTER_API_KEY = "your_openrouter_api_key"
```

### Linux / macOS

```bash
export OPENROUTER_API_KEY="your_openrouter_api_key"
```

Replace the placeholder with your actual API key.

**Security:** Never commit API keys to Git or hard-code them in source files.

The API key configured this way is available only to the current terminal session.

## Running the AI Agent

After configuring the API key, run the agent from the project root:

```bash
uv run python src/agent/runner.py
```

The agent starts the MCP server as a subprocess, discovers its available tools, and can call them to answer questions about the computer.

The current example asks the agent to retrieve system information and the current working directory, then prints the final response.

## How It Works

The application consists of three main components:

1. **AI Agent:** Receives the user's request and determines which tools are needed.
2. **MCP Client:** Communicates with the MCP server, discovers available tools, and sends tool calls.
3. **MCP Server:** Executes the requested Python functions and returns their results.

### Request Flow

```text
User Request
     |
     v
AI Agent + Language Model
     |
     v
MCP Client
     |
     | stdio
     v
System MCP Server
     |
     v
Python Tools
     |
     v
Tool Results
     |
     v
AI Agent
     |
     v
Final Response
```

The model selects tools based on the user's request. The MCP server executes the corresponding functions, and the results are returned to the agent to generate a response.

## Important Notes

- The MCP server and AI agent run as separate processes.
- The agent requires a valid OpenRouter API key and network access.
- The model must support the API features required by the Agents SDK.
- The available model is configured in `src