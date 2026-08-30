
def format_response(answer):

    if answer is None:
        return "No response was generated."

    return answer.strip()