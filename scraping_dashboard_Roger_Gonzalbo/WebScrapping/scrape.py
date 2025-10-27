import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://books.toscrape.com/"
page = requests.get(URL)

print("Descargando html...")
soup = BeautifulSoup(page.content, 'html.parser')

# Buscamos los contendedores de los libros
libros = soup.find_all('article', class_='product_pod')
print(f"Se han encontrado {len(libros)} libros")

datos_libros = []

#Mapeo para convertir el rating de texto a numero
mapa_rating = {
    "One" : 1,
    "Two" : 2,
    "Three" : 3,
    "Four" : 4,
    "Five" : 5,
}

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
df = pd.DataFrame(datos_libros)
df.to_csv("libros.csv", index=False)
print("Datos Guardados")