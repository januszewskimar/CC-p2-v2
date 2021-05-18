from api import app
import unittest

class TestPrediccionesV2(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_prediccion24(self):
        respuesta = self.app.get('/servicio/v2/prediccion/24horas/')
        self.assertEqual(respuesta.status_code, 200)
        
    def test_prediccion48(self):
        respuesta = self.app.get('/servicio/v2/prediccion/48horas/')
        self.assertEqual(respuesta.status_code, 200)
        
    def test_prediccion72(self):
        respuesta = self.app.get('/servicio/v2/prediccion/72horas/')
        self.assertEqual(respuesta.status_code, 200)
        
if __name__ == '__main__':
    unittest.main()
