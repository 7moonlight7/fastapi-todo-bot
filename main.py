from http.client import HTTPException
from sqlalchemy import func
from fastapi import FastAPI, Depends, Query
from database.models import Base
from sqlalchemy.orm import Session
from database.database import engine, SessionLocal
import hashlib
from pydantic_model import UserRegister, UserLogin, AddTask, ChangeTaskName, ChangeTaskDescription, \
    ChangeTaskStatus, ChangeTaskAll, DeleteTask
from database.models import User, Task


Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_dp():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/registration/')
def register(data: UserRegister, db: Session = Depends(get_dp)):
    hashed_password = hashlib.sha256(data.password.encode()).hexdigest()
    user = User(tg_id=data.tg_id, name=data.name, password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {'success': True, 'user_id': user.id}


@app.post('/login/')
def login(data: UserLogin, db: Session = Depends(get_dp)):
    user = db.query(User).filter(User.name == data.name).first()
    if not user:
        raise HTTPException(status_code=400, detail="Пользователь не найден")

    hashed_password = hashlib.sha256(data.password.encode()).hexdigest()
    if hashed_password != user.password:
        raise HTTPException(status_code=400, detail="Неверный пароль")

    if user.tg_id != data.tg_id:
        user.tg_id = data.tg_id
        db.commit()

    return {'success': True, 'user_id': user.id}


@app.post('/add_task/')
def add_task(data: AddTask, db: Session = Depends(get_dp)):
    user = db.query(User).filter(User.id == data.user_id).first()

    if user is None:
        raise HTTPException(status_code=400, detail='Пользователь не найден')

    max_task_number = db.query(func.max(Task.task_number)).filter(Task.user_id == user.id).scalar()
    if max_task_number is None:
        max_task_number = -1

    task = Task(task_name=data.name, description=data.description, user_id=user.id, task_number=max_task_number + 1)

    db.add(task)
    db.commit()
    db.refresh(task)
    return {'success': True, 'task_id': task.user_id}


@app.get('/get_list/')
def show_list(user_id: int = Query(...), db: Session = Depends(get_dp)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail='Пользователь не найден')

    return user.tasks


@app.post('/change_name/')
def change_name(data: ChangeTaskName, db: Session = Depends(get_dp)):
    user = db.query(User).filter(User.tg_id == data.tg_id).first()
    if not user:
        raise HTTPException(status_code=400, detail='Пользователь не найден')

    task = db.query(Task).filter(Task.task_number == data.task_number, Task.user_id == user.id).first()
    if not task:
        raise HTTPException(status_code=400, detail='Задача не найдена')

    task.task_name = data.new_task_name
    db.commit()

    return {'success': True, 'new_task_name': data.new_task_name}


@app.post('/change_description/')
def change_name(data: ChangeTaskDescription, db: Session = Depends(get_dp)):
    user = db.query(User).filter(User.tg_id == data.tg_id).first()
    if not user:
        raise HTTPException(status_code=400, detail='Пользователь не найден')

    task = db.query(Task).filter(Task.task_number == data.task_number, Task.user_id == user.id).first()
    if not task:
        raise HTTPException(status_code=400, detail='Задача не найдена')

    task.description = data.new_task_description
    db.commit()

    return {'success': True, 'new_task_name': data.new_task_description}


@app.post('/change_status/')
def change_name(data: ChangeTaskStatus, db: Session = Depends(get_dp)):
    user = db.query(User).filter(User.tg_id == data.tg_id).first()
    if not user:
        raise HTTPException(status_code=400, detail='Пользователь не найден')

    task = db.query(Task).filter(Task.task_number == data.task_number, Task.user_id == user.id).first()
    if not task:
        raise HTTPException(status_code=400, detail='Задача не найдена')

    task.is_completed = data.status
    db.commit()

    return {'success': True, 'new_task_status': data.status}


@app.post('/change_all/')
def change_name(data: ChangeTaskAll, db: Session = Depends(get_dp)):
    user = db.query(User).filter(User.tg_id == data.tg_id).first()
    if not user:
        raise HTTPException(status_code=400, detail='Пользователь не найден')

    task = db.query(Task).filter(Task.task_number == data.task_number, Task.user_id == user.id).first()
    if not task:
        raise HTTPException(status_code=400, detail='Задача не найдена')

    task.task_name = data.new_task_name
    task.description = data.new_task_description
    task.is_completed = data.status
    db.commit()

    return {'success': True, 'new_task_name': data.status}


@app.post('/delete/')
def change_name(data: DeleteTask, db: Session = Depends(get_dp)):
    user = db.query(User).filter(User.tg_id == data.tg_id).first()
    if not user:
        raise HTTPException(status_code=400, detail='Пользователь не найден')

    task = db.query(Task).filter(Task.task_number == data.task_number, Task.user_id == user.id).first()
    if not task:
        raise HTTPException(status_code=400, detail='Задача не найдена')
    else:
        db.delete(task)
        db.commit()

    return {'success': True}
