from models import Base, Question, GenerationNumberRequest, AnswerInput
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, desc, asc, func
from sqlalchemy.orm import sessionmaker, Session
from fastapi import FastAPI, HTTPException, Query, Depends, Body
import logging
import requests
import json

logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_handler = logging.FileHandler('app.log')

file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
#Подключение к базе
SQLALCHEMY_DATABASE_URI = "postgresql://postgres:Lilpeep228@localhost:5432/testps"
engine = create_engine(SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# В сервисе должно быть реализовано REST API, принимающее на вход POST запросы с содержимым вида {"questions_num": integer}  ;
# {
#     "questions_num": 2
# }

@app.post('/generation-num/', summary='Генерация вопросов для викторины',
          description='Создает новые вопросы для викторины '
                      'и возвращает предыдущий вопрос, если он есть в базе данных.', tags=['generation number'])
def generation_num(request_data: GenerationNumberRequest, db: Session = Depends(get_db)):
    """
    Генерация вопросов и ответов для викторины
    POST number
    GET text_question,text_answer
    """
    questions_num = request_data.questions_num
    # Пред вопрос
    if questions_num:
        previous_question = db.query(Question).order_by(Question.id.desc()).first()

        while True:
            url = f"https://jservice.io/api/random?count={questions_num}"
            response = requests.get(url)

            if response.status_code == 200:
                data = json.loads(response.text)

                for item in data:
                    question_text = item['question']
                    answer_text = item['answer']

                    existing_question = db.query(Question).filter(Question.text_question == question_text).first()

                    if existing_question is None:
                        new_question = Question(
                            text_question=question_text,
                            text_answer=answer_text
                        )
                        db.add(new_question)
                        db.commit()
                        logger.info('POST /generation-num/ successfully')
                        return {
                            "text_question": question_text,
                            "text_answer": answer_text,
                            "previous_question": {
                                "text_question": previous_question.text_question,
                                "text_answer": previous_question.text_answer
                            } if previous_question else {}
                        }
            else:
                # logger.error(f'Error request {response.status_code}')
                return f"error: {response.status_code}"
    else:
        # logger.error(f'Error questions_num > 0')
        return {"error": "Введите число больше 0"}


@app.get('/get-random-question/', summary='Получение случайного вопроса для викторины', tags=['quiz game'])
def get_random_question(db: Session = Depends(get_db)):
    """
    Получение случайного вопроса для викторины
    GET
    """
    random_question = db.query(Question).order_by(func.random()).first()

    if not random_question:
        return HTTPException(status_code=404, detail="Вопросы закончились")

    logging.info("GET /get-random-question/ successfully")
    return {
        "text_question": random_question.text_question,
        "question_id": random_question.id
    }


# http://127.0.0.1:8000/submit-answer/?q=13
# Canal Zone
@app.post('/submit-answer/', summary='Отправка ответа на вопрос', tags=['quiz game'])
def submit_answer(answer_input: AnswerInput, q: int = Query(description="ID вопроса", default=None),
                  db: Session = Depends(get_db)):
    """
    Отправка ответа на вопрос
    POST через аргумент q
    """

    question = db.query(Question).filter(Question.id == q).first()

    if not question:
        return HTTPException(status_code=404, detail="Вопрос не найден")

    user_answer = answer_input.answer.lower()
    correct_answer = question.text_answer.lower()
    logging.info("POST /submit-answer/ successfully")

    if user_answer == correct_answer:
        return {"message": "Правильно!"}
    else:
        return {"message": "Неправильно!"}
