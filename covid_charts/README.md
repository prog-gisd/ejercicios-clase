# Instrucciones para ejecutar el ejercicio del COVID19

Esta carpeta contiene todo el código del ejercicio desarrollado en clase sobre los
datos del caso de esudio del COVID19.

Todos los ficheros contienen comentarios explicando cada paso que se sigue y documentando lo que es necesario.

Para ejecutarlo correctamente, seguid las siguientes instrucciones:

- Para evitar tener problemas de rutas de ficheros, verificad que estáis en el directorio correcto en vuestra terminal. Si no es así, navegad por vuestro árbol de directorios con el comando "cd".
- Una vez que estéis en el directorio "covid_charts", podéis ejecutar cualquiera de los tres fichero".py" con: python "nombre del fichero".
- El orden correcto es el siguiente:

1. covid_sources.py para generar el fichero "sources_url.json"
2. covid_data.py para descargar los ficheros csv
3. covid_charts.py para cargar dichos ficheros y visualizar las gráficas.

Recordad que hay que instalar los módulos requests y matplotlib tal como se indica en los comentarios que se encuentra dentro del código.

El único fichero de datos que se incluye es el "population.json" con las poblaciones de algunos países. Todos los demás se generan/descargan ejecutando el código.

Por último, recordad crear una carpeta logs dentro de la carpeta "covid_charts" para que se puedan escribir los logs en ese directorio.