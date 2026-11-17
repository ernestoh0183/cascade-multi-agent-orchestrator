#!/usr/bin/env python3
"""
Interactive demonstration of Cascade Multi-Agent Orchestrator.
Runs two standard enterprise scenarios: routine warranty claim vs critical dispute.
"""

import json
import sys
import os

# Add parent dir to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from cascade_orchestrator import CascadeMultiAgentOrchestrator

def main():
    orchestrator = CascadeMultiAgentOrchestrator()

    print("=" * 70)
    print("CASCADE MULTI-AGENT ORCHESTRATOR DEMO (4Ruy.com)")
    print("=" * 70)

    # Scenario 1
    print("\n>>> ESCENARIO 1: RECLAMO DE GARANTÍA RUTINARIO (Fast Path)")
    msg1 = "El sensor IoT llegó quebrado en la caja cuando lo recibí el 2 de noviembre."
    print(f"Mensaje entrante: \"{msg1}\"")
    res1 = orchestrator.route_and_execute(msg1, customer_tier="standard")
    print(json.dumps(res1, indent=2, ensure_ascii=False))

    # Scenario 2
    print("\n>>> ESCENARIO 2: DISPUTA CONTRACTUAL ENTERPRISE (Frontier Reasoning Path)")
    msg2 = "Llevamos 3 días con el sistema caído perdiendo miles de dólares; si no resuelven hoy cancelamos el contrato y procederemos con nuestros abogados."
    print(f"Mensaje entrante: \"{msg2}\"")
    res2 = orchestrator.route_and_execute(msg2, customer_tier="enterprise")
    print(json.dumps(res2, indent=2, ensure_ascii=False))

    print("\n" + "=" * 70)
    print("Demo completada con éxito.")

if __name__ == "__main__":
    main()
