import unittest
from app import create_app
from app.transaction.entities import Store
from app.context import AppContext
from flask import json


class TestRegisterTransaction(unittest.TestCase):
    def setUp(self):
        app = create_app('config.TestConfig')
        self.client = app.test_client()
        self.context = AppContext()

    def tearDown(self):
        self.context.TransactionRepository.delete_all()
        self.context.StoreRepository.delete_all()


    def _add_sample_store(self):
        store = Store("45283163000167", "Nosso Restaurante de Todo Dia LTDA", "Fabio I.", "11909000300")
        self.context.StoreRepository.add(store)

    def test_unprocessable_if_invalid_store(self):
        headers = {'content-type': 'application/json'}
        result = self.client.post('/v1/transacao/', headers=headers,
                                  data=json.dumps({"estabelecimento": "60.283.163/0001-67",
                                                   "cliente" : "teste", "valor" : 10, "descricao" : "teste"}),
                                  follow_redirects=True)
        self.assertEqual(result.status_code, 422)

    def test_unprocessable_if_invalid_client(self):
        headers = {'content-type': 'application/json'}
        result = self.client.post('/v1/transacao/', headers=headers,
                                  data=json.dumps({"estabelecimento": "45.283.163/0001-67",
                                                   "cliente": "594.214.930-01", "valor": 10.1, "descricao": "teste"}),
                                  follow_redirects=True)

        self.assertEqual(result.status_code, 422)

    def test_ok_if_valid_client(self):
        self._add_sample_store()
        headers = {'content-type': 'application/json'}
        result = self.client.post('/v1/transacao/', headers=headers,
                                  data=json.dumps({"estabelecimento": "45.283.163/0001-67",
                                                   "cliente": "094.214.930-01", "valor": 590.01,
                                                   "descricao": "Almoço em restaurante chique pago via Shipay!"}),
                                  follow_redirects=True)

        self.assertEqual(result.status_code, 200)
