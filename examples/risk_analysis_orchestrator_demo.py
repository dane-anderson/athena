from core.orchestrator import AthenaOrchestrator


athena = AthenaOrchestrator()


result = athena.process_request(
    "Analyze Apple risk"
)


print(result)