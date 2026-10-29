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

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            res = run_tool(req.get("name"), req.get("arguments", {}))
            print(json.dumps({"jsonrpc": "2.0", "id": req.get("id"), "result": res}))
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32603, "message": str(e)}}))
        sys.stdout.flush()

if __name__ == "__main__":
    main()
