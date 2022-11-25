import json
import logging
import requests as req
# Para que este último import funcione,
# hay que instalar ese módulo en nuestro sistema.
# Para ello, ejecutar el siguiente comando 
# en la consola del sistema:
# pip install --upgrade requests


# Ejemplo de configuración de logging
logging.basicConfig(
    handlers=[logging.FileHandler(
        filename='./logs/covid_data.log',
        mode='a',
        encoding='utf-8')],
    format='%(asctime)s - %(name)s - %(levelname)s -> %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S'
)
# Obteniendo un Logger concreto para este proceso
logger = logging.getLogger('Covid Data')

def descarga_datos(source_url: str) -> str:
    '''Función que se conecta a una URL remota y descarga el contenido.
    Lo lee usando la codificación UTF-8 y devuelve el contenido de la
    URL como un string.'''
    response = req.get(url=source_url)
    return response.content.decode('utf8')

def guarda_en_fichero(datos: str, ruta: str) -> None:
    '''Función que guarda el texto que le pasas en datos (string)
    en el fichero con nombre ruta_fichero (string)

    Si la ruta indice algún subdirectorio, este método no creará
    dicho directorio, si no que lanzará un error. Por lo tanto,
    los directorios deberán estar creados a priori.'''
    with open(file=ruta, mode='w', encoding='utf8') as file:
        file.write(datos)

# Proceso de descarga de las URLs originales y guardado en ficheros csv.
if __name__ == '__main__':
    source_filename = './datos/source_urls.json'
    
    with open(file=source_filename, mode='r', encoding='utf8') as file:
        source_urls: dict[str, str] = json.load(file)
    logger.debug("Fichero de urls cargado correctamente.")

    logger.info("Categorías disponibles para descargar:")
    for clave in source_urls:
        logger.info("- " + clave)
    
    # Diccionario para guardar la ruta en la que se han
    # descargado los csv descargados.
    indice: dict[str, str] = {}
    for categoria, url in source_urls.items():
        datos_originales = descarga_datos(url)
        filename = './datos/'+categoria+'.csv'
        guarda_en_fichero(datos=datos_originales, ruta=filename)
        logger.info("Fichero guardado en " + filename)
        indice[categoria] = filename
    
    # Genera un fichero de índice para saber dónde está cada uno de los
    # ficheros descargados.
    index_filename = 'index.json'
    with open(file=index_filename, mode='w', encoding='utf8') as file:
        json.dump(indice, file, indent=3)
        logger.info("Índice de datos descargados guardado en " + index_filename)
    

    