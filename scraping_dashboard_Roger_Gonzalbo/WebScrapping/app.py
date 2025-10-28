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

# Verificación de columnas
if "precio" not in df.columns or "rating" not in df.columns:
    st.error("El CSV no contiene las columnas esperadas ('precio', 'rating').")
    st.stop()

# Slider para rango de precio
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

# Cálculo de promedios
precio_promedio = df_filtrado["precio"].mean()
rating_promedio = df_filtrado["rating"].mean()

# Fila de promedios más visual
st.subheader("📊 Promedios generales")
col1, col2 = st.columns(2)

col1.metric(
    label="💷 Precio promedio",
    value=f"£{precio_promedio:.2f}"
)

col2.metric(
    label="⭐ Rating promedio",
    value=f"{rating_promedio:.2f} / 5"
)

# Gráfico simple
st.subheader("Distribución de precios")
st.bar_chart(df_filtrado["precio"])
