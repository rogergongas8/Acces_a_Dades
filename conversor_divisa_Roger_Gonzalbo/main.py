import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import messagebox, ttk
import requests

URL = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"


def obtener_datos():
    try:
        response = requests.get(URL)
        if response.status_code == 200:
            root = ET.fromstring(response.content)

            tasas = {'EUR': 1.0}
            fecha = "Desconocida"

            for child in root.iter():
                if 'time' in child.attrib:
                    fecha = child.attrib['time']

                if 'currency' in child.attrib:
                    currency = child.attrib['currency']
                    rate = float(child.attrib['rate'])

                    tasas[currency] = rate


            return fecha, tasas

        else:
            messagebox.showerror("Error", "No se pudo conectar")
            return None, {}
    except Exception as e:
        messagebox.showerror("Error", f"Fallo: {e}")
        return None, {}


def convertir():
    try:
        importe = float(entry_cantidad.get())
        origen = combo_de.get()
        destino = combo_a.get()

        if origen in tasas_datos and destino in tasas_datos:
            tasa_origen = tasas_datos[origen]
            tasa_destino = tasas_datos[destino]

            resultado = (importe / tasa_origen) * tasa_destino
            lbl_resultado.config(text=f"{resultado:.2f} {destino}")
        else:
            messagebox.showwarning("Aviso", "Selecciona monedas válidas")
    except ValueError:
        messagebox.showerror("Error", "Introduce solo números")



root = tk.Tk()
root.title("Conversor Divisas BCE")

fecha_datos, tasas_datos = obtener_datos()

tk.Label(root, text=f"Fecha datos: {fecha_datos}").pack(pady=5)

tk.Label(root, text="Cantidad:").pack()
entry_cantidad = tk.Entry(root)
entry_cantidad.pack()

tk.Label(root, text="De:").pack()
combo_de = ttk.Combobox(root, values=list(tasas_datos.keys()))
combo_de.pack()
combo_de.set("EUR")

tk.Label(root, text="A:").pack()
combo_a = ttk.Combobox(root, values=list(tasas_datos.keys()))
combo_a.pack()
combo_a.set("USD")

btn_calc = tk.Button(root, text="Calcular", command=convertir)
btn_calc.pack(pady=10)

lbl_resultado = tk.Label(root, text="---", font=("Arial", 14, "bold"))
lbl_resultado.pack(pady=10)

root.mainloop()