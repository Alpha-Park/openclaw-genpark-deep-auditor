# -*- coding: utf-8 -*-
import sys, json
from client import OpenClawGenParkDeepAuditor

auditor = OpenClawGenParkDeepAuditor()

def run_tool(name, args):
    if name == "audit_trajectory":
        traj = args.get("trajectory", [])
        return auditor.audit_trajectory(traj)
    else:
        raise ValueError(f"Unknown tool: {name}")

from typing import Any, Dict, List, Optional

try:
    from mcp.server.fastmcp import FastMCP
except ImportError as exc:
    raise SystemExit("MCP requires the mcp package. Run: python -m pip install -r requirements.txt") from exc

mcp = FastMCP('openclaw-genpark-deep-auditor')

@mcp.tool()
def audit_trajectory(trajectory: Optional[List[Dict[str, Any]]] = None) -> str:
    """Audit an agent trajectory for loops and state anomalies."""
    return json.dumps(run_tool('audit_trajectory', {'trajectory': trajectory if trajectory is not None else []}))

def main():
    if "--test" in sys.argv:
        print("[TEST] Running OpenClaw Deep Auditor Self-Test...")
        t_clean = [{"action": "read", "tool": "file"}, {"action": "parse", "tool": "json"}]
        res1 = auditor.audit_trajectory(t_clean)
        assert res1["has_anomalies"] is False
        t_loop = [{"action": "call", "tool": "A"}, {"action": "call", "tool": "B"},
                  {"action": "call", "tool": "A"}, {"action": "call", "tool": "B"},
                  {"action": "call", "tool": "A"}, {"action": "call", "tool": "B"}]
        res2 = auditor.audit_trajectory(t_loop)
        assert res2["has_infinite_loop"] is True
        print("[TEST] All tests passed successfully!")
        return

    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
