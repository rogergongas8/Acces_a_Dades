import requests
from bs4 import BeautifulSoup
import pandas as pd

# --- Configuración inicial ---
URL_CATALOGO = "https://books.toscrape.com"
datos_libros = []

mapa_rating = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}

print("Iniciando scraping (método 'for' para 50 páginas)...")

for i in range(1, 10):

    # Construimos la URL a mano para cada página
    url_pagina = f"{URL_CATALOGO}page-{i}.html"

    print(f"Descargando: {url_pagina}")
    page = requests.get(url_pagina)

    # Si una página falla la saltamos
    if page.status_code != 200:
        print(f"Error en página {i}. Saltando...")
        continue

    soup = BeautifulSoup(page.content, 'html.parser')
    libros = soup.find_all('article', class_='product_pod')

    # Extracción de datos de la página
    for libro in libros:
        titulo = libro.h3.a["title"]
        precio_texto = libro.find("p", class_="price_color").get_text()
        precio = float(precio_texto.replace("£", ""))
        clase_rating = libro.find("p", class_="star-rating")["class"][1]
        rating = mapa_rating.get(clase_rating, 0)

        datos_libros.append({
            "titulo": titulo,
            "precio": precio,
            "rating": rating,
        })

# --- Guardado final de los datos ---
print(f"\nTotal de libros scrapeados: {len(datos_libros)}")
df = pd.DataFrame(datos_libros)
df.to_csv("libros.csv", index=False)
print("Datos Guardados en libros.csv")
