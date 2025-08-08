from pydantic import BaseModel


class UserRegister(BaseModel):
    tg_id: int
    name: str
    password: str


class UserLogin(BaseModel):
    tg_id: int
    name: str
    password: str


class AddTask(BaseModel):
    name: str
    description: str
    user_id: int


class Tg_Id(BaseModel):
    tg_id: int


class ChangeTaskName(BaseModel):
    tg_id: int
    task_number: int
    new_task_name: str


class ChangeTaskDescription(BaseModel):
    tg_id: int
    task_number: int
    new_task_description: str


class ChangeTaskStatus(BaseModel):
    tg_id: int
    task_number: int
    status: bool


class ChangeTaskAll(BaseModel):
    tg_id: int
    task_number: int
    new_task_name: str
    new_task_description: str
    status: bool


class DeleteTask(BaseModel):
    tg_id: int
    task_number: int
