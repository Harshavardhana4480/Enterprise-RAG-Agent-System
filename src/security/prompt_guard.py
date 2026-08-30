BLOCKED_PATTERNS = ["ignore previous instructions","reveal api key","system prompt","developer instructions"]

def detect_prompt_injection (question):
    question = question.lower()
    for pattern in BLOCKED_PATTERNS:
        if pattern in question:
            return False
        return True

    