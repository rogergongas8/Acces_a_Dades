import streamlit as st
import pandas as pd

path = "libros.csv"
st.title("Web scraping app")

try:
    df = pd.read_csv(path)
except FileNotFoundError:
    st.write("No se han encontrado el archivo csv")

st.sidebar.header("Filtros")

precio_min = float(df["Precio"].min())
precio_max = float(df["Precio"].max())

rango_precio = st.sidebar.slider(
    "
)