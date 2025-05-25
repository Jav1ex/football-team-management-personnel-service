from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from database 
import models, schemas
from datetime import date

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
jugadores_router = APIRouter(prefix="/jugadores", tags=["Jugadores"])
entrenadores_router = APIRouter(prefix="/entrenadores", tags=["Entrenadores"])
juega_en_router = APIRouter(prefix="/juega_en", tags=["JuegaEn"])
entrena_router = APIRouter(prefix="/entrena", tags=["Entrena"])

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Jugadores
@jugadores_router.post("/", response_model=schemas.Jugador)
async def create_jugador(jugador: schemas.JugadorCreate):
    data = jugador.dict()
    data["fecha_nac"] = date.fromisoformat(data["fecha_nac"])
    query = models.jugador.insert().values(**data)
    last_id = await database.execute(query)
    return {**jugador.dict(), "jugador_id": last_id}

@jugadores_router.get("/", response_model=List[schemas.Jugador])
async def read_jugadores():
    query = models.jugador.select()
    return await database.fetch_all(query)

@jugadores_router.get("/{jugador_id}", response_model=schemas.Jugador)
async def read_jugador(jugador_id: int):
    query = models.jugador.select().where(models.jugador.c.jugador_id == jugador_id)
    jugador = await database.fetch_one(query)
    if jugador is None:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return jugador

@jugadores_router.delete("/{jugador_id}")
async def delete_jugador(jugador_id: int):
    query = models.jugador.delete().where(models.jugador.c.jugador_id == jugador_id)
    result = await database.execute(query)
    return {"deleted": result}

@jugadores_router.put("/{jugador_id}", response_model=schemas.Jugador)
async def update_jugador(jugador_id: int, jugador: schemas.JugadorCreate):
    data = jugador.dict()
    data["fecha_nac"] = date.fromisoformat(data["fecha_nac"])
    query = models.jugador.update().where(models.jugador.c.jugador_id == jugador_id).values(**data)
    await database.execute(query)
    return {**jugador.dict(), "jugador_id": jugador_id}

# Entrenadores
@entrenadores_router.post("/", response_model=schemas.Entrenador)
async def create_entrenador(entrenador: schemas.EntrenadorCreate):
    data = entrenador.dict()
    data["fecha_nac"] = date.fromisoformat(data["fecha_nac"])
    query = models.entrenador.insert().values(**data)
    last_id = await database.execute(query)
    return {**entrenador.dict(), "entrenador_id": last_id}

@entrenadores_router.get("/", response_model=List[schemas.Entrenador])
async def read_entrenadores():
    query = models.entrenador.select()
    return await database.fetch_all(query)

@entrenadores_router.get("/{entrenador_id}", response_model=schemas.Entrenador)
async def read_entrenador(entrenador_id: int):
    query = models.entrenador.select().where(models.entrenador.c.entrenador_id == entrenador_id)
    entrenador = await database.fetch_one(query)
    if entrenador is None:
        raise HTTPException(status_code=404, detail="Entrenador no encontrado")
    return entrenador

@entrenadores_router.delete("/{entrenador_id}")
async def delete_entrenador(entrenador_id: int):
    query = models.entrenador.delete().where(models.entrenador.c.entrenador_id == entrenador_id)
    result = await database.execute(query)
    return {"deleted": result}

@entrenadores_router.put("/{entrenador_id}", response_model=schemas.Entrenador)
async def update_entrenador(entrenador_id: int, entrenador: schemas.EntrenadorCreate):
    data = entrenador.dict()
    data["fecha_nac"] = date.fromisoformat(data["fecha_nac"])
    query = models.entrenador.update().where(models.entrenador.c.entrenador_id == entrenador_id).values(**data)
    await database.execute(query)
    return {**entrenador.dict(), "entrenador_id": entrenador_id}

# JuegaEn
@juega_en_router.post("/", response_model=schemas.JuegaEn)
async def create_juega_en(juega_en: schemas.JuegaEnCreate):
    data = juega_en.dict()
    data["fecha_inicio"] = date.fromisoformat(data["fecha_inicio"])
    if data["fecha_fin"] is not None:
        data["fecha_fin"] = date.fromisoformat(data["fecha_fin"])
    query = models.juega_en.insert().values(**data)
    await database.execute(query)
    return juega_en

@juega_en_router.get("/", response_model=List[schemas.JuegaEn])
async def read_juega_en():
    query = models.juega_en.select()
    return await database.fetch_all(query)

