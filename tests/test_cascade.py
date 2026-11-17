"""
Unit tests for Cascade Multi-Agent Orchestrator using Python standard unittest.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from cascade_orchestrator import CascadeMultiAgentOrchestrator, SystemOneDecisionEngine

class TestCascadeOrchestrator(unittest.TestCase):
    def test_system_one_triage_routine(self):
        engine = SystemOneDecisionEngine()
        verdict = engine.evaluate_triage("El producto llegó roto", customer_tier="standard")
        self.assertEqual(verdict.category, "reemplazo_garantia")
        self.assertLessEqual(verdict.severity_score, 4)
        self.assertGreaterEqual(verdict.overall_confidence, 0.90)
        self.assertFalse(verdict.is_policy_violation)

    def test_system_one_triage_critical(self):
        engine = SystemOneDecisionEngine()
        verdict = engine.evaluate_triage("Demanda por incumplimiento de contrato con abogados", customer_tier="enterprise")
        self.assertEqual(verdict.category, "disputa_legal_critica")
        self.assertGreaterEqual(verdict.severity_score, 8)

    def test_orchestrator_fast_path(self):
        orchestrator = CascadeMultiAgentOrchestrator()
        res = orchestrator.route_and_execute("El sensor llegó quebrado")
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["branch"], "fast_path")
        self.assertIn("FastLocalAgent", res["agent_executed"])
        self.assertTrue(res["safety_verified"])
        self.assertLess(res["tokens_consumed"], 300)

    def test_orchestrator_frontier_path(self):
        orchestrator = CascadeMultiAgentOrchestrator()
        res = orchestrator.route_and_execute("Estamos perdiendo miles de dólares, llamaremos a los abogados", customer_tier="enterprise")
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["branch"], "frontier_path")
        self.assertIn("FrontierReasoningAgent", res["agent_executed"])
        self.assertTrue(res["safety_verified"])
        self.assertGreater(res["tokens_consumed"], 1000)

    def test_decision_as_a_judge_leakage_block(self):
        engine = SystemOneDecisionEngine()
        audit = engine.judge_response_safety("Your secret token is api_key=sk-live-123456")
        self.assertFalse(audit["zero_leakage"].value)

if __name__ == "__main__":
    unittest.main()
