def build_prompt (context, question):
    prompt =    f"""
You are an Enterprise AI Assistant.

Answer ONLY using the supplied context.

If the answer is not available,
reply:

"I could not find this information in the uploaded documents."

Context:
{context}

Question:
{question}

Answer:
"""

    return prompt
