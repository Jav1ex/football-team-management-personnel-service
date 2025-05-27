"""
CRUD operations for database entities.

Implements create, read, update, and delete logic for 'Jugador', 'Entrenador', 'JuegaEn' and 'Entrena'.
Dependencies: SQLAlchemy ORM, application models and schemas.
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import date
from . import models, schemas
from typing import List
from sqlalchemy.exc import SQLAlchemyError, OperationalError
import logging

logger = logging.getLogger(__name__)

# Jugador operations
def get_jugadores(db: Session, skip: int = 0, limit: int = 100):
    try:
        return db.query(models.jugador).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener jugadores: {str(e)}")
        raise

def get_jugador(db: Session, jugador_id: int):
    try:
        return db.query(models.jugador).filter(models.jugador.c.jugador_id == jugador_id).first()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener jugador {jugador_id}: {str(e)}")
        raise

def create_jugador(db: Session, jugador: schemas.JugadorCreate):
    try:
        data = jugador.dict()
        data["fecha_nac"] = date.fromisoformat(data["fecha_nac"])
        db_jugador = models.jugador.insert().values(**data)
        result = db.execute(db_jugador)
        db.commit()
        return {**data, "jugador_id": result.inserted_primary_key[0]}
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear jugador: {str(e)}")
        raise

def update_jugador(db: Session, jugador_id: int, jugador: schemas.JugadorCreate):
    try:
        data = jugador.dict()
        data["fecha_nac"] = date.fromisoformat(data["fecha_nac"])
        result = db.execute(
            models.jugador.update()
            .where(models.jugador.c.jugador_id == jugador_id)
            .values(**data)
        )
        db.commit()
        if result.rowcount == 0:
            return None
        return {**data, "jugador_id": jugador_id}
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar jugador {jugador_id}: {str(e)}")
        raise

def delete_jugador(db: Session, jugador_id: int):
    try:
        result = db.execute(
            models.jugador.delete().where(models.jugador.c.jugador_id == jugador_id)
        )
        db.commit()
        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al eliminar jugador {jugador_id}: {str(e)}")
        raise

# Entrenador operations
def get_entrenadores(db: Session, skip: int = 0, limit: int = 100):
    try:
        return db.query(models.entrenador).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener entrenadores: {str(e)}")
        raise

def get_entrenador(db: Session, entrenador_id: int):
    try:
        return db.query(models.entrenador).filter(models.entrenador.c.entrenador_id == entrenador_id).first()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener entrenador {entrenador_id}: {str(e)}")
        raise

def create_entrenador(db: Session, entrenador: schemas.EntrenadorCreate):
    try:
        data = entrenador.dict()
        data["fecha_nac"] = date.fromisoformat(data["fecha_nac"])
        db_entrenador = models.entrenador.insert().values(**data)
        result = db.execute(db_entrenador)
        db.commit()
        return {**data, "entrenador_id": result.inserted_primary_key[0]}
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear entrenador: {str(e)}")
        raise

def update_entrenador(db: Session, entrenador_id: int, entrenador: schemas.EntrenadorCreate):
    try:
        data = entrenador.dict()
        data["fecha_nac"] = date.fromisoformat(data["fecha_nac"])
        result = db.execute(
            models.entrenador.update()
            .where(models.entrenador.c.entrenador_id == entrenador_id)
            .values(**data)
        )
        db.commit()
        if result.rowcount == 0:
            return None
        return {**data, "entrenador_id": entrenador_id}
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar entrenador {entrenador_id}: {str(e)}")
        raise

def delete_entrenador(db: Session, entrenador_id: int):
    try:
        result = db.execute(
            models.entrenador.delete().where(models.entrenador.c.entrenador_id == entrenador_id)
        )
        db.commit()
        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al eliminar entrenador {entrenador_id}: {str(e)}")
        raise

# JuegaEn operations
def get_juega_en_list(db: Session, skip: int = 0, limit: int = 100):
    try:
        return db.query(models.juega_en).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener relaciones juega_en: {str(e)}")
        raise

def get_juega_en(db: Session, jugador_id: int, equipo_id: int, temporada_id: int):
    try:
        return db.query(models.juega_en).filter(
            and_(
                models.juega_en.c.jugador_id == jugador_id,
                models.juega_en.c.equipo_id == equipo_id,
                models.juega_en.c.temporada_id == temporada_id
            )
        ).first()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener relación juega_en: {str(e)}")
        raise

def create_juega_en(db: Session, juega_en: schemas.JuegaEnCreate):
    try:
        data = juega_en.dict()
        data["fecha_inicio"] = date.fromisoformat(data["fecha_inicio"])
        if data["fecha_fin"]:
            data["fecha_fin"] = date.fromisoformat(data["fecha_fin"])
        db_juega_en = models.juega_en.insert().values(**data)
        db.execute(db_juega_en)
        db.commit()
        return data
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear relación juega_en: {str(e)}")
        raise

def update_juega_en(db: Session, jugador_id: int, equipo_id: int, temporada_id: int, juega_en: schemas.JuegaEnCreate):
    try:
        data = juega_en.dict()
        data["fecha_inicio"] = date.fromisoformat(data["fecha_inicio"])
        if data["fecha_fin"]:
            data["fecha_fin"] = date.fromisoformat(data["fecha_fin"])
        result = db.execute(
            models.juega_en.update().where(
                and_(
                    models.juega_en.c.jugador_id == jugador_id,
                    models.juega_en.c.equipo_id == equipo_id,
                    models.juega_en.c.temporada_id == temporada_id
                )
            ).values(**data)
        )
        db.commit()
        if result.rowcount == 0:
            return None
        return data
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar relación juega_en: {str(e)}")
        raise

def delete_juega_en(db: Session, jugador_id: int, equipo_id: int, temporada_id: int):
    try:
        result = db.execute(
            models.juega_en.delete().where(
                and_(
                    models.juega_en.c.jugador_id == jugador_id,
                    models.juega_en.c.equipo_id == equipo_id,
                    models.juega_en.c.temporada_id == temporada_id
                )
            )
        )
        db.commit()
        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al eliminar relación juega_en: {str(e)}")
        raise

# Entrena operations
def get_entrena_list(db: Session, skip: int = 0, limit: int = 100):
    try:
        return db.query(models.entrena).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener relaciones entrena: {str(e)}")
        raise

def get_entrena(db: Session, entrenador_id: int, equipo_id: int, temporada_id: int):
    try:
        return db.query(models.entrena).filter(
            and_(
                models.entrena.c.entrenador_id == entrenador_id,
                models.entrena.c.equipo_id == equipo_id,
                models.entrena.c.temporada_id == temporada_id
            )
        ).first()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener relación entrena: {str(e)}")
        raise

def create_entrena(db: Session, entrena: schemas.EntrenaCreate):
    try:
        data = entrena.dict()
        data["fecha_inicio"] = date.fromisoformat(data["fecha_inicio"])
        if data["fecha_fin"]:
            data["fecha_fin"] = date.fromisoformat(data["fecha_fin"])
        db_entrena = models.entrena.insert().values(**data)
        db.execute(db_entrena)
        db.commit()
        return data
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear relación entrena: {str(e)}")
        raise

def update_entrena(db: Session, entrenador_id: int, equipo_id: int, temporada_id: int, entrena: schemas.EntrenaCreate):
    try:
        data = entrena.dict()
        data["fecha_inicio"] = date.fromisoformat(data["fecha_inicio"])
        if data["fecha_fin"]:
            data["fecha_fin"] = date.fromisoformat(data["fecha_fin"])
        result = db.execute(
            models.entrena.update().where(
                and_(
                    models.entrena.c.entrenador_id == entrenador_id,
                    models.entrena.c.equipo_id == equipo_id,
                    models.entrena.c.temporada_id == temporada_id
                )
            ).values(**data)
        )
        db.commit()
        if result.rowcount == 0:
            return None
        return data
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar relación entrena: {str(e)}")
        raise

def delete_entrena(db: Session, entrenador_id: int, equipo_id: int, temporada_id: int):
    try:
        result = db.execute(
            models.entrena.delete().where(
                and_(
                    models.entrena.c.entrenador_id == entrenador_id,
                    models.entrena.c.equipo_id == equipo_id,
                    models.entrena.c.temporada_id == temporada_id
                )
            )
        )
        db.commit()
        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al eliminar relación entrena: {str(e)}")
        raise 