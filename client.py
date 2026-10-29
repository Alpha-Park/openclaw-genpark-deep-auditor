# -*- coding: utf-8 -*-
"""
OpenClaw GenPark Deep Auditor
Standard Library only: math, collections, typing.
Monitors multi-hop agent execution trajectories for cyclic loops,
state transition anomalies, and trajectory divergence.
"""

from typing import Dict, List, Any

class OpenClawGenParkDeepAuditor:
    def __init__(self, max_allowed_loop_repetition: int = 2):
        self.max_allowed_loop_repetition = max_allowed_loop_repetition

    def audit_trajectory(self, trajectory: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        trajectory: list of {"step": 0, "action": "search", "tool": "google_search", "params_hash": "..."}
        """
        if not trajectory:
            return {"status": "CLEAN", "has_anomalies": False, "anomaly_score": 0.0}

        actions = [item.get("action", "") + ":" + item.get("tool", "") for item in trajectory]
        n = len(actions)

        # 1. Direct consecutive repetitions (e.g. search -> search -> search)
        consecutive_repeats = 0
        for i in range(1, n):
            if actions[i] == actions[i-1]:
                consecutive_repeats += 1

        # 2. Cycle detection (e.g., A -> B -> A -> B)
        detected_cycles = []
        for cycle_len in range(2, min(5, n // 2 + 1)):
            for i in range(n - 2 * cycle_len + 1):
                window1 = actions[i:i+cycle_len]
                window2 = actions[i+cycle_len:i+2*cycle_len]
                if window1 == window2:
                    detected_cycles.append({"cycle_pattern": window1, "start_step": i})

        # 3. Action diversity ratio (unique actions / total actions)
        diversity_ratio = round(len(set(actions)) / n, 3)

        # Composite anomaly score
        anomaly_score = 0.0
        anomaly_score += consecutive_repeats * 0.25
        anomaly_score += len(detected_cycles) * 0.35
        if diversity_ratio < 0.3 and n > 5:
            anomaly_score += 0.3
        anomaly_score = min(1.0, round(anomaly_score, 3))

        has_loop = len(detected_cycles) >= self.max_allowed_loop_repetition or consecutive_repeats >= 3

        status = "CLEAN"
        if anomaly_score >= 0.7: status = "CRITICAL_DRIFT"
        elif anomaly_score >= 0.4: status = "SUSPICIOUS_LOOP"

        return {
            "status": status,
            "has_anomalies": anomaly_score >= 0.4,
            "anomaly_score": anomaly_score,
            "has_infinite_loop": has_loop,
            "consecutive_repeat_count": consecutive_repeats,
            "detected_cycles": detected_cycles[:3],
            "action_diversity_ratio": diversity_ratio,
            "recommendation": "TERMINATE_EXECUTION" if has_loop else "CONTINUE"
        }
