from core.orchestrator import AthenaOrchestrator


athena = AthenaOrchestrator()

response = athena.process_request(
    "Explain what a derivative means in calculus."
)

print(response)