'''
Solución del Ejercicio 4 de la prueba realizada el
6 de octubre de 2022 en el aula de clase.

El enunciado está disponible en el Moodle de la asignatura.
Aunque se incluyen pequeños comentarios, este fichero no pretende
ser autocontenido. Por lo que se necesita el enunciado para entenderlo.
'''

'''INICIO DE LA SOLUCIÓN DEL EJERCICIO'''


def calcula_duracion_ola_de_calor(
        actual: list[tuple[str, float]],
        historico: list[tuple[str, float]]) -> int:
    '''Implementación de la función que se pide en el problema'''
    # Opción de finalización 1: longitudes erróneas
    if len(actual) > len(historico):
        print("Longitud de las listas -> error")
        print("Históricos no compatibles.")
        return -1

    # Se define un contador para la cantidad de días de la ola de calor
    contador = 0
    # Se recorre la lista desde el final
    for i in range(len(actual)):
        pos = -(i+1)
        # Se recuperan las tuplas de una posición específica (-1, -2, etc.)
        tupla_actual: tuple[str, float] = actual[pos]
        tupla_hist: tuple[str, float] = historico[pos]
        # Opción de finalización 2: fechas erróneas
        if tupla_actual[0] != tupla_hist[0]:
            print("Las fechas no cuadran en la posición", pos)
            print("actual ->", tupla_actual[0])
            print("histórico ->", tupla_hist[0])
            return -2
        elif tupla_actual[1] > tupla_hist[1]:
            # Si la temperatura es mayor, se cuenta un día más
            contador += 1
        else:
            # Si no, ya terminó la ola de calor actual
            break

    # Opción de salida 3: la ola de calor no dura lo suficiente
    if contador < 3:
        return -3
    else:
        # Opción de salida 4: duración de la ola de calor activa
        return contador


'''FIN DEL EJERCICIO'''


# Ejemplos de los parámetros que se usarán en la función
actual: list[tuple[str, float]] = [
    ("06/10/2022", 19.5),
    ("07/10/2022", 20.5),
    ("08/10/2022", 18.5),
    ("09/10/2022", 18.5)
]
historico: list[tuple[str, float]] = [
    ("06/10/2022", 10.5),
    ("07/10/2022", 8.5),
    ("08/10/2022", 11.5),
    ("09/10/2022", 12.5)
]

print('Probando la función 1: Calculando la duración de la ola de calor actual')
duracion_ola: int = calcula_duracion_ola_de_calor(actual, historico)
if duracion_ola < 0:
    print("Error: ", duracion_ola)
else:
    print("La ola de calor actual está durando", duracion_ola)



'''Se incluye a continuación otra posible función sobre los mismos datos'''
def dias_mas_calurosos(
        actual: list[tuple[str, float]],
        historico: list[tuple[str, float]],
        umbral: float = 5.0) -> list[str]:
    '''Función que devuelve una lista de los días que han sido
    más caluros que la media histórica para esa fecha por una 
    cantidad dada (valor del parámetro umbral).
    
    Se podrían hacer las mismas comprobaciones de longitudes y fechas
    que en la función anterior; pero no se repite por simplicidad.'''

    # Se define la lista donde iremos metiendo las fechas
    lista: list[str] = []
    # Se recorre la lista desde el final
    for i in range(len(actual)):
        pos = -(i+1)
        # Se recuperan las tuplas, igual que antes
        tupla_actual: tuple[str, float] = actual[pos]
        tupla_hist: tuple[str, float] = historico[pos]
        # Condición para ver si el día fue lo suficientmente caluroso
        if tupla_actual[1] - tupla_hist[1] >= umbral:
            # Si es así, se incluye en la lista
            lista.append(tupla_actual[0])
    # Se devuelve la lista resultante
    return lista


print('Probando la función 2: Lista de días más calurosos')
dias: list[str] = dias_mas_calurosos(actual, historico, umbral=7.0)
print("Los días más caluroso han sido:")
for dia in dias:
    print("\t-", dia)
