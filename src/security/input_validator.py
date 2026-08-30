def validate_question(question):
    if not question:
        raise ValueError("Question cannot be empty")
    if len(question.strip())==0:
        raise ValueError ("Question cannot contain only spaces")
    if len(question)>500:
        raise ValueError ("Question exceeds maximum length.")
    return True
