'''
Módulo para almacenar funciones que...
'''
import random

discotecas = {
    "Cats": 15.0,
    "Pachá": 30.0,
    "Iron": 5.0
}

respuestas_portero = {
    'bordes': [
        '¿Pero de qué vas? ¡Fuera de aquí!',
        'Esto es una mierda...',
        'Esto es insulante...'
    ],
    'afirmativas': [
        "Venga, entra pero que nadie te vea...",
        "Venga, que no miro...",
        "Vale, pero no se lo digas a nadie."
    ],
    'para_mayores': [
        'Por supuesto',
        'Que tengáis buena noche',
        'Cuidado con los abrigos'
    ]
}


def get_edad() -> int:
    '''
    Esta función devuelve la edad del usuario.
    Autor: a.carrera@upm.es
    '''
    respuesta: str = input("Dime tu edad: ")
    edad: int = int(respuesta)
    return edad


def es_mayor_de_edad(edad: int) -> bool:
    return edad >= 18


def elegir_discoteca() -> str:
    discoteca = input("¿Dónde vamos? ")
    while discoteca not in discotecas:
        discoteca = input("No conozco es discoteca. Dime otra: ")
    print("De acuerdo. Vamos a", discoteca)
    return discoteca


def intenta_soborno(nombre: str) -> bool:
    soborno_al_portero = float(input("¿Cuánto dinero le das al portero? "))
    coste = discotecas[nombre]
    if soborno_al_portero >= coste:
        print(random.choice(respuestas_portero["afirmativas"]))
        return True
    else:
        print(random.choice(respuestas_portero["bordes"]))
        return False


def conversacion_con_portero(discoteca: str, mayor_de_edad: bool = False) -> bool:
    if mayor_de_edad:
        print(random.choice(respuestas_portero["para_mayores"]))
        return True
    else:
        print("Eres menor de edad... y no te dejan entrar.")
        soborno = input("¿Quieres sobornar al portero? ")
        # Se define una lista de respuestas aceptables a la pregunta previa
        passwords = ["Sí", "Si", "si", "sí", "venga va", "vale", "Vale"]
        if soborno in passwords:
            soborno_exitoso = intenta_soborno(discoteca)
            return soborno_exitoso
        else:
            print("Pues nada... vete a casa.")
            return False


if __name__ == '__main__':
    print("Este es un módulo de biblioteca.")
    print("Simplemente almacena funciones.")
