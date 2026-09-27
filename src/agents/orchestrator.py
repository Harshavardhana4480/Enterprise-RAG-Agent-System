from loguru import logger
from unstructured import documents

from src.agents.planner import PlannerAgent
from src.agents.reasoner import ReasoningAgent
from src.agents.retriever import RetrieverAgent
from src.agents.validator import ValidatorAgent


class AgentOrchestrator:

    def __init__(self):
        self.planner = PlannerAgent()
        self.retriever = RetrieverAgent()
        self.reasoner = ReasoningAgent()
        self.validator = ValidatorAgent()

    def execute(self, question):

        logger.info("RAG request started")

        logger.info("Planner started")

        plan = self.planner.create_plan(question)

        documents = self.retriever.retrieve(
            question,
            plan["max_documents"]
        )

        logger.info(
            "Retriever completed"
        )

        answer = self.reasoner.reason(
            documents,
            question
        )

        logger.info(
            "Reasoning completed"
        )

        logger.info(
            f"Generated answer type: {type(answer)}"
        )

        logger.info(
            f"Generated answer: {repr(answer)}"
        )

        if not self.validator.validate(answer):

            logger.warning(
                "Answer validation failed"
            )

            return "Unable to validate the answer."

        logger.info(
            "RAG request completed successfully"
        )

        return answer