from dominio.alumno import Alumno
import os

class AlumnosMatriculados:
    archivo = "alumnos.txt"

    @staticmethod
    def matricular_alumno(alumno: Alumno):
        with open(AlumnosMatriculados.archivo, "a", encoding="utf-8") as archivo:
            archivo.write(f"{alumno.nombre}\n")
        print(f"Alumno '{alumno.nombre}' matriculado correctamente.")

    @staticmethod
    def listar_alumnos():
        if not os.path.exists(AlumnosMatriculados.archivo):
            print("No hay alumnos matriculados todavía.")
            return

        print("\nLista de alumnos matriculados:")
        with open(AlumnosMatriculados.archivo, "r", encoding="utf-8") as archivo:
            alumnos = archivo.readlines()
            for alumno in alumnos:
                print(f"- {alumno.strip()}")

    @staticmethod
    def eliminar_alumno(nombre: str):
        if not os.path.exists(AlumnosMatriculados.archivo):
            print("No existe el archivo de alumnos.")
            return

        with open(AlumnosMatriculados.archivo, "r", encoding="utf-8") as archivo:
            alumnos = [linea.strip() for linea in archivo]

        if nombre not in alumnos:
            print(f"No se encontró al alumno '{nombre}'.")
            return

        alumnos.remove(nombre)

        with open(AlumnosMatriculados.archivo, "w", encoding="utf-8") as archivo:
            for alumno in alumnos:
                archivo.write(f"{alumno}\n")

        print(f"Alumno '{nombre}' eliminado correctamente.")