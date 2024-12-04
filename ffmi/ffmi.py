from enum import Enum
from typing import Any
import pickle
import json
import csv
import logging

# logging.basicConfig(level=logging.WARNING, filename='ffmi3.log')
# Configuring log file
log_file="ffmi_new.log"
logging.basicConfig(
    handlers=[logging.FileHandler(
        filename=log_file,
        mode='a',
        encoding='utf-8')],
    format='%(asctime)s - %(name)s - %(levelname)s -> %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger('Loggger FFMI')


class ValorParametroIncorrectoError(Exception):
    def __init__(self, **kwargs) -> None:
        super().__init__("Los parámetros tienen un valor no aceptado por la función " + str(kwargs.get("funcion")))
        logger.warning("Los parámetros tienen un valor no aceptado por la función " + str(kwargs.get("funcion")))
        self.altura = kwargs.get("altura")
        self.peso = kwargs.get("peso")
        self.porcentaje_grasa = kwargs.get("porcentaje_grasa")

class Pesaje:
    def __init__(self, altura: int, peso: float, porcentaje_grasa: float):
        if altura <= 0 or peso <= 0 or porcentaje_grasa >= 100 or porcentaje_grasa <= 0:
            raise ValorParametroIncorrectoError(
                funcion=Pesaje.__init__,
                altura=altura,
                peso=peso,
                porcentaje_grasa=porcentaje_grasa)
        self.altura = altura
        self.peso = peso
        self.porcentaje_grasa = porcentaje_grasa
        logger.info("Pesaje creado -> Altura: " + str(altura) + " Peso: " + str(peso) + " Grasa: " + str(porcentaje_grasa))

class SexoBiologico(Enum):
    HOMBRE = 1
    MUJER = 2

class NivelFFMI(Enum):
    BAJO = 1
    MEDIO = 2
    ALTO = 3
    EXCELENTE = 4
    SUPERIOR = 5
    SOSPECHOSO_CONSUMO_ESTEROIDES = 6
    CONSUMO_ESTEROIDES = 7
    IMPOSIBLE = 8

TABLA_FFMI = {
    SexoBiologico.HOMBRE: {
        NivelFFMI.BAJO: (10,18),
        NivelFFMI.MEDIO: (18,20),
        NivelFFMI.ALTO: (20,22),
        NivelFFMI.EXCELENTE: (22,23),
        NivelFFMI.SUPERIOR: (23,26),
        NivelFFMI.SOSPECHOSO_CONSUMO_ESTEROIDES: (26,28),
        NivelFFMI.CONSUMO_ESTEROIDES: (28,30)
    },
    SexoBiologico.MUJER: {
        NivelFFMI.BAJO: (8,15),
        NivelFFMI.MEDIO: (15,17),
        NivelFFMI.ALTO: (17,18),
        NivelFFMI.EXCELENTE: (18,19),
        NivelFFMI.SUPERIOR: (19,21.5),
        NivelFFMI.SOSPECHOSO_CONSUMO_ESTEROIDES: (21.5,25),
        NivelFFMI.CONSUMO_ESTEROIDES: (25,27)
    }
}

def calcula_ffmi(pesaje: Pesaje) -> float:
    ffm = pesaje.peso * (1-(pesaje.porcentaje_grasa/100))
    ffmi = ffm / ((pesaje.altura/100)**2)
    ffmi = round(ffmi,2)
    msg: str = "ffmi = " + str(ffmi)
    logger.debug(msg)
    return ffmi

def get_nivel_ffmi(ffmi: float, sexo: SexoBiologico) -> NivelFFMI:
    niveles: dict[NivelFFMI, tuple[int,int]] = TABLA_FFMI.get(sexo)
    for nivel, umbrales in niveles.items():
        if umbrales[0] <= ffmi < umbrales[1]:
            return nivel
    else:
        return NivelFFMI.IMPOSIBLE

class PersonaNombreError(Exception):
    def __init__(self, nombre: Any) -> None:
        super().__init__("No se puede crear una persona con nombre " + str(nombre))
        logger.warning("Error al crear una persona.")
        self.nombre_erroneo = nombre
        
    def get_tipo(self) -> Any:
        return (type(self.nombre_erroneo))
    
    def print_recomendaciones(self) -> None:
        print("El nombre debe ser un string de al menos 1 caracter de longitud.")
        
class Persona:
    def __init__(self, nombre: str = None, sexo: SexoBiologico = None, fichero: str = None) -> None:
        if not nombre and not sexo and fichero:
            if fichero.endswith(".pickle"):
                self.cargaPickle(fichero)
            elif fichero.endswith(".json"):
                self.cargaJSON(fichero)
            else:
                logger.warning("Intentando cargar una persona desde un fichero con formato desconocido. -> " + fichero)
                raise Exception("Intentando cargar una persona desde un fichero con formato desconocido. -> " + fichero)
        elif nombre and sexo and not fichero:
            if type(nombre) != str or len(nombre) == 0:
                raise PersonaNombreError(nombre)
            self.nombre: str = nombre
            self.sexo: SexoBiologico = sexo
            self.pesajes: list[Pesaje] = []
        else:
            raise Exception("No se puede crear una persona sin ningún dato")
        
    def registra_pesaje(self, pesaje: Pesaje) -> None:
        self.pesajes.append(pesaje)
        
    def calcula_nivel_ffmi_actual(self) -> NivelFFMI | None:
        if len(self.pesajes) == 0:
            logger.info("No hay ningún pesaje registrado para " + self.nombre)
            return None
        else:
            ffmi: float = calcula_ffmi(self.pesajes[-1])
            nivel: NivelFFMI = get_nivel_ffmi(ffmi, self.sexo)
            return nivel
        
    def calcula_nivel_ffmi_medio(self, semanas: int = 4) -> NivelFFMI | None:
        if len(self.pesajes) < semanas:
            logger.info("No hay suficientes pesajes registrados para " + self.nombre)
            return None
        pesajes: list[Pesaje] = self.pesajes[-semanas:]
        ffmis: list[float] = [calcula_ffmi(pesaje) for pesaje in pesajes]
        # ffmis = []
        # for pesaje in pesajes:
        #     ffmis.append(calcula_ffmi(pesaje))
        ffmi_medio: float = sum(ffmis)/len(ffmis)
        nivel: NivelFFMI = get_nivel_ffmi(ffmi_medio, self.sexo)
        return nivel
    
    def guardaPickle(self, nombreFichero: str) -> None:
        with open(nombreFichero, mode='wb') as file:
            pickle.dump(self, file)
    
    def cargaPickle(self, nombreFichero: str) -> None:
        with open(nombreFichero, mode='rb') as file:
            p: Persona = pickle.load(file)
            self.nombre = p.nombre
            self.sexo = p.sexo
            self.pesajes = p.pesajes
    
    def guardaJSON(self, nombreFichero: str) -> None:
        datos: dict[str, Any] = {}
        datos['nombre'] = self.nombre
        datos['sexo'] = self.sexo.name
        lista_pesajes = []
        for pesaje in self.pesajes:
            p: tuple[int, float, float] = (pesaje.altura, pesaje.peso, pesaje.porcentaje_grasa)
            lista_pesajes.append(p)
        datos['pesajes'] = lista_pesajes
        with open(nombreFichero, mode='w', encoding='utf8') as file:
            json.dump(datos, file, indent=3)

    def cargaJSON(self, nombreFichero: str) -> None:
        with open(nombreFichero, mode='r', encoding='utf8') as file:
            datos: dict[str, Any] = json.load(file)
            self.nombre = datos.get("nombre")
            sexo: str = datos.get("sexo")
            for nombre, elemento in SexoBiologico.__members__.items():
                if sexo == nombre:
                    self.sexo = elemento
            if not self.sexo:
                logger.warning("Datos del JSON modificados, incoherencia de datos")
                raise Exception("Datos del JSON modificados, incoherencia de datos")
            lista_pesajes = datos.get("pesajes")
            lista = []
            for pesaje in lista_pesajes:
                p = Pesaje(pesaje[0], pesaje[1], pesaje[2])
                lista.append(p)
            self.pesajes = lista

class ProcesoSupervisionGimnasio:
    def __init__(self, fichero: str = "personas.csv"):
        self.personas: dict[str, Persona] = {}
        with open(fichero, mode='r', encoding='utf8') as file:
            reader: csv.DictReader = csv.DictReader(file, delimiter=',')
            for linea in reader:
                nombre = linea.get("Nombre")
                if nombre not in self.personas:
                    sexo_str: str = linea.get("Sexo")
                    sexo: SexoBiologico = None
                    for name, elemento in SexoBiologico.__members__.items():
                        if sexo_str == name:
                            sexo = elemento
                            break
                    if not sexo:
                        logger.warning("Datos del JSON modificados, incoherencia de datos")
                        raise Exception("Datos del JSON modificados, incoherencia de datos")
                    p = Persona(nombre, sexo)
                    self.personas[nombre] = p
                altura = int(linea.get("Altura"))
                peso = float(linea.get("Peso"))
                grasa = float(linea.get("PorcentajeGrasa"))
                pesaje = Pesaje(altura, peso, grasa)
                persona = self.personas.get(nombre)
                persona.registra_pesaje(pesaje)
                    
    def imprime_listado_personas(self) -> None:
        print("Personas registradas:")
        for persona in self.personas.values():
            print(persona.nombre, "->", persona.sexo.name)

if __name__ == '__main__':
    try:
        p1 = Persona("Ilia Topuria", SexoBiologico.HOMBRE)
        p1.calcula_nivel_ffmi_actual()
        pesaje = Pesaje(170, 65.5, 8)
        p1.registra_pesaje(pesaje)
        print("Nivel pre-combate ->", p1.calcula_nivel_ffmi_actual().name.title())
        pesaje = Pesaje(170, 75.5, 8)
        p1.registra_pesaje(pesaje)    
        print("Nivel pre-combate ->", p1.calcula_nivel_ffmi_actual().name.title())
        p1.guardaPickle("topuria.pickle")
        
        p1 = Persona(fichero="topuria.pickle")
        p1.guardaJSON(nombreFichero="topuria.json")
        
        
        p1 = Persona(fichero="topuria.json")
        print("Nivel actual->", p1.calcula_nivel_ffmi_actual().name.title())
        
        print("Nivel medio 3 semanas ->", p1.calcula_nivel_ffmi_medio(3).name.title())
        
        
        proc = ProcesoSupervisionGimnasio()
        proc.imprime_listado_personas()
    except ValorParametroIncorrectoError as e:
        logger.info("Se está creando algún pesaje con datos incorrectos.")
        logger.info("Datos -> altura: " + str(e.altura) + " - peso: " + str(e.peso) + " - porcentaje_grasa: " + str(e.porcentaje_grasa))
    except PersonaNombreError as e:
        logger.info("Se ha creado una persona con un nombre incorrecto.")
    except:
        logger.info("Ha habido algún error desconocido.")