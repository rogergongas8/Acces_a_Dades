import tkinter as tk
from tkinter import scrolledtext
import google.generativeai as genai
import os
from dotenv import load_dotenv

# --- Configuración Inicial ---

# 1. Cargar la clave API desde el archivo .env
load_dotenv()
API_KEY = os.getenv('API_KEY')

# Verificar si la clave API se cargó correctamente
if not API_KEY:
    print("Error: No se encontró la API_KEY. Asegúrate de crear un archivo .env con API_KEY=tu_clave")
    exit()

# 2. Configurar la API de Google Gemini
try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-2.5-pro')
except Exception as e:
    print(f"Error al configurar Gemini: {e}")
    exit()


# 3. Función para leer el contexto
def cargar_contexto():
    try:
        with open("servicios.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print("Error: No se encontró el archivo 'servicios.txt'.")
        return "No hay información de servicios disponible."


# --- Lógica del Asistente ---

def enviar_mensaje():
    pregunta_usuario = entrada_usuario.get()
    if not pregunta_usuario.strip():
        return

    # Mostrar la pregunta del usuario en el chat
    area_chat.config(state=tk.NORMAL)
    area_chat.insert(tk.END, f"Tú: {pregunta_usuario}\n\n")
    area_chat.config(state=tk.DISABLED)

    # Limpiar la barra de entrada
    entrada_usuario.delete(0, tk.END)

    try:
        # 4. Combinar el contexto con la pregunta
        contexto = cargar_contexto()
        prompt_completo = f"""
        **Contexto (Información de la Peluquería):**
        {contexto}

        **Instrucción:**
        Eres un asistente virtual de la peluquería "Cortecitos".
        Responde la pregunta del usuario basándote **únicamente** en el contexto proporcionado.
        Si la pregunta no se puede responder con el contexto, dilo amablemente.

        **Pregunta del Usuario:**
        {pregunta_usuario}
        """

        # 5. Llamar a la API de Gemini
        response = model.generate_content(prompt_completo)

        # 6. Procesar la respuesta (manejo básico de la respuesta)
        respuesta_ia = response.text

        # Mostrar la respuesta del asistente en el chat
        area_chat.config(state=tk.NORMAL)
        area_chat.insert(tk.END, f"Asistente: {respuesta_ia}\n\n")
        area_chat.config(state=tk.DISABLED)
        area_chat.see(tk.END)

    except Exception as e:
        area_chat.config(state=tk.NORMAL)
        area_chat.insert(tk.END, f"Error: No se pudo conectar con la API. {e}\n\n")
        area_chat.config(state=tk.DISABLED)


# --- Creación de la Interfaz Gráfica ---

ventana = tk.Tk()
ventana.title("Asistente de Peluquería IA")
ventana.geometry("500x600")

# Área de chat para mostrar la conversación
area_chat = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, state=tk.DISABLED, font=("Arial", 11))
area_chat.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

# Frame para la entrada y el botón
frame_entrada = tk.Frame(ventana)
frame_entrada.pack(padx=10, pady=10, fill=tk.X)

# Cuadro de texto para la pregunta del usuario
entrada_usuario = tk.Entry(frame_entrada, font=("Arial", 11))
entrada_usuario.pack(side=tk.LEFT, expand=True, fill=tk.X, ipady=5)

# Botón de Enviar
boton_enviar = tk.Button(frame_entrada, text="Enviar", command=enviar_mensaje)
boton_enviar.pack(side=tk.RIGHT, padx=5)

# --- Iniciar la aplicación ---

# Mensaje de bienvenida inicial
area_chat.config(state=tk.NORMAL)
area_chat.insert(tk.END, "¡Hola! Soy el asistente de la Peluquería Brillo Estelar. ¿En qué puedo ayudarte hoy?\n\n")
area_chat.config(state=tk.DISABLED)

# Ejecutar el bucle principal de Tkinter
ventana.mainloop()