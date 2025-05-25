from pydantic import BaseModel
from typing import Optional
from datetime import date

class JugadorBase(BaseModel):
    nombre: str
    apellidos: str
    fecha_nac: str  # Para entrada, string
    nacionalidad: str
    posicion: str
    salario: float

class JugadorCreate(JugadorBase):
    pass

class Jugador(JugadorBase):
    jugador_id: int
    fecha_nac: date  # Para salida, date
    class Config:
        orm_mode = True

class EntrenadorBase(BaseModel):
    nombre: str
    apellidos: str
    fecha_nac: str  # Para entrada, string
    nacionalidad: str
    años_experiencia: int

class EntrenadorCreate(EntrenadorBase):
    pass

class Entrenador(EntrenadorBase):
    entrenador_id: int
    fecha_nac: date  # Para salida, date
    class Config:
        orm_mode = True

class JuegaEnBase(BaseModel):
    jugador_id: int
    equipo_id: int
    temporada_id: int
    fecha_inicio: str
    fecha_fin: Optional[str] = None

class JuegaEnCreate(JuegaEnBase):
    pass

class JuegaEn(JuegaEnBase):
    class Config:
        orm_mode = True

class EntrenaBase(BaseModel):
    entrenador_id: int
    equipo_id: int
    temporada_id: int
    fecha_inicio: str
    fecha_fin: Optional[str] = None

class EntrenaCreate(EntrenaBase):
    pass

class Entrena(EntrenaBase):
    class Config:
        orm_mode = True 