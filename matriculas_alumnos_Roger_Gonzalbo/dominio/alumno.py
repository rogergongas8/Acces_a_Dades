class Alumno:
    def __init__(self, nombre: str):
        self.nombre = nombre

    def __str__(self):
        return f"Alumno: {self.nombre}"