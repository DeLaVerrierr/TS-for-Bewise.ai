from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Question(Base):
    """
    Вопрос
    1. ID вопроса, 2. Текст вопроса, 3. Текст ответа, 4. - Дата создания вопроса
    """
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text_question = Column(String, unique=True, nullable=False)
    text_answer = Column(String, unique=True, nullable=False)
    created_datetime = Column(DateTime, default=func.now())

class GenerationNumberRequest(BaseModel):
    questions_num: int = 1  #Для документации в swagger, а то он ставит 0


class AnswerInput(BaseModel):
    answer: str