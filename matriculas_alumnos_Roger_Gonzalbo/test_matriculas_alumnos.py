from dominio.alumno import Alumno
from servicio.AlumnosMatriculados import AlumnosMatriculados


def mostrar_menu():
    print("\n--- MENU ---")
    print("1. Matricular alumno")
    print("2. Listar alumnos")
    print("3. Eliminar archivo de alumnos")
    print("4. Salir")


def ejecutar_menu():
    while True:
        mostrar_menu()
        opcion = input("Selecciona una opcion: ")

        if opcion == "1":
            nombre = input("Nombre del alumno: ").strip()
            if not nombre:
                print("El nombre no puede estar vacío.")
                continue
            alumno = Alumno(nombre)
            AlumnosMatriculados.matricular_alumno(alumno)

        elif opcion == "2":
            AlumnosMatriculados.listar_alumnos()

        elif opcion == "3":
            nombre = input("Nombre del alumno a eliminar: ").strip()
            AlumnosMatriculados.eliminar_alumno(nombre)

        elif opcion == "4":
            print("Saliendo del programa...")
            break

        else:
            print("Opción no válida. Intenta de nuevo.")


if __name__ == "__main__":
    ejecutar_menu()