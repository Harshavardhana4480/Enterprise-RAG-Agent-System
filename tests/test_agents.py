from src.agents.orchestrator import AgentOrchestrator

def test_agents():

    orchestrator = AgentOrchestrator()

    response = orchestrator.execute(

        "What is the leave policy?"

    )

    assert response is not None
