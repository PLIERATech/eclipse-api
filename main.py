from fastapi import *
from typing import Annotated
from fastapi.openapi.utils import get_openapi
import uvicorn
from pydantic import BaseModel
from sqlalchemy import *
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

#// Лист тегов в документации
tag_list = [
    "Граждане 🤵",
    "База данных 🗃️",
    "Root"
]

#// Движок для БД
engine = create_async_engine('sqlite+aiosqlite:///eclipseid.db')
new_session = async_sessionmaker(engine, expire_on_commit=False)

#// Сессия в БД
async def get_session():
    async with new_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]
class Base(DeclarativeBase):
    pass

#// БД
class EclipseID(Base):
    __tablename__ = "citizens"

    id: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[str] = mapped_column(unique=True)
    dsc_id: Mapped[int] = mapped_column(unique=True)
    role: Mapped[str]
    passport: Mapped[str] = mapped_column(unique=True)

#// Приложение АПИ
app = FastAPI()

#* Развернуть БД
@app.post('/setup_db', tags=[tag_list[1]], summary="Развернуть БД")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"status": True, "message": "База данных успешно развёрнута!"}

#. 0 страница
@app.get("/", tags=[tag_list[2]])
async def main_page():
    return "EclipseID API v0.0.1"

#. Список всех граждан
@app.get("/citizens", tags=[tag_list[0]], summary="Получить открытый список граждан")
async def get_citizens(session: SessionDep):
    query = select(EclipseID)
    result = await session.execute(query)
    return result.scalars().all()

#. Получить гражданина по никнейму
@app.get("/citizens/nickname/{nickname}", tags=[tag_list[0]], summary="Получить гражданина по никнейму")
async def get_citizens(session: SessionDep, nickname: str):
    query = select(EclipseID).where(EclipseID.nickname == nickname)
    result = await session.execute(query)
    return result.scalars().all()

#. Получить гражданина по Discord ID
@app.get("/citizens/dsc_id/{dsc_id}", tags=[tag_list[0]], summary="Получить гражданина по Discord ID")
async def get_citizens(session: SessionDep, dsc_id: int):
    query = select(EclipseID).where(EclipseID.dsc_id == dsc_id)
    result = await session.execute(query)
    return result.scalars().all()

#. Получить гражданина по паспорту
@app.get("/citizens/passport/{passport}", tags=[tag_list[0]], summary="Получить гражданина по паспорту")
async def get_citizens(session: SessionDep, passport: str):
    query = select(EclipseID).where(EclipseID.passport == passport)
    result = await session.execute(query)
    return result.scalars().all()

#// Пайдентик переменных для нового гражданина
class NewCitizen(BaseModel):
    nickname: str
    dsc_id: int
    role: str
    passport: str
class NewCitizenSchema(NewCitizen):
    id: int

#* Добавть нового гражданина
@app.post("/citizens", tags=[tag_list[0]], summary="Добавить нового гражданина")
async def add_citizen(new_citizen: NewCitizen, session: SessionDep):
    added_citizen = EclipseID(
        nickname=new_citizen.nickname,
        dsc_id=new_citizen.dsc_id,
        role=new_citizen.role,
        passport= new_citizen.passport
    )
    session.add(added_citizen)
    await session.commit()
    return {"status": True, "message": "Гражданин внесён в реестр!"}


#? Кастомная страница документации
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="ECLIPSEID API",
        version="0.0.1",
        description="Докуменация по **API Экосистемы ECLIPSEID**",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema
app.openapi = custom_openapi


# #// Инициализация АПИ
# if __name__ == "__main__":
#     uvicorn.run("main:app", reload=True, port=1000, host="0.0.0.0")

#// Инициализация АПИ
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)