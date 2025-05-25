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

# Jugador operations
def get_jugadores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.jugador).offset(skip).limit(limit).all()

def get_jugador(db: Session, jugador_id: int):
    return db.query(models.jugador).filter(models.jugador.c.jugador_id == jugador_id).first()

def create_jugador(db: Session, jugador: schemas.JugadorCreate):
    data = jugador.dict()
    data["fecha_nac"] = date.fromisoformat(data["fecha_nac"])
    db_jugador = models.jugador.insert().values(**data)
    result = db.execute(db_jugador)
    db.commit()
    return {**data, "jugador_id": result.inserted_primary_key[0]}

def update_jugador(db: Session, jugador_id: int, jugador: schemas.JugadorCreate):
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

def delete_jugador(db: Session, jugador_id: int):
    result = db.execute(
        models.jugador.delete().where(models.jugador.c.jugador_id == jugador_id)
    )
    db.commit()
    return result.rowcount > 0

# Entrenador operations
def get_entrenadores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.entrenador).offset(skip).limit(limit).all()

def get_entrenador(db: Session, entrenador_id: int):
    return db.query(models.entrenador).filter(models.entrenador.c.entrenador_id == entrenador_id).first()

def create_entrenador(db: Session, entrenador: schemas.EntrenadorCreate):
    data = entrenador.dict()
    data["fecha_nac"] = date.fromisoformat(data["fecha_nac"])
    db_entrenador = models.entrenador.insert().values(**data)
    result = db.execute(db_entrenador)
    db.commit()
    return {**data, "entrenador_id": result.inserted_primary_key[0]}

def update_entrenador(db: Session, entrenador_id: int, entrenador: schemas.EntrenadorCreate):
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

def delete_entrenador(db: Session, entrenador_id: int):
    result = db.execute(
        models.entrenador.delete().where(models.entrenador.c.entrenador_id == entrenador_id)
    )
    db.commit()
    return result.rowcount > 0

# JuegaEn operations
def get_juega_en_list(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.juega_en).offset(skip).limit(limit).all()

def get_juega_en(db: Session, jugador_id: int, equipo_id: int, temporada_id: int):
    return db.query(models.juega_en).filter(
        and_(
            models.juega_en.c.jugador_id == jugador_id,
            models.juega_en.c.equipo_id == equipo_id,
            models.juega_en.c.temporada_id == temporada_id
        )
    ).first()

def create_juega_en(db: Session, juega_en: schemas.JuegaEnCreate):
    data = juega_en.dict()
    data["fecha_inicio"] = date.fromisoformat(data["fecha_inicio"])
    if data["fecha_fin"]:
        data["fecha_fin"] = date.fromisoformat(data["fecha_fin"])
    db_juega_en = models.juega_en.insert().values(**data)
    db.execute(db_juega_en)
    db.commit()
    return data

def update_juega_en(db: Session, jugador_id: int, equipo_id: int, temporada_id: int, juega_en: schemas.JuegaEnCreate):
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

def delete_juega_en(db: Session, jugador_id: int, equipo_id: int, temporada_id: int):
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

# Entrena operations
def get_entrena_list(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.entrena).offset(skip).limit(limit).all()

def get_entrena(db: Session, entrenador_id: int, equipo_id: int, temporada_id: int):
    return db.query(models.entrena).filter(
        and_(
            models.entrena.c.entrenador_id == entrenador_id,
            models.entrena.c.equipo_id == equipo_id,
            models.entrena.c.temporada_id == temporada_id
        )
    ).first()

def create_entrena(db: Session, entrena: schemas.EntrenaCreate):
    data = entrena.dict()
    data["fecha_inicio"] = date.fromisoformat(data["fecha_inicio"])
    if data["fecha_fin"]:
        data["fecha_fin"] = date.fromisoformat(data["fecha_fin"])
    db_entrena = models.entrena.insert().values(**data)
    db.execute(db_entrena)
    db.commit()
    return data

def update_entrena(db: Session, entrenador_id: int, equipo_id: int, temporada_id: int, entrena: schemas.EntrenaCreate):
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

def delete_entrena(db: Session, entrenador_id: int, equipo_id: int, temporada_id: int):
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