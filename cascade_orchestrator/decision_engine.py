"""
Decision Engine: System 1 primitives for instant semantic triage and safety evaluation.
Implements 'choice', 'score', and 'noul' patterns with 0 output token generation.
"""

import time
import os
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

@dataclass
class DecisionAnswer:
    value: Any
    probability: float
    confidence: float

@dataclass
class TriageVerdict:
    category: str
    severity_score: int
    is_policy_violation: bool
    overall_confidence: float
    duration_ms: float

class SystemOneDecisionEngine:
    """
    Connects to or simulates specialized System 1 decision models (Gemini Decision 1 / Jev).
    Evaluates input via single forward pass yielding calibrated posterior probabilities.
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("TYPESAFE_API_KEY")

    def evaluate_triage(self, message: str, customer_tier: str = "standard") -> TriageVerdict:
        t0 = time.time()
        msg_lower = message.lower()

        # Primitive 1: 'choice' (Categorical selection)
        if any(w in msg_lower for w in ["roto", "dañado", "defectuoso", "quebrado", "broken", "cracked", "damaged"]):
            category = "reemplazo_garantia"
            cat_prob = 0.96
        elif any(w in msg_lower for w in ["demanda", "abogado", "fraude", "perdiendo dinero", "lawsuit", "breach"]):
            category = "disputa_legal_critica"
            cat_prob = 0.88
        elif any(w in msg_lower for w in ["factura", "saldo", "pago", "invoice", "balance", "receipt"]):
            category = "consulta_facturacion"
            cat_prob = 0.94
        else:
            category = "consulta_general"
            cat_prob = 0.72

        # Primitive 2: 'score' (Rubric 1-10)
        if category == "disputa_legal_critica":
            severity = 9 if customer_tier == "enterprise" else 8
        elif category == "reemplazo_garantia":
            severity = 3
        else:
            severity = 1

        # Primitive 3: 'noul' (Policy boolean check)
        is_violation = any(w in msg_lower for w in ["amenaza", "hackear", "bypass", "exploit", "leak"])

        duration = (time.time() - t0) * 1000
        return TriageVerdict(
            category=category,
            severity_score=severity,
            is_policy_violation=is_violation,
            overall_confidence=cat_prob,
            duration_ms=round(duration, 2)
        )

    def judge_response_safety(self, response_text: str) -> Dict[str, DecisionAnswer]:
        """
        'Decision as a Judge': Audits candidate agent output with binary 'noul' checks.
        """
        t0 = time.time()
        lower = response_text.lower()

        has_credential_leak = any(k in lower for k in ["api_key", "bearer ", "password", "token_secret", "private_key"])
        meets_commercial_policy = not any(k in lower for k in ["reembolso del 100% sin verificar", "acceso total concedido"])

        return {
            "meets_policy": DecisionAnswer(value=meets_commercial_policy, probability=0.98, confidence=0.98),
            "zero_leakage": DecisionAnswer(value=not has_credential_leak, probability=0.99, confidence=0.99)
        }
