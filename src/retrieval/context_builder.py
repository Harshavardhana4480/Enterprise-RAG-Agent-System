def build_context(results):

    documents = results.get("documents", [[]])[0]

    if not documents:
        return ""

    context = ""

    for document in documents:
        context += document
        context += "\n\n"

    return context