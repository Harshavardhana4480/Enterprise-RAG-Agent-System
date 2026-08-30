from src.rag.llm_service import generate_answer
from src.rag.prompt_builder import build_prompt
from src.retrieval.context_builder import build_context

class ReasoningAgent:

    def reason(self, retrieval_results, question):

        # Build context from the retrieved document chunks
        context = build_context(retrieval_results)

        # Handle cases where no relevant documents are retrieved
        if not context.strip():
            return (
                "I could not find this information "
                "in the uploaded documents."
            )

        # Build the prompt using the retrieved context and user question
        prompt = build_prompt(context, question)

        # Generate the final answer using the LLM
        return generate_answer(prompt)