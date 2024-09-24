'''
Nombre: mis_funciones
Autor: Álvaro Carrera (a.carrera@upm.es)
nblbblalbajsdlkfajfd


'''
import string

def es_primo(num: int) -> bool:
    if num < 2:
        print("Los números primos son aquellos naturales mayores que 1 que solo son didivasdfljkasñlfjasdl")
        return False
    # for i in range(2,num):
    rango = range(2,num)
    for i in rango:
        if num%i == 0:
            return False
    # return True
    else:
        return True
    
    
def es_robusta(password: str) -> bool:
    '''
    - longitud mínima: 8
    - al menos 1 mayúscula
    - al menos 1 minúscula
    - al menos 1 símbolo
    - al menos 1 número
    '''
    if len(password) < 8:
        return False
    # condiciones = [False, False, False, False]
    # condiciones = []
    # for i in range(4):
    #     condiciones.append(False)
    condiciones = [False for i in range(4)]
    for caracter in password:
        print("Evaluando el caracter:", caracter)
        if caracter.isupper():
            condiciones[0] = True
        elif caracter.islower():
            condiciones[1] = True
        elif caracter.isnumeric():
            condiciones[3] = True
        elif caracter in string.punctuation:
            condiciones[2] = True
        
        for condicion in condiciones:
            if not condicion:
                break
        else:
            print("Contraseña robusta")
            return True
    else:
        print("Contraseña débil")
        return False
    
if __name__ == '__main__':
    # while True:
        # msg = input("Introduce un número entero: ")
        # if msg == "stop":
        #     break
        # x = int(msg)
        # primo = es_primo(x)
        # print(primo)
        
    password = input("Introduce una contraseña para comprobar: ")
    while not es_robusta(password):
        password = input("Introduce otra más robusta: ")
    else:
        print("De acuerdo, tu contraseña es: ", password)
