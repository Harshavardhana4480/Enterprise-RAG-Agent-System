class ValidatorAgent:
    def validate(self, answer):
        if len(answer.strip())==0:
            return False
        return True
    