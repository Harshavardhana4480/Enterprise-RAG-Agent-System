MAX_QUERY_LENGTH = 2000


def validate_user_query(question: str) -> tuple[bool, str]:

    # Check whether the input is empty
    if not question or not question.strip():

        return False, (
            "Please enter a question."
        )

    # Check maximum query length
    if len(question) > MAX_QUERY_LENGTH:

        return False, (
            f"Your question is too long. "
            f"Please keep it below "
            f"{MAX_QUERY_LENGTH} characters."
        )

    return True, ""