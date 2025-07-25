from fastapi import FastAPI, Depends, HTTPException, APIRouter, Request
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv  

from app.models import Base
from app import models, schemas, crud
from app.database import Base, engine, SessionLocal
from app.assistant.assistant import ask_assistant

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))
Base.metadata.create_all(bind=engine)

router = APIRouter()
app = FastAPI(title="Todo API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", tags=["root"])
def read_root():
    return {"message": "API is up"}

@app.get("/todos", response_model=list[schemas.TodoOut])
def list_todos(db: Session = Depends(get_db)):
    return crud.get_todos(db)

@app.post("/todos", response_model=schemas.TodoOut, status_code=201)
def add_todo(todo_in: schemas.TodoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db, todo_in)

@app.put("/todos/{todo_id}", response_model=schemas.TodoOut)
def edit_todo(todo_id: int, todo_in: schemas.TodoBase, db: Session = Depends(get_db)):
    todo = crud.update_todo(db, todo_id, todo_in)
    if not todo:
        raise HTTPException(404, "Todo not found")
    return todo

@app.delete("/todos/{todo_id}", status_code=204)
def remove_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = crud.delete_todo(db, todo_id)
    if not todo:
        raise HTTPException(404, "Todo not found")

@app.post("/ask-assistant")
async def ask_assistant(request: Request):
    data = await request.json()
    prompt = data.get("prompt")
    if not prompt:
        raise HTTPException(400, "Prompt is required")
    return {"response": ask_assistant(prompt)}