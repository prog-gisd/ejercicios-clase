import json
import logging

# Datos proporcionados públicamente por la Johns Hopkins University
# a través de su Center for Systems Science and Engineering (CSSE)
# publicados en el repositorio de Github
# https://github.com/CSSEGISandData/COVID-19 

# Ejemplo de configuración de logging
logging.basicConfig(
    handlers=[logging.FileHandler(
        filename='./logs/covid_sources.log',
        mode='a',
        encoding='utf-8')],
    format='%(asctime)s - %(name)s - %(levelname)s -> %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)
# Obteniendo un Logger concreto para este proceso
logger = logging.getLogger('Covid Sources')


# Proceso de creación de archivo resumen de las URLs originales.
if __name__ == '__main__':
    raw_urls: dict[str, str] = {}
    raw_urls['confirmed'] = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
    raw_urls['deaths'] = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
    raw_urls['recovered'] = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'

    filename = './datos/source_urls.json'
    try:
        with open(file=filename, mode='w', encoding='utf8') as file:
            json.dump(raw_urls, file, indent=3)
            logger.info("Fichero " + filename + " escrito correctamente.")
    except Exception as e:
        logger.error("No se ha podido escribir el fichero " + filename)
        logger.error(e.__str__)
