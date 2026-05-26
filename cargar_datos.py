# cargar_datos.py
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from configuracion import cadena_base_datos
from genera_tablas import Continente, Pais, Jugador

# Configuración del motor y la sesión
engine = create_engine(cadena_base_datos)
Session = sessionmaker(bind=engine)
session = Session()

# Función segura para conversión de tipos de datos
def convertir_entero(valor):
    try:
        return int(valor)
    except:
        return 0

# 1. Leer el archivo CSV dentro de la carpeta data
df = pd.read_csv("data/jugadores_futbol.csv")

print("-> Iniciando la carga de datos en las entidades ORM...")

# 2. Recorrer y procesar de forma relacional buscando por variaciones de nombre
for _, fila in df.iterrows():
    
    # Buscamos las columnas de forma flexible (sirve para 'continente' o 'Continente')
    nombre_continente = str(fila.get("continente") if "continente" in fila else fila.get("Continente", "Desconocido")).strip()
    nombre_pais_nacimiento = str(fila.get("pais_nacimiento") if "pais_nacimiento" in fila else fila.get("Pais_nacimiento", fila.get("Pais_Nacimiento", "Desconocido"))).strip()
    nombre_pais_juega = str(fila.get("pais_donde_juega") if "pais_donde_juega" in fila else fila.get("Pais_donde_juega", fila.get("Pais_Donde_Juega", "Desconocido"))).strip()
    nombre_jugador = str(fila.get("nombre_jugador") if "nombre_jugador" in fila else fila.get("Nombre_jugador", fila.get("Nombre_Jugador", "Anonimo"))).strip()

    # ==========================================
    # Gestión del Continente
    # ==========================================
    continente = session.query(Continente).filter_by(
        nombre=nombre_continente
    ).first()

    if continente is None:
        continente = Continente(
            nombre=nombre_continente
        )
        session.add(continente)
        session.commit()

    # ==========================================
    # Gestión del País de Nacimiento
    # ==========================================
    pais_nacimiento = session.query(Pais).filter_by(
        nombre=nombre_pais_nacimiento
    ).first()

    if pais_nacimiento is None:
        pais_nacimiento = Pais(
            nombre=nombre_pais_nacimiento,
            continente_id=continente.id
        )
        session.add(pais_nacimiento)
        session.commit()

    # ==========================================
    # Gestión del País Donde Juega
    # ==========================================
    pais_juega = session.query(Pais).filter_by(
        nombre=nombre_pais_juega
    ).first()

    if pais_juega is None:
        pais_juega = Pais(
            nombre=nombre_pais_juega
        )
        session.add(pais_juega)
        session.commit()

    # ==========================================
    # Creación del Registro del Jugador
    # ==========================================
    # Buscamos dinámicamente los valores numéricos y de texto restantes
    posicion = str(fila.get("posicion") if "posicion" in fila else fila.get("Posicion", "Desconocida")).strip()
    edad_val = fila.get("edad") if "edad" in fila else fila.get("Edad", 0)
    partidos_val = fila.get("numero_partidos_seleccion") if "numero_partidos_seleccion" in fila else fila.get("Numero_partidos_seleccion", 0)
    goles_val = fila.get("goles_seleccion") if "goles_seleccion" in fila else fila.get("Goles_seleccion", 0)

    jugador = Jugador(
        nombre=nombre_jugador,
        posicion=posicion,
        edad=convertir_entero(edad_val),
        numero_partidos_seleccion=convertir_entero(partidos_val),
        goles_seleccion=convertir_entero(goles_val),
        pais_nacimiento_id=pais_nacimiento.id,
        pais_donde_juega_id=pais_juega.id
    )

    session.add(jugador)

# Guardar la colección de jugadores agregados
session.commit()
session.close()

print("Datos cargados correctamente.")