from loguru import logger

from src.rag.llm_service import generate_answer
from src.rag.prompt_builder import build_prompt
from src.retrieval.context_builder import build_context


class ReasoningAgent:

    def reason(self, retrieval_results, question):

        logger.info(
            f"REASONER QUESTION: {repr(question)}"
        )

        # Build context
        context = build_context(retrieval_results)

        logger.info(
            f"CONTEXT LENGTH: {len(context)}"
        )

        logger.info(
            f"CONTEXT PREVIEW: {context[:500]!r}"
        )

        # Handle no retrieved context
        if not context.strip():
            logger.warning(
                "No context available for reasoning."
            )

            return (
                "I could not find this information "
                "in the uploaded documents."
            )

        # Build prompt
        prompt = build_prompt(
            context,
            question
        )

        logger.info(
            f"PROMPT LENGTH: {len(prompt)}"
        )

        # Generate answer
        answer = generate_answer(prompt)

        logger.info(
            f"LLM ANSWER TYPE: {type(answer)}"
        )

        logger.info(
            f"LLM ANSWER LENGTH: {len(answer) if answer else 0}"
        )

        logger.info(
            f"LLM ANSWER: {repr(answer)}"
        )

        return answer