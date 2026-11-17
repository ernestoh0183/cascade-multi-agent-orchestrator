"""
Cascade Multi-Agent Orchestrator
Hybrid System 1 (Decision Models) + System 2 (Reasoning Models) Architecture.
"""

from .decision_engine import SystemOneDecisionEngine, TriageVerdict, DecisionAnswer
from .agents import FastLocalAgent, FrontierReasoningAgent
from .orchestrator import CascadeMultiAgentOrchestrator

__version__ = "1.0.0"
__all__ = [
    "SystemOneDecisionEngine",
    "TriageVerdict",
    "DecisionAnswer",
    "FastLocalAgent",
    "FrontierReasoningAgent",
    "CascadeMultiAgentOrchestrator",
]
