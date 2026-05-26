# app.py
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, aliased

from configuracion import cadena_base_datos
# Importamos las entidades desde tu archivo genera_tablas
from genera_tablas import Continente, Pais, Jugador 

# Configuración del motor y la sesión
engine = create_engine(cadena_base_datos)
Session = sessionmaker(bind=engine)
session = Session()

# Configuración de la página en Streamlit
st.set_page_config(
    page_title="Taller 08 - ORM",
    layout="wide"
)

st.title("Taller 08 - Integración de datos y ORM")

# =============================================================================
# 1. TABLA GENERAL DE JUGADORES
# =============================================================================
st.subheader("1. Tabla general de jugadores")

# Como mapeamos la tabla Pais dos veces (nacimiento y donde juega),
# usamos un alias para obtener el nombre del país donde juega de forma limpia.
PaisJuega = aliased(Pais)

# Modifica la consulta de la tabla 1 en tu app.py:

consulta_jugadores = session.query(
    Jugador.nombre,  
    Pais.nombre.label("pais_nacimiento"),
    PaisJuega.nombre.label("pais_donde_juega"), 
    Jugador.posicion,
    Jugador.edad,
    Jugador.numero_partidos_seleccion,
    Jugador.goles_seleccion,
    Continente.nombre.label("continente")
).select_from(Jugador).join(
    Pais,
    Jugador.pais_nacimiento_id == Pais.id,
    isouter=True # <--- CORRECCIÓN: Trae al jugador aunque falle el join
).join(
    PaisJuega,
    Jugador.pais_donde_juega_id == PaisJuega.id,
    isouter=True # <--- CORRECCIÓN
).join(
    Continente,
    Pais.continente_id == Continente.id,
    isouter=True # <--- CORRECCIÓN
).all()

df_jugadores = pd.DataFrame(
    consulta_jugadores,
    columns=[
        "nombre_jugador",
        "pais_nacimiento",
        "pais_donde_juega",
        "posicion",
        "edad",
        "numero_partidos_seleccion",
        "goles_seleccion",
        "continente"
    ]
)

st.dataframe(df_jugadores, use_container_width=True)

# =============================================================================
# 2. RESUMEN POR CONTINENTE
# =============================================================================
st.subheader("2. Resumen por continente")

consulta_continente = session.query(
    Continente.nombre.label("continente"),
    func.count(Jugador.id).label("numero_jugadores"),
    func.sum(Jugador.goles_seleccion).label("total_goles")
).select_from(Continente).join(
    Pais,
    Pais.continente_id == Continente.id
).join(
    Jugador,
    Jugador.pais_nacimiento_id == Pais.id
).group_by(
    Continente.nombre
).all()

df_continente = pd.DataFrame(
    consulta_continente,
    columns=[
        "continente",
        "número de jugadores de la base",
        "número goles"
    ]
)

st.dataframe(df_continente, use_container_width=True)

# =============================================================================
# 3. RESUMEN POR PAÍS
# =============================================================================
st.subheader("3. Resumen por país")

consulta_pais = session.query(
    Pais.nombre.label("paise"),
    func.count(Jugador.id).label("numero_jugadores"),
    func.sum(Jugador.goles_seleccion).label("total_goles")
).select_from(Pais).join(
    Jugador,
    Jugador.pais_nacimiento_id == Pais.id
).group_by(
    Pais.nombre
).all()

df_pais = pd.DataFrame(
    consulta_pais,
    columns=[
        "paise",
        "número de jugadores de la base",
        "número de goles"
    ]
)

st.dataframe(df_pais, use_container_width=True)

# Cerramos la sesión al finalizar las consultas del frontend
session.close()