class ValidatorAgent:
    def validate(self, answer):
        return len(answer.strip()) != 0
    