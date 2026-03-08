from typing import List, Dict

class ContextPack:
    def __init__(self, question: str, snippets: List[Dict]):
        self.question = question
        self.snippets = snippets

    def to_dict(self):
        return {
            "question": self.question,
            "context": self.snippets
        }

def create_context_pack(question, retrieved_context):
    return ContextPack(question, retrieved_context)