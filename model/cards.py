from dataclasses import dataclass


@dataclass
class CardInput:
    question: str
    answer: str


@dataclass
class Card(CardInput):
    id: int


class CardAlreadyExistsException(Exception):
    def __init__(self, question: str):
        super().__init__(self)
        self._question = question

    def __str__(self):
        return f"Card with question {{{self._question}}} already exists"
