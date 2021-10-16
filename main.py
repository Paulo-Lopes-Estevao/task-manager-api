from typing import List, Optional
import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import databases
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.coercions import _deep_is_literal
from sqlalchemy.sql.expression import null, true
from sqlalchemy.sql.functions import current_timestamp
from pydantic import BaseModel
from pydantic import BaseConfig
BaseConfig.arbitrary_types_allowed = True


DATABASE_URL = "sqlite:///./task.db"


database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

persons = sqlalchemy.Table(
    "person",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer,
                      primary_key=True, autoincrement=true),
    sqlalchemy.Column("name", sqlalchemy.String, nullable=true),
    sqlalchemy.Column("email", sqlalchemy.VARCHAR(125), nullable=true),
    sqlalchemy.Column("photo", sqlalchemy.Text, nullable=true),
    sqlalchemy.Column("updated", sqlalchemy.DATETIME,
                      onupdate=current_timestamp),
    sqlalchemy.Column("created", sqlalchemy.DATETIME,
                      onupdate=current_timestamp),
)

task = sqlalchemy.Table(
    "task",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer,
                      primary_key=True, autoincrement=true),
    sqlalchemy.Column("title", sqlalchemy.String(50), nullable=true),
    sqlalchemy.Column("data", sqlalchemy.DATE, nullable=true),
    sqlalchemy.Column("state", sqlalchemy.BOOLEAN),
    sqlalchemy.Column("updated", sqlalchemy.DATETIME, default=current_timestamp,
                      nullable=true),
    sqlalchemy.Column("created", sqlalchemy.DATETIME,
                      default=current_timestamp, nullable=true),
)


engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)


class PersonOut(BaseModel):
    id: int
    name: str
    email: str
    photo: str
    updated: str
    created: str


class PersonInp(BaseModel):
    name: str
    email: str
    photo: str


class TaskInp(BaseModel):
    title: Optional[str] =None
    data: Optional[datetime.date] = None
    state: Optional[bool]=None

    class Config:
        orm_mode = True



class TaskOut(BaseModel):
    id: int
    title: str
    data: datetime.date
    state: bool
    updated: datetime.datetime
    created: datetime.datetime

    class Config:
        orm_mode = True


app = FastAPI(
    version="0.1",
    title="SNIR Teste Front-End",
    redoc_url=None
    
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/task", response_model_exclude_defaults=TaskOut,
name="Task",
tags=["TASK"]
)
async def read_task():
    """
        Listagem das Tasks
    """
    query = task.select()
    return await database.fetch_all(query)


@app.post("/task", response_model_exclude_defaults=TaskInp,
name="Task",
tags=["TASK"]
)
async def create_task(tasks: TaskInp):
    """
        Criação das Tasks
    """
    query = task.insert().values(title=tasks.title,data=tasks.data,state=True,updated=datetime.datetime.now(),created=datetime.datetime.now())
    last_record_task = await database.execute(query)
    return {**tasks.dict()}

@app.put("/task/{id_task}", response_model_exclude_defaults=TaskInp,
name="Task",
tags=["TASK"]
)
async def create_task(id_task: int,tasks: TaskInp):
    """
        Actualização das Tasks
    """
    query = task.update().where(task.c.id==id_task).values(**tasks.dict())
    last_record_task = await database.execute(query)
    return {**tasks.dict()}


@app.delete("/task/{id_task}", response_model_exclude_defaults=TaskInp,
name="Task",
tags=["TASK"]
)
async def create_task(id_task: int,tasks: TaskInp):
    """
        Apagar a Task
    """
    query = task.delete().where(task.c.id==id_task)
    last_record_task = await database.execute(query)
    return {**tasks.dict()}