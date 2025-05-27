from fastapi import FastAPI, HTTPException, APIRouter, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from . import models, schemas, crud
from .database import get_db, execute_with_retry
import time
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware para manejar errores de base de datos
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"Request completed in {process_time:.2f} seconds")
        return response
    except OperationalError as e:
        logger.error(f"Error de conexión a la base de datos: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={"detail": "Error de conexión a la base de datos. Por favor, intente nuevamente."}
        )
    except SQLAlchemyError as e:
        logger.error(f"Error de SQLAlchemy: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={"detail": "Error en la operación de base de datos. Por favor, intente nuevamente."}
        )
    except Exception as e:
        logger.error(f"Error interno del servidor: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Error interno del servidor"}
        )

# Routers
jugadores_router = APIRouter(prefix="/jugadores", tags=["Jugadores"])
entrenadores_router = APIRouter(prefix="/entrenadores", tags=["Entrenadores"])
juega_en_router = APIRouter(prefix="/juega_en", tags=["JuegaEn"])
entrena_router = APIRouter(prefix="/entrena", tags=["Entrena"])

# Jugadores
@jugadores_router.post("/", response_model=schemas.Jugador)
async def create_jugador(jugador: schemas.JugadorCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_jugador(db=db, jugador=jugador)
    except SQLAlchemyError as e:
        logger.error(f"Error al crear jugador: {str(e)}")
        raise HTTPException(status_code=503, detail="Error al crear el jugador")

@jugadores_router.get("/", response_model=List[schemas.Jugador])
async def read_jugadores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        logger.info(f"Obteniendo jugadores (skip={skip}, limit={limit})")
        jugadores = execute_with_retry(crud.get_jugadores, db, skip=skip, limit=limit)
        logger.info(f"Se obtuvieron {len(jugadores)} jugadores")
        return jugadores
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener jugadores: {str(e)}")
        raise HTTPException(status_code=503, detail="Error al obtener los jugadores")

@jugadores_router.get("/{jugador_id}", response_model=schemas.Jugador)
async def read_jugador(jugador_id: int, db: Session = Depends(get_db)):
    try:
        jugador = execute_with_retry(crud.get_jugador, db, jugador_id=jugador_id)
        if jugador is None:
            raise HTTPException(status_code=404, detail="Jugador no encontrado")
        return jugador
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener jugador {jugador_id}: {str(e)}")
        raise HTTPException(status_code=503, detail="Error al obtener el jugador")

@jugadores_router.delete("/{jugador_id}")
async def delete_jugador(jugador_id: int, db: Session = Depends(get_db)):
    try:
        if execute_with_retry(crud.delete_jugador, db, jugador_id=jugador_id):
            return {"deleted": True}
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    except SQLAlchemyError as e:
        logger.error(f"Error al eliminar jugador {jugador_id}: {str(e)}")
        raise HTTPException(status_code=503, detail="Error al eliminar el jugador")

@jugadores_router.put("/{jugador_id}", response_model=schemas.Jugador)
async def update_jugador(jugador_id: int, jugador: schemas.JugadorCreate, db: Session = Depends(get_db)):
    try:
        updated_jugador = execute_with_retry(crud.update_jugador, db, jugador_id=jugador_id, jugador=jugador)
        if updated_jugador is None:
            raise HTTPException(status_code=404, detail="Jugador no encontrado")
        return updated_jugador
    except SQLAlchemyError as e:
        logger.error(f"Error al actualizar jugador {jugador_id}: {str(e)}")
        raise HTTPException(status_code=503, detail="Error al actualizar el jugador")

# Entrenadores
@entrenadores_router.post("/", response_model=schemas.Entrenador)
async def create_entrenador(entrenador: schemas.EntrenadorCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_entrenador(db=db, entrenador=entrenador)
    except SQLAlchemyError as e:
        logger.error(f"Error al crear entrenador: {str(e)}")
        raise HTTPException(status_code=503, detail="Error al crear el entrenador")

@entrenadores_router.get("/", response_model=List[schemas.Entrenador])
async def read_entrenadores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        logger.info(f"Obteniendo entrenadores (skip={skip}, limit={limit})")
        entrenadores = execute_with_retry(crud.get_entrenadores, db, skip=skip, limit=limit)
        logger.info(f"Se obtuvieron {len(entrenadores)} entrenadores")
        return entrenadores
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener entrenadores: {str(e)}")
        raise HTTPException(status_code=503, detail="Error al obtener los entrenadores")

@entrenadores_router.get("/{entrenador_id}", response_model=schemas.Entrenador)
async def read_entrenador(entrenador_id: int, db: Session = Depends(get_db)):
    try:
        entrenador = execute_with_retry(crud.get_entrenador, db, entrenador_id=entrenador_id)
        if entrenador is None:
            raise HTTPException(status_code=404, detail="Entrenador no encontrado")
        return entrenador
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener entrenador {entrenador_id}: {str(e)}")
        raise HTTPException(status_code=503, detail="Error al obtener el entrenador")

@entrenadores_router.delete("/{entrenador_id}")
async def delete_entrenador(entrenador_id: int, db: Session = Depends(get_db)):
    try:
        if execute_with_retry(crud.delete_entrenador, db, entrenador_id=entrenador_id):
            return {"deleted": True}
        raise HTTPException(status_code=404, detail="Entrenador no encontrado")
    except SQLAlchemyError as e:
        logger.error(f"Error al eliminar entrenador {entrenador_id}: {str(e)}")
        raise HTTPException(status_code=503, detail="Error al eliminar el entrenador")

@entrenadores_router.put("/{entrenador_id}", response_model=schemas.Entrenador)
async def update_entrenador(entrenador_id: int, entrenador: schemas.EntrenadorCreate, db: Session = Depends(get_db)):
    try:
        updated_entrenador = execute_with_retry(crud.update_entrenador, db, entrenador_id=entrenador_id, entrenador=entrenador)
        if updated_entrenador is None:
            raise HTTPException(status_code=404, detail="Entrenador no encontrado")
        return updated_entrenador
    except SQLAlchemyError as e:
        logger.error(f"Error al actualizar entrenador {entrenador_id}: {str(e)}")
        raise HTTPException(status_code=503, detail="Error al actualizar el entrenador")

# JuegaEn
@juega_en_router.post("/", response_model=schemas.JuegaEn)
async def create_juega_en(juega_en: schemas.JuegaEnCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_juega_en(db=db, juega_en=juega_en)
    except SQLAlchemyError as e:
        logger.error(f"Error al crear relación juega_en: {str(e)}")
        raise HTTPException(status_code=503, detail="Error al crear la relación juega_en")

@juega_en_router.get("/", response_model=List[schemas.JuegaEn])
async def read_juega_en(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        logger.info(f"Obteniendo relaciones juega_en (skip={skip}, limit={limit})")
        relaciones = execute_with_retry(crud.get_juega_en_list, db, skip=skip, limit=limit)
        logger.info(f"Se obtuvieron {len(relaciones)} relaciones")
        return relaciones
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener relaciones juega_en: {str(e)}")
        raise HTTPException(status_code=503, detail="Error al obtener las relaciones juega_en")

@juega_en_router.get("/{jugador_id}/{equipo_id}/{temporada_id}", response_model=schemas.JuegaEn)
async def read_juega_en_item(jugador_id: int, equipo_id: int, temporada_id: int, db: Session = Depends(get_db)):
    try:
        juega_en = execute_with_retry(crud.get_juega_en, db, jugador_id=jugador_id, equipo_id=equipo_id, temporada_id=temporada_id)
        if juega_en is None:
            raise HTTPException(status_code=404, detail="JuegaEn no encontrado")
        return juega_en
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener relación juega_en: {str(e)}")
        raise HTTPException(status_code=503, detail="Error al obtener la relación juega_en")

@juega_en_router.delete("/{jugador_id}/{equipo_id}/{temporada_id}")
async def delete_juega_en(jugador_id: int, equipo_id: int, temporada_id: int, db: Session = Depends(get_db)):
    try:
        if execute_with_retry(crud.delete_juega_en, db, jugador_id=jugador_id, equipo_id=equipo_id, temporada_id=temporada_id):
            return {"deleted": True}
        raise HTTPException(status_code=404, detail="JuegaEn no encontrado")
    except SQLAlchemyError as e:
        logger.error(f"Error al eliminar relación juega_en: {str(e)}")
        raise HTTPException(status_code=503, detail="Error al eliminar la relación juega_en")

@juega_en_router.put("/{jugador_id}/{equipo_id}/{temporada_id}", response_model=schemas.JuegaEn)
async def update_juega_en(
    jugador_id: int, equipo_id: int, temporada_id: int,
    juega_en: schemas.JuegaEnCreate, db: Session = Depends(get_db)
):
    try:
        updated_juega_en = execute_with_retry(
            crud.update_juega_en,
            db, jugador_id=jugador_id, equipo_id=equipo_id,
            temporada_id=temporada_id, juega_en=juega_en
        )
        if updated_juega_en is None:
            raise HTTPException(status_code=404, detail="JuegaEn no encontrado")
        return updated_juega_en
    except SQLAlchemyError as e:
        logger.error(f"Error al actualizar relación juega_en: {str(e)}")
        raise HTTPException(status_code=503, detail="Error al actualizar la relación juega_en")

# Entrena
@entrena_router.post("/", response_model=schemas.Entrena)
async def create_entrena(entrena: schemas.EntrenaCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_entrena(db=db, entrena=entrena)
    except SQLAlchemyError as e:
        logger.error(f"Error al crear relación entrena: {str(e)}")
        raise HTTPException(status_code=503, detail="Error al crear la relación entrena")

@entrena_router.get("/", response_model=List[schemas.Entrena])
async def read_entrena(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        logger.info(f"Obteniendo relaciones entrena (skip={skip}, limit={limit})")
        relaciones = execute_with_retry(crud.get_entrena_list, db, skip=skip, limit=limit)
        logger.info(f"Se obtuvieron {len(relaciones)} relaciones")
        return relaciones
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener relaciones entrena: {str(e)}")
        raise HTTPException(status_code=503, detail="Error al obtener las relaciones entrena")

@entrena_router.get("/{entrenador_id}/{equipo_id}/{temporada_id}", response_model=schemas.Entrena)
async def read_entrena_item(entrenador_id: int, equipo_id: int, temporada_id: int, db: Session = Depends(get_db)):
    try:
        entrena = execute_with_retry(crud.get_entrena, db, entrenador_id=entrenador_id, equipo_id=equipo_id, temporada_id=temporada_id)
        if entrena is None:
            raise HTTPException(status_code=404, detail="Entrena no encontrado")
        return entrena
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener relación entrena: {str(e)}")
        raise HTTPException(status_code=503, detail="Error al obtener la relación entrena")

@entrena_router.delete("/{entrenador_id}/{equipo_id}/{temporada_id}")
async def delete_entrena(entrenador_id: int, equipo_id: int, temporada_id: int, db: Session = Depends(get_db)):
    try:
        if execute_with_retry(crud.delete_entrena, db, entrenador_id=entrenador_id, equipo_id=equipo_id, temporada_id=temporada_id):
            return {"deleted": True}
        raise HTTPException(status_code=404, detail="Entrena no encontrado")
    except SQLAlchemyError as e:
        logger.error(f"Error al eliminar relación entrena: {str(e)}")
        raise HTTPException(status_code=503, detail="Error al eliminar la relación entrena")

@entrena_router.put("/{entrenador_id}/{equipo_id}/{temporada_id}", response_model=schemas.Entrena)
async def update_entrena(
    entrenador_id: int, equipo_id: int, temporada_id: int,
    entrena: schemas.EntrenaCreate, db: Session = Depends(get_db)
):
    try:
        updated_entrena = execute_with_retry(
            crud.update_entrena,
            db, entrenador_id=entrenador_id, equipo_id=equipo_id,
            temporada_id=temporada_id, entrena=entrena
        )
        if updated_entrena is None:
            raise HTTPException(status_code=404, detail="Entrena no encontrado")
        return updated_entrena
    except SQLAlchemyError as e:
        logger.error(f"Error al actualizar relación entrena: {str(e)}")
        raise HTTPException(status_code=503, detail="Error al actualizar la relación entrena")

# Incluir routers
app.include_router(jugadores_router)
app.include_router(entrenadores_router)
app.include_router(juega_en_router)
app.include_router(entrena_router) 