@juega_en_router.get("/{jugador_id}/{equipo_id}/{temporada_id}", response_model=schemas.JuegaEn)
async def read_juega_en_item(jugador_id: int, equipo_id: int, temporada_id: int):
    query = models.juega_en.select().where(
        (models.juega_en.c.jugador_id == jugador_id) &
        (models.juega_en.c.equipo_id == equipo_id) &
        (models.juega_en.c.temporada_id == temporada_id)
    )
    juega_en = await database.fetch_one(query)
    if juega_en is None:
        raise HTTPException(status_code=404, detail="JuegaEn no encontrado")
    return juega_en

@juega_en_router.delete("/{jugador_id}/{equipo_id}/{temporada_id}")
async def delete_juega_en(jugador_id: int, equipo_id: int, temporada_id: int):
    query = models.juega_en.delete().where(
        (models.juega_en.c.jugador_id == jugador_id) &
        (models.juega_en.c.equipo_id == equipo_id) &
        (models.juega_en.c.temporada_id == temporada_id)
    )
    result = await database.execute(query)
    return {"deleted": result}

@juega_en_router.put("/{jugador_id}/{equipo_id}/{temporada_id}", response_model=schemas.JuegaEn)
async def update_juega_en(jugador_id: int, equipo_id: int, temporada_id: int, juega_en: schemas.JuegaEnCreate):
    data = juega_en.dict()
    data["fecha_inicio"] = date.fromisoformat(data["fecha_inicio"])
    if data["fecha_fin"] is not None:
        data["fecha_fin"] = date.fromisoformat(data["fecha_fin"])
    query = models.juega_en.update().where(
        (models.juega_en.c.jugador_id == jugador_id) &
        (models.juega_en.c.equipo_id == equipo_id) &
        (models.juega_en.c.temporada_id == temporada_id)
    ).values(**data)
    await database.execute(query)
    return juega_en

# Entrena
@entrena_router.post("/", response_model=schemas.Entrena)
async def create_entrena(entrena: schemas.EntrenaCreate):
    data = entrena.dict()
    data["fecha_inicio"] = date.fromisoformat(data["fecha_inicio"])
    if data["fecha_fin"] is not None:
        data["fecha_fin"] = date.fromisoformat(data["fecha_fin"])
    query = models.entrena.insert().values(**data)
    await database.execute(query)
    return entrena

@entrena_router.get("/", response_model=List[schemas.Entrena])
async def read_entrena():
    query = models.entrena.select()
    return await database.fetch_all(query)

@entrena_router.get("/{entrenador_id}/{equipo_id}/{temporada_id}", response_model=schemas.Entrena)
async def read_entrena_item(entrenador_id: int, equipo_id: int, temporada_id: int):
    query = models.entrena.select().where(
        (models.entrena.c.entrenador_id == entrenador_id) &
        (models.entrena.c.equipo_id == equipo_id) &
        (models.entrena.c.temporada_id == temporada_id)
    )
    entrena = await database.fetch_one(query)
    if entrena is None:
        raise HTTPException(status_code=404, detail="Entrena no encontrado")
    return entrena

@entrena_router.delete("/{entrenador_id}/{equipo_id}/{temporada_id}")
async def delete_entrena(entrenador_id: int, equipo_id: int, temporada_id: int):
    query = models.entrena.delete().where(
        (models.entrena.c.entrenador_id == entrenador_id) &
        (models.entrena.c.equipo_id == equipo_id) &
        (models.entrena.c.temporada_id == temporada_id)
    )
    result = await database.execute(query)
    return {"deleted": result}

@entrena_router.put("/{entrenador_id}/{equipo_id}/{temporada_id}", response_model=schemas.Entrena)
async def update_entrena(entrenador_id: int, equipo_id: int, temporada_id: int, entrena: schemas.EntrenaCreate):
    data = entrena.dict()
    data["fecha_inicio"] = date.fromisoformat(data["fecha_inicio"])
    if data["fecha_fin"] is not None:
        data["fecha_fin"] = date.fromisoformat(data["fecha_fin"])
    query = models.entrena.update().where(
        (models.entrena.c.entrenador_id == entrenador_id) &
        (models.entrena.c.equipo_id == equipo_id) &
        (models.entrena.c.temporada_id == temporada_id)
    ).values(**data)
    await database.execute(query)
    return entrena

# Incluir routers
app.include_router(jugadores_router)
app.include_router(entrenadores_router)
app.include_router(juega_en_router)
app.include_router(entrena_router) 