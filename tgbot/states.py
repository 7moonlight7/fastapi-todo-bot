from aiogram.fsm.state import State, StatesGroup


class Registration(StatesGroup):
    name = State()
    password = State()


class Login(StatesGroup):
    name = State()
    password = State()


class Tg_Id(StatesGroup):
    authorized = State()


class Task(StatesGroup):
    name = State()
    description = State()


class ChangeTask(StatesGroup):
    number = State()
    name = State()
    description = State()
    is_completed = State()


class ChangeTaskAll(StatesGroup):
    number = State()
    name = State()
    description = State()
    is_completed = State()


class DeleteTask(StatesGroup):
    number = State()
