# Diccionario de supermercados keys=nombres y values = diccionario de producto/precio
supermercados = {
    "mercadona": {
        "azúcar": 2.0,
        "verdura": 12.0,
        "carne": 20.5,
        "pescado": 17.3,
        "leche": 3.2,
        "huevos": 4.3
    },
    "dia": {
        "azúcar": 2.0,
        "verdura": 11.0,
        "carne": 18.5,
        "pescado": 17.3,
        "huevos": 4.3
    },
    "consum": {
        "azúcar": 2.0,
        "verdura": 11.0,
        "carne": 18.5,
        "pescado": 17.3,
        "huevos": 4.3,
        "cereales": 5.1
    },
    "lidl": {
        "azúcar": 2.0,
        "verdura": 11.0,
        "carne": 18.5,
        "pescado": 17.3,
        "huevos": 4.3,
        "cereales": 5.1
    },
    "carrefour": {
        "azúcar": 2.0,
        "verdura": 11.0,
        "carne": 18.5,
        "pescado": 17.3,
        "huevos": 4.3,
        "cereales": 5.1
    },
    "aldi": {
        "azúcar": 2.0,
        "verdura": 11.0,
        "carne": 18.5,
        "pescado": 17.3,
        "huevos": 4.3,
        "cereales": 5.1
    },
    "supercor": {
        "azúcar": 2.0,
        "verdura": 11.0,
        "carne": 18.5,
        "pescado": 17.3,
        "huevos": 4.3,
        "cereales": 5.1
    },
    "corte ingés": {
        "azúcar": 2.0,
        "verdura": 11.0,
        "carne": 18.5,
        "pescado": 17.3,
        "huevos": 4.3,
        "cereales": 5.1
    },
    "sanchez romero": {
        "azúcar": 2.0,
        "verdura": 11.0,
        "carne": 18.5,
        "pescado": 17.3,
        "huevos": 4.3,
        "caviar": 200
    }
}

def elegir_supermercado() -> str:
    respuesta = input("¿Donde quieres comprar hoy? En el:\n")
    if respuesta in supermercados.keys():
        print("Vale, compramos en", respuesta)
        return respuesta
    else:
        print("Ese supermercado no está disponible en esta tienda online.")
        exit(1)

def imprimir_ticket(cesta: list[str]) -> None:
    
    total_a_pagar = 0

    # aquí definimos una lista de alimentos que solo se han pedido una vez
    productos_unicos = []
    cantidad = []  # aqui se pone un numerito en función a la csantidad que hemos pedido de cada cosa
    for alimento in cesta:
        if alimento not in productos_unicos:
            # aqui añades los alimentos que hemos pedido en general
            productos_unicos.append(alimento)
            cantidad.append(1)  # y pones un uno en cantidad
        else:  # si has pedido varias cantidades de un alimento
            # con esto incluimos en productos unicos las cantidades de más
            index = productos_unicos.index(alimento)
            cantidad_previa = cantidad[index]
            # y con esto sumas 1 a la cantidad inicial en funcion a cuantas unidades de más has pedido
            cantidad[index] = cantidad_previa+1

    for alimento in productos_unicos:  # y este ultimo for es el que genera el tiket
        # definimos el precio por unidad con un index
        precio_unitario = listado_precios.get(alimento, 0.0)
        # definimos el numero de unidades con otro index
        unidades = cantidad[productos_unicos.index(alimento)]
        # multiplicamos el numero de unidad por la cantidad de unidades
        precio = precio_unitario * unidades
        total_a_pagar += precio  # sumamos todo

        # y se imprime todo

        print(unidades, "x", alimento, "(", precio_unitario, "€) ->", precio, "€")

    print("TOTAL:", total_a_pagar, "€")

def get_cesta_con_asistente(listado_precios: dict[str, float]) -> list[str]:
    cesta = []
    while True:  # utilizamos while para que te siga preguntando todo el rato que alimento quieres
        alimento = input("¿qué alimento necesita? ")
        if alimento == "No quiero nada más" or alimento == "Quiero pagar ya":
            break  # si pones q no quieres más, con el break salta directamente al tiket de la compra
        elif alimento in listado_precios:
            cesta.append(alimento)  # si está, se añade directamente a la cesta
            print("De acuerdo, he añadido", alimento, "a tu cesta de la compra.")
        else:
            print("Lo siento, pero no tenemos ese producto")
    return cesta

# Inicio del programa principal
if __name__ == '__main__':
    supermercado_objetivo: str = elegir_supermercado()
    listado_precios: dict[str, float] = supermercados.get(supermercado_objetivo)
    cesta = get_cesta_con_asistente(listado_precios)
    imprimir_ticket(cesta)