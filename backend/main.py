import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from prometheus_fastapi_instrumentator import Instrumentator

from db.db import get_conn
from db.init_db import init_db
from ai_q_gen.question_generator import generate_question
from models.schemas import TopicChoice, AnswerRequest

# Init DB on start
init_db()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

Instrumentator().instrument(app).expose(app)


@app.get("/topics")
def get_topics():
    conn = get_conn()
    topics = conn.execute("SELECT id, name FROM topics").fetchall()
    return [{"id": t["id"], "name": t["name"]} for t in topics]

@app.post("/get_question")
def get_question(choice: TopicChoice):
    conn = get_conn()
    row = conn.execute("SELECT name FROM topics WHERE id = ?", (choice.topic_id,)).fetchone()
    if not row:
        return {"error": "Invalid topic"}
    sentence, choices, answer, hint = generate_question(row["name"])
    return {"sentence": sentence, "choices": choices, "answer": answer, "hint": hint}

@app.post("/submit_answer")
def submit_answer(req: AnswerRequest):
    correct = int(req.user_answer.strip().lower() == req.answer.strip().lower())
    conn = get_conn()
    conn.execute(
        "INSERT INTO game_history (topic_id, sentence, choices, answer, hint, user_answer, correct) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (req.topic_id, req.sentence, req.choices, req.answer, req.hint, req.user_answer, correct)
    )
    conn.commit()
    return {"correct": bool(correct)}

@app.get("/score/{topic_id}")
def get_score(topic_id: int):
    conn = get_conn()
    row = conn.execute(
        "SELECT SUM(correct) as s, COUNT(*) as n FROM game_history WHERE topic_id=?",
        (topic_id,)
    ).fetchone()
    return {"score": row["s"] or 0, "attempted": row["n"] or 0}
