from pydantic import BaseModel
class QuestionSchema(BaseModel):
    question: str
    class Config:
        extra = 'forbid'