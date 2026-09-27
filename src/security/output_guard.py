def validate_output(answer: str) -> bool:

    if not answer:
        return False

    return len(answer.strip()) != 0
