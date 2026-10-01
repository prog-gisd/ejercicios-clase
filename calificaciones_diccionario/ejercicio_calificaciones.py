import random

alumnos: dict[str, float] = {
    "María": 7.7,
    "Jorge": 6.2,
    "Pablo": 9.5
}

base: str = "Alumno-"
for i in range(50):
    calificacion: float = round(random.random() * 10.0, 2)
    nombre = base + str(i)
    alumnos[nombre] = calificacion

print("Número de alumnos:", len(alumnos))

calificaciones = alumnos.values()
calificacion_media = sum(calificaciones)/len(alumnos)
print("Calificación media:", calificacion_media)

num_aprobados = 0
for calificacion in alumnos.values():
    if calificacion >= 5.0:
        num_aprobados += 1
num_suspensos = len(alumnos) - num_aprobados

print("Número de aprobados:", num_aprobados)
print("Número de suspensos:", num_suspensos)


listados: dict[str, list[str]] = {
    "SOBRESALIENTES": [],
    "NOTABLES": [],
    "APROBADOS": [],
    "SUSPENSOS": [],
    "LOS QUE SE EQUIVOCARON DE EXAMEN": []
}
for nombre, calificacion in alumnos.items():
    if calificacion >= 9.0:
        lista_sobresalientes: list[str] = listados["SOBRESALIENTES"]
        lista_sobresalientes.append(nombre)
    elif calificacion >= 7.0:
        listados["NOTABLES"].append(nombre)
    elif calificacion >= 5.0:
        listados["APROBADOS"].append(nombre)
    elif calificacion >= 2.0:
        listados["SUSPENSOS"].append(nombre)
    else:
        listados["LOS QUE SE EQUIVOCARON DE EXAMEN"].append(nombre)



for categoria, listado in listados.items():
    print("Alumnos con", categoria, "->", len(listado))
    for nombre in listado:
        print(nombre, "->", alumnos[nombre])
    print('-'*20)
    
    
    
print("COMIENZA LA BÚSQUEDA INTERACTIVAD DE CALIFICACIONES")
print("="*20)
fin: bool = False
while not fin:
    target: str = input("Dime de qué alumno quieres conocer la calificación: ")
    if not target: # target == "" o len(target) == 0
        fin = True
    print("Calificación de", target, "->", alumnos.get(target, "NP"))
else:
    print("FIN DE LA BÚSQUEDA DE NOMBRES")