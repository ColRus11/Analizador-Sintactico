class Estudiante:
    def __init__(self, nombre, edad, calificaciones):
        self.nombre = nombre
        self.edad = edad
        self.calificaciones = calificaciones
    
    def promedio(self):
        return sum(self.calificaciones) / len(self.calificaciones)
    
    def es_mayor_de_edad(self):
        return self.edad >= 18

def crear_estudiantes():
    estudiantes = [
        Estudiante("Juan", 20, [8, 9, 7]),
        Estudiante("Ana", 17, [10, 9, 8]),
        Estudiante("Luis", 19, [6, 7, 5])
    ]
    return estudiantes

def imprimir_estudiantes(estudiantes):
    for estudiante in estudiantes:
        print("Nombre: " + estudiante.nombre + ", Promedio: " + str(estudiante.promedio()))
        if estudiante.es_mayor_de_edad():
            print(estudiante.nombre + " es mayor de edad.")
        else:
            print(estudiante.nombre + " no es mayor de edad.")

# Crear estudiantes y mostrar sus detalles
estudiantes = crear_estudiantes()
imprimir_estudiantes(estudiantes)
