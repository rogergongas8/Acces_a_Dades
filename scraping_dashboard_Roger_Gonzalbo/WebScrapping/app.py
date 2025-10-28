import streamlit as st
import pandas as pd

path = "libros.csv"
st.title("Web scraping app")

# Cargar datos
try:
    df = pd.read_csv(path)
except FileNotFoundError:
    st.error("No se ha encontrado el archivo 'libros.csv'. Ejecuta primero el script de scraping.")
    st.stop()

st.sidebar.header("Filtros")

# Aseguramos que los nombres de columnas sean correctos
if "precio" not in df.columns or "rating" not in df.columns:
    st.error("El CSV no contiene las columnas esperadas ('precio', 'rating').")
    st.stop()

# Slider de rango de precio
precio_min = float(df["precio"].min())
precio_max = float(df["precio"].max())

rango_precio = st.sidebar.slider(
    "Rango de precio (£)",
    min_value=precio_min,
    max_value=precio_max,
    value=(precio_min, precio_max)
)

# Selector de rating
rating_sel = st.sidebar.multiselect(
    "Filtrar por rating",
    options=sorted(df["rating"].unique()),
    default=sorted(df["rating"].unique())
)

# Filtrado de datos
df_filtrado = df[
    (df["precio"] >= rango_precio[0]) &
    (df["precio"] <= rango_precio[1]) &
    (df["rating"].isin(rating_sel))
]

st.write(f"Se muestran {len(df_filtrado)} libros de {len(df)} totales.")
st.dataframe(df_filtrado)

# Estadísticas básicas
st.subheader("Estadísticas")
st.write(df_filtrado.describe())

# Gráfico simple
st.subheader("Distribución de precios")
st.bar_chart(df_filtrado["precio"])
