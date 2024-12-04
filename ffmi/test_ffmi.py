import unittest

from ffmi import *

class FFMITestCase(unittest.TestCase):
    def test_calcula_ffmi(self):
        p = Pesaje(180, 85, 12.5)
        ffmi = calcula_ffmi(p)
        assert ffmi == 22.96
        
        p = Pesaje(188, 78, 24)
        ffmi = calcula_ffmi(p)
        assert ffmi == 16.77
        
        p = Pesaje(178, 83, 11)
        ffmi = calcula_ffmi(p)
        assert ffmi == 23.31
        
    def test_get_nivel_ffmi(self):
        nivel = get_nivel_ffmi(22, SexoBiologico.MUJER)
        assert nivel == NivelFFMI.SOSPECHOSO_CONSUMO_ESTEROIDES
        
        nivel = get_nivel_ffmi(35, SexoBiologico.MUJER)
        assert nivel == NivelFFMI.IMPOSIBLE
        
        nivel = get_nivel_ffmi(5, SexoBiologico.MUJER)
        assert nivel == NivelFFMI.IMPOSIBLE
        
        nivel = get_nivel_ffmi(35, SexoBiologico.HOMBRE)
        assert nivel == NivelFFMI.IMPOSIBLE
        
        nivel = get_nivel_ffmi(25, SexoBiologico.HOMBRE)
        assert nivel == NivelFFMI.SUPERIOR
        
    def test_get_nivel_ffmi_limites(self):
        nivel = get_nivel_ffmi(18, SexoBiologico.HOMBRE)
        assert nivel == NivelFFMI.MEDIO
        
        nivel = get_nivel_ffmi(10, SexoBiologico.HOMBRE)
        assert nivel == NivelFFMI.BAJO
        
        nivel = get_nivel_ffmi(9.9, SexoBiologico.HOMBRE)
        assert nivel == NivelFFMI.IMPOSIBLE
        
        nivel = get_nivel_ffmi(30, SexoBiologico.HOMBRE)
        assert nivel == NivelFFMI.IMPOSIBLE
        
        nivel = get_nivel_ffmi(27, SexoBiologico.MUJER)
        assert nivel == NivelFFMI.IMPOSIBLE
        
        nivel = get_nivel_ffmi(15, SexoBiologico.MUJER)
        assert nivel == NivelFFMI.MEDIO
        
        nivel = get_nivel_ffmi(8, SexoBiologico.MUJER)
        assert nivel == NivelFFMI.BAJO
        
        nivel = get_nivel_ffmi(7.9, SexoBiologico.MUJER)
        assert nivel == NivelFFMI.IMPOSIBLE
        
    def test_persona_constructor(self):
        
        try:
            p = Persona("Juan", sexo=SexoBiologico.HOMBRE)
            assert p.nombre == "Juan"
            assert p.sexo == SexoBiologico.HOMBRE
            assert p.pesajes == []
            assert len(p.pesajes) == 0
        except PersonaNombreError as e:
            assert e is None
            
        try:
            p = Persona("Jacinta", sexo=SexoBiologico.MUJER)
            assert p.nombre == "Jacinta"
            assert p.sexo == SexoBiologico.MUJER
            assert p.pesajes == []
            assert len(p.pesajes) == 0
        except PersonaNombreError as e:
            assert e is None
        
    def test_persona_constructor_excepciones(self):
        try:
            p = Persona(None, sexo=SexoBiologico.HOMBRE)
        except PersonaNombreError as e:
            assert e is not None
            assert e.get_tipo() == type(None)
            assert e.nombre_erroneo == None
            
        try:
            p = Persona('', sexo=SexoBiologico.HOMBRE)
        except PersonaNombreError as e:
            assert e is not None
            assert e.get_tipo() == str
            assert e.nombre_erroneo == ''
            assert len(e.nombre_erroneo) == 0
            
        try:
            p = Persona(True, sexo=SexoBiologico.HOMBRE)
        except PersonaNombreError as e:
            assert e is not None
            assert e.get_tipo() == bool
            assert e.nombre_erroneo == True
            
    def test_pesaje_error(self):
        try:
            p = Pesaje(-1, 50, 20)
            assert p == None
        except ValorParametroIncorrectoError as e:
            assert e is not None
            assert e != None
            assert e.altura == -1
            assert e.peso == 50
            assert e.porcentaje_grasa == 20
            
        
        try:
            p = Pesaje(170, -50, 20)
            assert p == None
        except ValorParametroIncorrectoError as e:
            assert e is not None
            assert e != None
            assert e.altura == 170
            assert e.peso == -50
            assert e.porcentaje_grasa == 20
            
        
        try:
            p = Pesaje(170, 50, -20)
            assert p == None
        except ValorParametroIncorrectoError as e:
            assert e is not None
            assert e != None
            assert e.altura == 170
            assert e.peso == 50
            assert e.porcentaje_grasa == -20
        
        try:
            p = Pesaje(170, 50, 120)
            assert p == None
        except ValorParametroIncorrectoError as e:
            assert e is not None
            assert e != None
            assert e.altura == 170
            assert e.peso == 50
            assert e.porcentaje_grasa == 120
    
    def test_pesaje_error_limites(self):
        try:
            p = Pesaje(0, 50, 20)
            assert p == None
        except ValorParametroIncorrectoError as e:
            assert e is not None
            assert e != None
            assert e.altura == 0
            assert e.peso == 50
            assert e.porcentaje_grasa == 20
            
        
        try:
            p = Pesaje(170, 0, 20)
            assert p == None
        except ValorParametroIncorrectoError as e:
            assert e is not None
            assert e != None
            assert e.altura == 170
            assert e.peso == 0
            assert e.porcentaje_grasa == 20
            
        
        try:
            p = Pesaje(170, 50, 0)
            assert p == None
        except ValorParametroIncorrectoError as e:
            assert e is not None
            assert e != None
            assert e.altura == 170
            assert e.peso == 50
            assert e.porcentaje_grasa == 0
        
        try:
            p = Pesaje(170, 50, 100)
            assert p == None
        except ValorParametroIncorrectoError as e:
            assert e is not None
            assert e != None
            assert e.altura == 170
            assert e.peso == 50
            assert e.porcentaje_grasa == 100
    
if __name__ == '__main__':
    unittest.main()