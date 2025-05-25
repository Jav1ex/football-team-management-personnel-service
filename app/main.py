from fastapi import FastAPI, HTTPException, APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import get_db

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

# Jugadores
@jugadores_router.post("/", response_model=schemas.Jugador)
async def create_jugador(jugador: schemas.JugadorCreate, db: Session = Depends(get_db)):
    return crud.create_jugador(db=db, jugador=jugador)

@jugadores_router.get("/", response_model=List[schemas.Jugador])
async def read_jugadores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    jugadores = crud.get_jugadores(db, skip=skip, limit=limit)
    return jugadores

@jugadores_router.get("/{jugador_id}", response_model=schemas.Jugador)
async def read_jugador(jugador_id: int, db: Session = Depends(get_db)):
    jugador = crud.get_jugador(db, jugador_id=jugador_id)
    if jugador is None:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return jugador

@jugadores_router.delete("/{jugador_id}")
async def delete_jugador(jugador_id: int, db: Session = Depends(get_db)):
    if crud.delete_jugador(db, jugador_id=jugador_id):
        return {"deleted": True}
    raise HTTPException(status_code=404, detail="Jugador no encontrado")

@jugadores_router.put("/{jugador_id}", response_model=schemas.Jugador)
async def update_jugador(jugador_id: int, jugador: schemas.JugadorCreate, db: Session = Depends(get_db)):
    updated_jugador = crud.update_jugador(db, jugador_id=jugador_id, jugador=jugador)
    if updated_jugador is None:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return updated_jugador

# Entrenadores
@entrenadores_router.post("/", response_model=schemas.Entrenador)
async def create_entrenador(entrenador: schemas.EntrenadorCreate, db: Session = Depends(get_db)):
    return crud.create_entrenador(db=db, entrenador=entrenador)

@entrenadores_router.get("/", response_model=List[schemas.Entrenador])
async def read_entrenadores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    entrenadores = crud.get_entrenadores(db, skip=skip, limit=limit)
    return entrenadores

@entrenadores_router.get("/{entrenador_id}", response_model=schemas.Entrenador)
async def read_entrenador(entrenador_id: int, db: Session = Depends(get_db)):
    entrenador = crud.get_entrenador(db, entrenador_id=entrenador_id)
    if entrenador is None:
        raise HTTPException(status_code=404, detail="Entrenador no encontrado")
    return entrenador

@entrenadores_router.delete("/{entrenador_id}")
async def delete_entrenador(entrenador_id: int, db: Session = Depends(get_db)):
    if crud.delete_entrenador(db, entrenador_id=entrenador_id):
        return {"deleted": True}
    raise HTTPException(status_code=404, detail="Entrenador no encontrado")

@entrenadores_router.put("/{entrenador_id}", response_model=schemas.Entrenador)
async def update_entrenador(entrenador_id: int, entrenador: schemas.EntrenadorCreate, db: Session = Depends(get_db)):
    updated_entrenador = crud.update_entrenador(db, entrenador_id=entrenador_id, entrenador=entrenador)
    if updated_entrenador is None:
        raise HTTPException(status_code=404, detail="Entrenador no encontrado")
    return updated_entrenador

# JuegaEn
@juega_en_router.post("/", response_model=schemas.JuegaEn)
async def create_juega_en(juega_en: schemas.JuegaEnCreate, db: Session = Depends(get_db)):
    return crud.create_juega_en(db=db, juega_en=juega_en)

@juega_en_router.get("/", response_model=List[schemas.JuegaEn])
async def read_juega_en(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_juega_en_list(db, skip=skip, limit=limit)

@juega_en_router.get("/{jugador_id}/{equipo_id}/{temporada_id}", response_model=schemas.JuegaEn)
async def read_juega_en_item(jugador_id: int, equipo_id: int, temporada_id: int, db: Session = Depends(get_db)):
    juega_en = crud.get_juega_en(db, jugador_id=jugador_id, equipo_id=equipo_id, temporada_id=temporada_id)
    if juega_en is None:
        raise HTTPException(status_code=404, detail="JuegaEn no encontrado")
    return juega_en

@juega_en_router.delete("/{jugador_id}/{equipo_id}/{temporada_id}")
async def delete_juega_en(jugador_id: int, equipo_id: int, temporada_id: int, db: Session = Depends(get_db)):
    if crud.delete_juega_en(db, jugador_id=jugador_id, equipo_id=equipo_id, temporada_id=temporada_id):
        return {"deleted": True}
    raise HTTPException(status_code=404, detail="JuegaEn no encontrado")

@juega_en_router.put("/{jugador_id}/{equipo_id}/{temporada_id}", response_model=schemas.JuegaEn)
async def update_juega_en(
    jugador_id: int, equipo_id: int, temporada_id: int,
    juega_en: schemas.JuegaEnCreate, db: Session = Depends(get_db)
):
    updated_juega_en = crud.update_juega_en(
        db, jugador_id=jugador_id, equipo_id=equipo_id,
        temporada_id=temporada_id, juega_en=juega_en
    )
    if updated_juega_en is None:
        raise HTTPException(status_code=404, detail="JuegaEn no encontrado")
    return updated_juega_en

# Entrena
@entrena_router.post("/", response_model=schemas.Entrena)
async def create_entrena(entrena: schemas.EntrenaCreate, db: Session = Depends(get_db)):
    return crud.create_entrena(db=db, entrena=entrena)

@entrena_router.get("/", response_model=List[schemas.Entrena])
async def read_entrena(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_entrena_list(db, skip=skip, limit=limit)

@entrena_router.get("/{entrenador_id}/{equipo_id}/{temporada_id}", response_model=schemas.Entrena)
async def read_entrena_item(entrenador_id: int, equipo_id: int, temporada_id: int, db: Session = Depends(get_db)):
    entrena = crud.get_entrena(db, entrenador_id=entrenador_id, equipo_id=equipo_id, temporada_id=temporada_id)
    if entrena is None:
        raise HTTPException(status_code=404, detail="Entrena no encontrado")
    return entrena

@entrena_router.delete("/{entrenador_id}/{equipo_id}/{temporada_id}")
async def delete_entrena(entrenador_id: int, equipo_id: int, temporada_id: int, db: Session = Depends(get_db)):
    if crud.delete_entrena(db, entrenador_id=entrenador_id, equipo_id=equipo_id, temporada_id=temporada_id):
        return {"deleted": True}
    raise HTTPException(status_code=404, detail="Entrena no encontrado")

@entrena_router.put("/{entrenador_id}/{equipo_id}/{temporada_id}", response_model=schemas.Entrena)
async def update_entrena(
    entrenador_id: int, equipo_id: int, temporada_id: int,
    entrena: schemas.EntrenaCreate, db: Session = Depends(get_db)
):
    updated_entrena = crud.update_entrena(
        db, entrenador_id=entrenador_id, equipo_id=equipo_id,
        temporada_id=temporada_id, entrena=entrena
    )
    if updated_entrena is None:
        raise HTTPException(status_code=404, detail="Entrena no encontrado")
    return updated_entrena

# Incluir routers
app.include_router(jugadores_router)
app.include_router(entrenadores_router)
app.include_router(juega_en_router)
app.include_router(entrena_router) 