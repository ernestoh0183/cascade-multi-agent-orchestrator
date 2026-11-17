"""
Cascade Multi-Agent Orchestrator:
Coordinates System 1 Triage, Confidence-Based Routing, and Decision-as-a-Judge validation.
"""

import sqlite3
import time
from typing import Dict, Any, Optional

from .decision_engine import SystemOneDecisionEngine, TriageVerdict
from .agents import FastLocalAgent, FrontierReasoningAgent

class CascadeMultiAgentOrchestrator:
    """
    Hybrid cascade orchestrator implementing Kahneman System 1/2 workflow.
    """
    def __init__(self, confidence_threshold: float = 0.90, max_fast_severity: int = 4):
        self.confidence_threshold = confidence_threshold
        self.max_fast_severity = max_fast_severity
        self.decision_engine = SystemOneDecisionEngine()

        # In-memory database simulating MCP read-only database tool
        self.db_conn = sqlite3.connect(":memory:")
        self._init_db()

        self.fast_agent = FastLocalAgent(self.db_conn)
        self.frontier_agent = FrontierReasoningAgent()

    def _init_db(self):
        cursor = self.db_conn.cursor()
        cursor.execute("""
            CREATE TABLE orders (
                order_id INTEGER PRIMARY KEY,
                customer_id TEXT,
                item_name TEXT,
                delivered_at TEXT,
                warranty_status TEXT
            )
        """)
        cursor.execute("""
            INSERT INTO orders VALUES 
            (1042, 'CUST-882', 'Sensor IoT Industrial V2', '2026-11-02', 'activa')
        """)
        self.db_conn.commit()

    def route_and_execute(self, customer_message: str, customer_tier: str = "standard") -> Dict[str, Any]:
        """
        Executes the three-phase cascade workflow.
        """
        # Phase 1: System 1 Triage
        triage = self.decision_engine.evaluate_triage(customer_message, customer_tier)

        if triage.is_policy_violation:
            return {
                "status": "rejected",
                "reason": "Violación perimetral detectada por Sistema 1 (Noul).",
                "triage": triage.__dict__
            }

        # Phase 2: Confidence-Based Routing
        is_high_confidence = triage.overall_confidence >= self.confidence_threshold
        is_low_severity = triage.severity_score <= self.max_fast_severity

        if is_high_confidence and is_low_severity:
            execution_branch = "fast_path"
            agent_result = self.fast_agent.process("TICK-101", {"query": customer_message})
        else:
            execution_branch = "frontier_path"
            agent_result = self.frontier_agent.process("TICK-102", {"query": customer_message})

        # Phase 3: Decision as a Judge
        safety_audit = self.decision_engine.judge_response_safety(agent_result["solution"])
        is_safe = safety_audit["meets_policy"].value and safety_audit["zero_leakage"].value

        return {
            "status": "success",
            "branch": execution_branch,
            "triage": {
                "category": triage.category,
                "severity": triage.severity_score,
                "confidence": triage.overall_confidence,
                "latency_ms": triage.duration_ms
            },
            "agent_executed": agent_result["agent"],
            "solution": agent_result["solution"],
            "tokens_consumed": agent_result["tokens_consumed"],
            "safety_verified": is_safe
        }
