# genera_tablas.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, ForeignKey

# se importa información del archivo configuracion
from configuracion import cadena_base_datos

# se genera el enlace al gestor de base de datos
engine = create_engine(cadena_base_datos)

Base = declarative_base()

class Continente(Base):
    __tablename__ = 'continentes'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))

    # Un club tiene muchos jugadores -> Un continente tiene muchos paises
    paises = relationship("Pais", back_populates="continente")

    def __repr__(self):
        return "Continente(%d): nombre=%s" % (self.id, self.nombre)


class Pais(Base):
    __tablename__ = 'paises'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))

    # se agrega la columna continente_id como ForeignKey
    continente_id = Column(Integer, ForeignKey('continentes.id'))
    
    # Mapea la relación con Continente
    continente = relationship("Continente", back_populates="paises")

    def __repr__(self):
        return "Pais(%d): nombre=%s" % (self.id, self.nombre)


class Jugador(Base):
    __tablename__ = 'jugadores'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    posicion = Column(String(100))
    edad = Column(Integer)
    numero_partidos_seleccion = Column(Integer)
    goles_seleccion = Column(Integer)

    # Llaves foráneas simples que apuntan al id de la entidad pais
    pais_nacimiento_id = Column(Integer, ForeignKey('paises.id'))
    pais_donde_juega_id = Column(Integer, ForeignKey('paises.id'))

    # Relaciones directas para obtener el objeto Pais correspondiente
    pais_nacimiento = relationship("Pais", foreign_keys=[pais_nacimiento_id])
    pais_donde_juega = relationship("Pais", foreign_keys=[pais_donde_juega_id])

    def __repr__(self):
        return "Jugador: %s - posición: %s - edad: %d" % (self.nombre, self.posicion, self.edad)


# Genera físicamente las tablas en la base de datos (paises.db)
Base.metadata.create_all(engine)