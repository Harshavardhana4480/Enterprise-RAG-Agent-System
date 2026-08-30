from src.retrieval.query_embedding import generate_query_embedding
from src.retrieval.retriever import retrieve_documents
from src.retrieval.context_builder import build_context
from src.rag.response_formatter import format_response

from src.rag.prompt_builder import build_prompt
from src.rag.llm_service import generate_answer

def ask_question(question):
    query_embedding = generate_query_embedding(question)
    retrieve_results = retrieve_documents(query_embedding)

    context = build_context(retrieve_results)

      # Handling Missing Context
    if not context.strip():
        return (
            "No relevant information "
            "was found in the uploaded documents."
        )
    
    prompt = build_prompt(context, question)

    answer = generate_answer(prompt)

    return format_response(answer)

    retrieve_results = retrieve_documents(query_embedding)

    print("\nRETRIEVED RESULTS:")
    print(retrieve_results)
    context = build_context(retrieve_results)

    print("\nBUILT CONTEXT:")
    print(context)

# if not context or not context.strip():
# return(
# "I could not find this information "
# "in the uploaded documents."
# )