# -*- coding: utf-8 -*-
from client import OpenClawGenParkDeepAuditor

def main():
    auditor = OpenClawGenParkDeepAuditor()
    print("=== OpenClaw GenPark Deep Trajectory Auditor ===")

    # Simulated trapped agent in infinite search retry loop
    stuck_agent_trajectory = [
        {"step": 1, "action": "scrape", "tool": "web_fetch"},
        {"step": 2, "action": "parse", "tool": "html_parser"},
        {"step": 3, "action": "scrape", "tool": "web_fetch"},
        {"step": 4, "action": "parse", "tool": "html_parser"},
        {"step": 5, "action": "scrape", "tool": "web_fetch"},
        {"step": 6, "action": "parse", "tool": "html_parser"}
    ]

    report = auditor.audit_trajectory(stuck_agent_trajectory)
    print(f"Audit Status: {report['status']}")
    print(f"Anomaly Score: {report['anomaly_score']}")
    print(f"Infinite Loop: {report['has_infinite_loop']}")
    print(f"Action Recommendation: {report['recommendation']}")

if __name__ == "__main__":
    main()
