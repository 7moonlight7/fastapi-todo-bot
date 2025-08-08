from typing import List
from sqlalchemy import String, ForeignKey, create_engine
from sqlalchemy.orm import mapped_column, Mapped, relationship, declarative_base, sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column()
    name: Mapped[str] = mapped_column(String(10))
    password: Mapped[int] = mapped_column()
    tasks: Mapped[List["Task"]] = relationship(back_populates='user')


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    task_name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    is_completed: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    task_number: Mapped[int] = mapped_column(default=0)
    user: Mapped['User'] = relationship(back_populates='tasks')
