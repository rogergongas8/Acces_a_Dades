import streamlit as st
import pandas as pd
import numpy as np


path = "libros.csv"
st.title("Scrapeada historica ")

#  Cargar Datos
try:
    df = pd.read_csv(path)
except FileNotFoundError:
    st.error(
        "Error: No se ha encontrado el archivo 'libros.csv'. "
    )
    st.stop()

#Sidebar de Filtros
st.sidebar.header("Filtros")

## . Filtro de Precio
precio_min = float(df["precio"].min())
precio_max = float(df["precio"].max())

rango_precio = st.sidebar.slider(
    "Filtrar por precio (€)",
    min_value=precio_min,
    max_value=precio_max,
    value=(precio_min, precio_max)
)

## Filtro de Rating
ratings_disponibles = sorted(df["rating"].unique())
ratings_seleccionados = st.sidebar.multiselect(
    "Filtrar por rating (estrellas)",
    options=ratings_disponibles,
    default=ratings_disponibles
)

# Logica del filtro (es el que manda a la hora de mostrar los libros filtrados)
df_filtrado = df[
    (df["precio"] >= rango_precio[0]) &
    (df["precio"] <= rango_precio[1]) &
    (df["rating"].isin(ratings_seleccionados))
    ].copy()

#Página Principal
st.header("Resultados de la Búsqueda")

# Primero, calculamos las métricas (promedios)
total_libros_filtrados = len(df_filtrado)
if total_libros_filtrados > 0:
    # Calculamos promedios solo si hay libros
    precio_promedio = df_filtrado["precio"].mean()
    rating_promedio = df_filtrado["rating"].mean()
else:
    # Si no hay libros, ponemos 0
    precio_promedio = 0.0
    rating_promedio = 0.0

# Usamos st.columns para ponerlas una al lado de la otra
col1, col2, col3 = st.columns(3)
col1.metric(label="Libros Encontrados", value=total_libros_filtrados)
col2.metric(label="Precio Promedio", value=f"€{precio_promedio:.2f}")
col3.metric(label="Rating Promedio", value=f"{rating_promedio:.1f} ★")

# Grafico de Barras
st.subheader("Distribución de Ratings")
if total_libros_filtrados > 0:
    # Contamos cuantos libros hay de cada rating
    rating_counts = df_filtrado["rating"].value_counts().sort_index()

    # Le ponemos un nombre al índice para que el gráfico se vea bien
    rating_counts.index.name = "Rating (estrellas)"

    #  grafico simple
    st.bar_chart(rating_counts)
else:
    st.write("No hay libros que coincidan con los filtros para mostrar un gráfico.")

# tabla de Datos
st.subheader(f"Datos: {len(df_filtrado)} de {len(df)} libros")
st.dataframe(df_filtrado)
