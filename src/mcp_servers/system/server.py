import platform
from pathlib import Path

import psutil
from mcp.server import MCPServer


mcp = MCPServer("system-mcp")


@mcp.tool()
def get_system_info() -> dict:
    """Return basic operating system information."""
    return {
        "os": platform.system(),
        "os_version": platform.version(),
        "computer": platform.node(),
        "python_version": platform.python_version(),
    }


@mcp.tool()
def get_current_directory() -> str:
    """Return current working directory."""
    return str(Path.cwd())


@mcp.tool()
def list_processes() -> list[dict]:
    """List up to 10 running processes."""
    processes = []

    for process in psutil.process_iter(["pid", "name"]):
        try:
            processes.append(process.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

        if len(processes) >= 10:
            break

    return  processes


if __name__ == "__main__":
    mcp.run()