from pydantic import BaseModel

class TopicChoice(BaseModel):
    topic_id: int

class AnswerRequest(BaseModel):
    topic_id: int
    sentence: str
    choices: str
    answer: str
    hint: str
    user_answer: str
