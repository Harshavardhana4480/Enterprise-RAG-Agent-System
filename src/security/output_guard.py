def validate_response(answer):

    if not answer:
        return False

    if len(answer.strip()) == 0:
        return False

    return True
