from sqlalchemy import Table, Column, Integer, String, BigInteger, Numeric, Date, ForeignKey, MetaData, Enum
from database import metadata

jugador = Table(
    "jugador",
    metadata,
    Column("jugador_id", BigInteger, primary_key=True),
    Column("nombre", String(50), nullable=False),
    Column("apellidos", String(50), nullable=False),
    Column("fecha_nac", Date, nullable=False),
    Column("nacionalidad", String(50), nullable=False),
    Column("posicion", String(50), nullable=False),  # Usar String para el enum
    Column("salario", Numeric(12, 2), nullable=False),
)

entrenador = Table(
    "entrenador",
    metadata,
    Column("entrenador_id", BigInteger, primary_key=True),
    Column("nombre", String(50), nullable=False),
    Column("apellidos", String(50), nullable=False),
    Column("fecha_nac", Date, nullable=False),
    Column("nacionalidad", String(50), nullable=False),
    Column("años_experiencia", Integer, nullable=False),
)

juega_en = Table(
    "juega_en",
    metadata,
    Column("jugador_id", BigInteger, ForeignKey("jugador.jugador_id", ondelete="CASCADE"), primary_key=True),
    Column("equipo_id", BigInteger, ForeignKey("equipo.equipo_id", ondelete="CASCADE"), primary_key=True),
    Column("temporada_id", BigInteger, ForeignKey("temporada.temporada_id", ondelete="CASCADE"), primary_key=True),
    Column("fecha_inicio", Date, nullable=False),
    Column("fecha_fin", Date, nullable=True),
)

entrena = Table(
    "entrena",
    metadata,
    Column("entrenador_id", BigInteger, ForeignKey("entrenador.entrenador_id", ondelete="CASCADE"), primary_key=True),
    Column("equipo_id", BigInteger, ForeignKey("equipo.equipo_id", ondelete="CASCADE"), primary_key=True),
    Column("temporada_id", BigInteger, ForeignKey("temporada.temporada_id", ondelete="CASCADE"), primary_key=True),
    Column("fecha_inicio", Date, nullable=False),
    Column("fecha_fin", Date, nullable=True),
) 