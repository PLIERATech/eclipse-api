from fastapi import *
from fastapi.openapi.utils import get_openapi
import uvicorn
from pydantic import BaseModel

app = FastAPI()

tag_list = [
    "Граждане 🤵"
]

citizens = [
    {
        "id": 1,
        "nickname": "PRISTORoff0",
        "dsc_id": 436507782263603200,
        "role": "emperror",
        "passport": "GSTDJRU71623U92K"
    },
    {
        "id": 2,
        "nickname": "_Tecxas",
        "dsc_id": 839340956988866580,
        "role": "chancellor",
        "passport": "SLAOP947ABSH3NCD"
    }
]

#. Список всех граждан
@app.get("/citizens", tags=[tag_list[0]], summary="Получить открытый список граждан 📃")
def get_citizens():
    return citizens

#. Найти гражданина по никнейму
@app.get("/citizens/nickname/{nickname}", tags=[tag_list[0]], summary="Найти гражданина по Никнейму 🏷️")
def find_citizen_nickname(nickname: str):
    for citizen_bynick in citizens:
        if citizen_bynick["nickname"] == nickname:
            return citizen_bynick
    raise HTTPException(status_code=404)
    
#. Найти гражданина по Discord ID
@app.get("/citizens/id/{dsc_id}", tags=[tag_list[0]], summary="Найти гражданина по Discord ID 📋")
def find_citizen_id(dsc_id: int):
    for citizen_byid in citizens:
        if citizen_byid["dsc_id"] == dsc_id:
            return citizen_byid
    raise HTTPException(status_code=404)

#. Найти гражданина по номеру паспорта
@app.get("/citizens/passport/{passport}", tags=[tag_list[0]], summary="Найти гражданина по номеру паспорта 📓")
def find_citizen_nickname(passport: str):
    for citizen_bypassport in citizens:
        if citizen_bypassport["passport"] == passport:
            return citizen_bypassport
    raise HTTPException(status_code=404)

class NewCitizen(BaseModel):
    nickname: str
    dsc_id: int
    role: str
    passport: str

#* Добавть нового гражданина
@app.post("/citizens", tags=[tag_list[0]], summary="Добавить нового гражданина 📝")
def add_citizen(new_citizen: NewCitizen):
    citizens.append({
        "nickname": new_citizen.nickname,
        "dsc_id": new_citizen.dsc_id,
        "role": new_citizen.role,
        "passport": new_citizen.passport
    })
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

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)