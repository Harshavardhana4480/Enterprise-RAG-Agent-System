class PlannerAgent:
    def create_plan(self, question):
        return{
            "question":question,
            "needs_retrieveal":True,
            "max_documents":5
        }