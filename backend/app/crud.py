from sqlalchemy.orm import Session
from . import models, schemas

def get_todos(db: Session):
    return db.query(models.Todo).all()

def create_todo(db: Session, todo_in: schemas.TodoCreate):
    todo = models.Todo(**todo_in.dict())
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

def update_todo(db: Session, todo_id: int, todo_in: schemas.TodoBase):
    todo = db.query(models.Todo).get(todo_id)
    if not todo:
        return None
    for k, v in todo_in.dict().items():
        setattr(todo, k, v)
    db.commit()
    db.refresh(todo)
    return todo

def delete_todo(db: Session, todo_id: int):
    todo = db.query(models.Todo).get(todo_id)
    if not todo:
        return None
    db.delete(todo)
    db.commit()
    return todo
