import json
import csv
import logging
import matplotlib.pyplot as plt
# Hay que ejecutar el siguiente comando en la terminal
# para instalar el módulo matplotlib:
# pip install --upgrade matplotlib

# Ejemplo de configuración de logging
logging.basicConfig(
    handlers=[logging.FileHandler(
        filename='./logs/covid_charts.log',
        mode='a',
        encoding='utf-8')],
    format='%(asctime)s - %(name)s - %(levelname)s -> %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)
# Obteniendo un Logger concreto para este proceso
logger = logging.getLogger('Covid Charts')


class NonPopulationError(Exception):
    '''Excepción que representa un error cuando un objeto Country
    no tiene un valor para su atributo población.'''
    def __init__(self, country_name: str, extra_msg: str = ''):
        super().__init__("La población de " + country_name + ' no está disponible. ' + extra_msg)
        self.name = country_name

class Country:
    '''Clase que representa un país con los datos proporcionados
    por la Johns Hopkins University en el repositorio de
    github https://github.com/CSSEGISandData/COVID-19 '''
    def __init__(self, headers: list[str], datos: list[str]):
        '''El constructor de la clase Country recibe
        dos listas como parámetros:

        - headers: lista con todas las cabeceras del csv
        - raw_data: lista con los valores de una fila del csv'''
        self.province = datos[0]
        self.name = datos[1]
        self.latitude = datos[2]
        self.longitude = datos[3]
        # Configura un logger propio para este objeto
        self.country_logger = logging.getLogger('Country Logger de ' + self.name)
        
        # Carga todos los datos con sus fechas asociadas
        fechas = headers[4:]
        valores = datos[4:]
        self.datos: dict[str, int] = {}
        for i in range(len(fechas)):
            fecha_anglo: str = fechas[i]
            partes: list[str] = fecha_anglo.split('/')
            fecha_esp: str = partes[1]+'/'+partes[0]+'/'+partes[2]
            self.datos[fecha_esp] = int(valores[i])
        
        # Se definen otros dos atributos que 
        # solo se inicializarán si se necesitan
        self.casos_diarios: dict[str, int] = None
        self.population: int = None
        
        msg = "Datos cargados para " + self.name
        if self.province:
            msg += " - " + self.province
        self.country_logger.info(msg)
        
    def get_daily_cases(self) -> dict[str, int]:
        '''Método para calcular los casos diarios.
        
        Usando los datos de casos totales de los csv,
        genera un diccionario con las fechas como claves 
        y los casos diarios como valores asociados a dichas claves.'''
        # Se comprueba si ya está inicializado el atributo
        # self.casos_diarios, si no lo está, se inicializa.
        if not self.casos_diarios:
            self.casos_diarios = {}
            fechas: list[str] = list(self.datos.keys())
            datos: list[int] = list(self.datos.values())
            
            # Se calcula los casos diarios como los datos de un día
            # menos los datos del día anterior.
            for i in range(1, len(fechas)):
                # Comenzamos en el día 1 y no en el 0,
                # porque necesito poder acceder al
                # día anterior y no tengo días anteriores
                # al día 0 de mi lista.
                self.casos_diarios[fechas[i]] = datos[i]-datos[i-1]
                
            # Tras ver el resultado de la operación anterior,
            # se observan "anomalías". Por ejemplo, fechas que tienen
            # cifras muy elevadas junto a fechas que tiene 0 casos.
            # Esto es debido a que ciertos días no se registraban los datos
            # por ser fin de semana, festivos, etc.
            # Por lo tanto, dado que hay días sin incrementos de casos,
            # vamos a procesarlos para obtener una aproximación más cercana
            # a la realidad.
            
            # Para ello, vamos a realizar un "aplanamiento" de esos picos.
            # Y "aplanaremos" varias veces la curva, porque tendremos varios
            # días seguidos sin incrementos (sábados y domingos,
            # periodos festivos, etc.)
            
            # Número de veces que vamos a repetir el proceso
            repeticiones: int = 7
            for _ in range(repeticiones):
                fechas: list[str] = list(self.casos_diarios.keys())
                datos: list[int] = list(self.casos_diarios.values())
                for i in range(len(fechas)):
                    # "Aplanamos" los picos de nuestra curva
                    # asumiendo que un día hubo un número similar
                    # de contagios que el siguiente.
                    if datos[i] <= 0 and i+1 < len(fechas):
                        # Repartimos la mitad en cada día,
                        # ya que si no reducimos los que metemos en el día anterior,
                        # estaríamos metiendo "casos artificiales".
                        # Es decir, datos falsos/erróneos.
                        # Con esto, simplemente estamos repartiéndolos para
                        # aproximarnos a la realidad, que es: que los casos
                        # existián aunque no estaban siendo notificados.
                        self.casos_diarios[fechas[i]] = datos[i+1]/2
                        self.casos_diarios[fechas[i+1]] = datos[i+1]/2
        # Finalmente, se devuelve el diccionario de casos diarios.
        return self.casos_diarios
        
        
    def get_ai(self, size: int = 14) -> dict[str, int]:
        '''Esta función utiliza el propio atributo de
        casos_diarios para calcular la incidencia acumulada (IA).
        Usa el parámetro size (int, con un valor por defecto de 14)
        para determinar el tamaño de la ventana para el cálculo de IA.'''
        
        # En este caso, también podríamos tener una atributo 
        # que guardara el resultado de la incidencia acumulada,
        # pero esta vez debería ser un diccionario que tuviera
        # como claves, los tamaños de "ventanas" utilizados para
        # calcular esa incidencia acumulada y como valores,
        # los propios diccionarios de IA calculados en este método.

        # Esto lo dejo aquí como idea... (y como propuesta de ejercicio)
        # Este método solo va a calcular la incidencia acumulada con
        # una ventana igual al valor del parámetro size y lo devuelve.
        
        # Como necesitamos la población del país para calcular
        # el valor de incidencia acumulada, si no se tiene, se
        # lanza una excecpión.
        if not self.population:
            raise NonPopulationError(
                name=self.name,
                extra_msg='No se puede calcular la IA sin la población.')
        
        ia_country = {}
        diarios = self.casos_diarios if self.casos_diarios != None else self.get_daily_cases()
        fechas = list(diarios.keys())
        datos = list(diarios.values())
        
        # Ojo con la definición de estos límites en el siguiente for...
        # Para simplificar la explicación usaremos el ejemplo del cálculo de
        # IA a 7 días.
        # Si tengo una serie temporal de 15 días (posiciones 0 a 14 de mis listas),
        # solo puedo empezar a calcular la IA a 7 días desde el día 6 (del día 0 al día 6),
        # por eso la variable i empieza en el valor size-1 (7-1=6) y llega a 
        # tener un valor len(fechas)-1 (15-1=14), porque recordemos que la 
        # función range no incluye el límite superior.
        # Es decir, la secuencia de valores de i será: 6,7,8,9,10,11,12,13,14
        for i in range(size-1, len(fechas)):
            # Por lo tanto, para cada fecha, calculamos su IA con una ventana de días
            # definida por la variable size.
            ia=0
            # Siguiendo el ejemplo de IA a 7 días, comenzamos a sumar la ventana temporal
            # desde i-(size-1) (6-(7-1)=0), es decir, el primer valor de la lista,
            # hasta i+1 (6+1=7), usando 7 como límite superior del range,
            # tendremos la secuencia: 0,1,2,3,4,5,6 (exactamente los 7 primeros días)
            # que queremos usar para calcular la IA a 7 días del día 6.
            # 
            # Siguiendo la misma forma de proceder, cuando
            # i sea igual a 14 (último valor que toma i):
            # i-(size-1) = 14-(7-1)=8, e i+1 = 14+1 = 15,
            # por lo tanto, la secuencia de valores para i será:
            # 8,9,10,11,12,13,14 (de nuevo, 7 valores para calcular la IA a 7 días del día 14)
            for j in range(i-(size-1), i+1):
                ia += datos[j]
            # Se calcula la IA teniendo en cuenta la población del país
            ia = (ia/self.population)*100000
            # y se guarda en el diccionario con la fecha que se ha calculado como clave.
            ia_country[fechas[i]] = ia
        # Finalmente, devuelve el diccionario completo con fechas (string) como claves 
        # y la incidencia acumulada (int) como valor
        return ia_country

def load_countries(filename: str) -> list[Country]:
    '''Esta función recibe la ruta del fichero csv (string) donde
    están guardados los datos. Lee el fichero enteror
    y crea objetos Country con los datos de cada línea.

    Al finalizar la carga de todos los datos, devuelve una
    lista con todos los objetos Country creados.'''
    countries: list[Country] = []
    with open(file=filename, mode='r', encoding='utf8') as file:
        csv_reader = csv.reader(file)
        logger.debug("Leyendo fichero " + filename)
        headers: list[str] = None
        for linea in csv_reader:
            if headers == None:
                # La primera línea la guarda a parte para
                # usarla en el constructor del objeto Country.
                headers = linea
                logger.debug("Cargadas las cabeceras")
            else:
                # Crea un país y lo añade al a lista.
                country = Country(headers, linea)
                countries.append(country)
    # Devuelve la lista completa.
    return countries

def get_country(
    countries: list[Country],
    name: str,
    province: str = ''):
    '''Busca un objeto Country dentro de la lista facilitada hasta
    encontrar uno con los valores de:

    - name (string): Nombre del país
    - province (string): Nombre de la provincia con valor por defecto '' (string vacío)

    Si no encuentra ningún objeto Country que cumpla 
    con los requisitos, devuelve None'''
    for country in countries:
        if country.name == name and country.province == province:
            return country
    return None

def load_populations(filename: str) -> dict[str, int]:
    '''Carga el fichero json, especificado en el parámetro filename
    que contiene un diccionario con nombres de países como claves
    y las poblaciones de dichos países como valores.'''
    with open(filename, mode='r', encoding='utf8') as file:
        populations = json.load(file)
        return populations


# Proceso que carga los csv, crea los objetos Country y dibuja algunas gráficas.
if __name__ == '__main__':
    with open('index.json', mode='r', encoding='utf8') as file:
        indice = json.load(file)
    
    # Selecciona la fuente de datos entre las categorías disponibles.
    filename = indice['confirmed']
    countries: list[Country] = load_countries(filename)
    
    # Países que se van a analizar
    target_names: list[str] = [
        'Spain',
        'Portugal',
        'France',
        'Germany',
        'Italy'
        ]
    selected_countries: list[Country] = []
    for name in target_names:
        country: Country = get_country(countries, name)
        selected_countries.append(country)
    
    # Genera gráficas a partir de aquí
    for country in selected_countries:
        # Total de casos confirmados por fecha
        total = country.datos
        plt.plot(total.keys(), total.values(), label=country.name)
    plt.xlabel("Fecha")
    plt.ylabel("Total contagios confirmados")
    plt.legend()
    plt.show()
    
    for country in selected_countries:
        # Casos diarios confirmados por fecha
        daily_cases: dict[str, int] = country.get_daily_cases()
        plt.plot(daily_cases.keys(), daily_cases.values(), label=country.name)
    plt.xlabel("Fecha")
    plt.ylabel("Casos diarios confirmados")
    plt.legend()
    plt.show()
    
    # Carga las poblaciones de los países de los cuales se tienen datos de población
    populations: dict[str, int] = load_populations('./datos/population.json')
    for country_name, population in populations.items():
        country = get_country(countries, country_name)
        country.population = population
    
    for country in selected_countries:
        # Incidencia acumulada a 14 días por fecha
        daily_acummulated_incidence: dict[str, int] = country.get_ai()
        plt.plot(daily_acummulated_incidence.keys(), daily_acummulated_incidence.values(), label=country.name)
    plt.xlabel("Fecha")
    plt.ylabel("Incidencia acumulada a 14 días")
    plt.legend()
    plt.show()
    
    for country in selected_countries:
        # Incidencia acumulada a 7 días por fecha
        daily_acummulated_incidence: dict[str, int] = country.get_ai(size=7)
        plt.plot(daily_acummulated_incidence.keys(), daily_acummulated_incidence.values(), label=country.name)
    plt.xlabel("Fecha")
    plt.ylabel("Incidencia acumulada a 7 días")
    plt.legend()
    plt.show()