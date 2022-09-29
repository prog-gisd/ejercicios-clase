'''
Este ejemplo trata de mostrar el uso de sentencias
condicionales usando también listas e inputs
'''
from funciones_disco import get_edad, conversacion_con_portero, es_mayor_de_edad, elegir_discoteca

'''
Inicio del programa
'''
if __name__ == '__main__':
    edad: int = get_edad()
    print(edad)
    disco = elegir_discoteca()
    has_entrado = conversacion_con_portero(
        discoteca=disco,
        mayor_de_edad=es_mayor_de_edad(edad)
    )

    if has_entrado:
        print("Venga, ahora fiesta!")
    else:
        print("A tu casa a jugar al parchís")
else:
    print("disco.py no es el módulo principal en esta ocasión")
