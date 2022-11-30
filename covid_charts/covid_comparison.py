from covid_charts import Country, load_countries, get_country, load_populations
import json
import matplotlib.pyplot as plt
import logging

# Ejemplo de configuración de logging
logging.basicConfig(
    handlers=[logging.FileHandler(
        filename='./logs/covid_comparison.log',
        mode='a',
        encoding='utf-8')],
    format='%(asctime)s - %(name)s - %(levelname)s -> %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)
# Obteniendo un Logger concreto para este proceso
logger = logging.getLogger('Covid Charts')

def show_chart(
    xlabel: str = '',
    ylabel: str = '',
    **datos: dict[str, dict[str, int]]) -> None:
    '''Función que recibe un número indeterminado de
    diccionarios para mostrar todos ellos en las gráficas.
    
    Se le pasan como parámetros las etiquetas de ambos ejes
    y los diccionarios. Se usan las keywords de los parámetros
    como nombres de esa serie numérica.'''
    
    # Se cogen las keywords y los datos (diccionarios)
    for k, v in datos.items():
        # Por ejemplo, si se recibe el argumento:
        # Confirmados=country.get_ai()
        # k será igual al string "Confirmados"
        # y v será igual al resultado de la función
        # get_ai(), es decir, un dict[str, int]
        plt.plot(v.keys(), v.values(), label=k)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()

if __name__ == '__main__':
    with open('index.json', mode='r', encoding='utf8') as file:
        indice = json.load(file)
    
    # Selecciona la fuente de datos entre las categorías disponibles.
    filename = indice['confirmed']
    countries_confirmed: list[Country] = load_countries(filename)
    logger.info("Cargada la información de casos confirmados.")
    filename = indice['deaths']
    countries_deaths: list[Country] = load_countries(filename)
    logger.info("Cargada la información de defunciones.")
    
    # Países que se van a analizar
    target_names: list[str] = [
        'Spain',
        'Portugal',
        'France',
        'Germany',
        'Italy'
        ]
    selected_countries_confirmed: list[Country] = []
    selected_countries_deaths: list[Country] = []
    for name in target_names:
        country: Country = get_country(countries_confirmed, name)
        selected_countries_confirmed.append(country)
        country_deaths: Country = get_country(countries_deaths, name)
        selected_countries_deaths.append(country_deaths)
    logger.info("Datos de los países objetivo cargados correctamente.")
    
    # Carga las poblaciones de los países de los cuales se tienen datos de población
    populations: dict[str, int] = load_populations('./datos/population.json')
    logger.info("Fichero de poblaciones cargado correctamente.")
    for country_name, population in populations.items():
        country = get_country(countries_confirmed, country_name)
        country.population = population
        country_deaths = get_country(countries_deaths, country_name)
        country_deaths.population = population
        logger.debug("Población de " + country_name + " -> " + str(population))
    logger.info("Poblaciones de los países objetivo cargadas correctamente.")
        
    target_country_name = 'Spain'
    logger.info("Generando gráficas para: " + target_country_name)
    country_confirmed = get_country(countries_confirmed, target_country_name)
    country_deaths = get_country(countries_deaths, target_country_name)
    
    # Genera gráficas a partir de aquí
    # Total de casos confirmados por fecha
    show_chart(
        xlabel="Fecha",
        ylabel=target_country_name + " - Total",
        Confirmados=country_confirmed.datos,
        Muertes=country_deaths.datos)
    
    show_chart(
        xlabel="Fecha",
        ylabel=target_country_name + " - Casos diarios",
        Confirmados=country_confirmed.get_daily_cases(),
        Muertes=country_deaths.get_daily_cases())
    
    show_chart(
        xlabel="Fecha",
        ylabel=target_country_name + " - IA a 14 días",
        Confirmados=country_confirmed.get_ai(),
        Muertes=country_deaths.get_ai())
    
    show_chart(
        xlabel="Fecha",
        ylabel=target_country_name + " - Gráfica Mixta",
        IA_14=country_confirmed.get_ai(),
        IA_7=country_confirmed.get_ai(size=7),
        Muertes=country_deaths.get_daily_cases())