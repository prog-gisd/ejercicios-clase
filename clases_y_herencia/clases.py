class Persona:
    '''Clase simple para representar una persona'''
    def __init__(self, nombre: str, dni: str):
        self.nombre = nombre
        self.dni = dni
        
    def __del__(self):
        print("Borrando persona -> \n" + self.info())
        self.nombre = None
        self.dni = None
        print("Persona borrada")
        
    def info(self) -> str:
        msg: str = 'Nombre: ' + self.nombre + '\t'
        msg += ' DNI: ' + self.dni
        return msg


class Alumno(Persona):
    '''Clase que representa un Alumno herendando
    de la clase Persona'''
    
    def __init__(self, lista: list, nombre: str,
                 dni: str, edad: int = 18):
        super().__init__(nombre, dni)
        self.edad: int = edad
        self.lista = lista
        self.lista.append(self)
        
    def __del__(self):
        self.lista = None
        self.nombre = None
        self.dni = None
        self.edad = None
        self.lista = None
        
    def cambio_de_nombre(self, nombre: str):
        self.nombre = nombre
        
    def info(self) -> str:
        msg: str = super().info() +'\t'
        msg += ' Edad: ' + str(self.edad)
        return msg
    
    def incrementa_edad(self) -> None:
        self.edad += 1
        
    def alumno_mas_viejo(self, alumno):
        edad_alumno: int = alumno.edad
        mi_edad: int = self.edad
        if mi_edad < edad_alumno:
            return alumno
        else:
            return self

if __name__ == '__main__':
    p = Persona("Adrián", "13564")
    del p
    
    listado_alumnos: list[Alumno] = []
    
    a1 = Alumno(listado_alumnos, "Juan", "20394238", 20)
    a2 = Alumno(dni="234234", nombre="María", lista=listado_alumnos)
    a3 = Alumno(nombre="Ana", dni="234234", lista=listado_alumnos)
    
    print("¿Cuántos alumnos hay?", len(listado_alumnos))
    
    print("Listado de personas:")
    for alumno in listado_alumnos:
        print(alumno.info())

    listado_alumnos.remove(a1)
    del a1

    print("Listado de alumnos:")
    for alumno in listado_alumnos:
        print(alumno.info())

