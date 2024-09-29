from src.coletar_vagas import coletar_vagas
import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
import os

class TestVagaColetor(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data='[]')
    def test_carregar_cache(self, mock_file):
        coletor = VagaColetor(cache_file='vagas_cache.json')
        self.assertEqual(coletor.vagas_cache, [])

    @patch('builtins.open', new_callable=mock_open)
    def test_salvar_cache(self, mock_file):
        coletor = VagaColetor()
        coletor.vagas_cache = [{'cargo': 'Desenvolvedor', 'localidade': 'São Paulo', 'efetividade': 'CLT'}]
        coletor.salvar_cache()
        mock_file().write.assert_called_once_with(json.dumps(coletor.vagas_cache))

    @patch('requests.get')
    @patch('time.sleep', return_value=None)  # Para evitar esperar durante os testes
    def test_coletar_vagas(self, mock_sleep, mock_get):
        mock_get.return_value = MagicMock(status_code=200, text='<ul aria-label="Lista de Vagas"><li data-testid="job-list__listitem"><div class="sc-f5007364-4">Desenvolvedor</div><div class="sc-f5007364-5">São Paulo</div><div class="sc-f5007364-6">CLT</div></li></ul>')
        
        coletor = VagaColetor()
        vagas = coletor.coletar_vagas()
        
        self.assertEqual(len(vagas), 1)
        self.assertEqual(vagas[0]['cargo'], 'Desenvolvedor')
        self.assertEqual(vagas[0]['localidade'], 'São Paulo')
        self.assertEqual(vagas[0]['efetividade'], 'CLT')

    def test_validar_vaga(self):
        coletor = VagaColetor()
        vaga_valida = {'cargo': 'Desenvolvedor', 'localidade': 'São Paulo', 'efetividade': 'CLT'}
        vaga_invalida = {'cargo': 'Desenvolvedor', 'localidade': 'São Paulo'}
        
        self.assertTrue(coletor.validar_vaga(vaga_valida))
        self.assertFalse(coletor.validar_vaga(vaga_invalida))

    def test_filtrar_vagas(self):
        coletor = VagaColetor()
        coletor.vagas_cache = [
            {'cargo': 'Desenvolvedor', 'localidade': 'São Paulo', 'efetividade': 'CLT'},
            {'cargo': 'Analista', 'localidade': 'Rio de Janeiro', 'efetividade': 'PJ'},
            {'cargo': 'Desenvolvedor', 'localidade': 'São Paulo', 'efetividade': 'PJ'}
        ]
        
        vagas_filtradas = coletor.filtrar_vagas(localidade='São Paulo')
        self.assertEqual(len(vagas_filtradas), 2)

        vagas_filtradas = coletor.filtrar_vagas(efetividade='PJ')
        self.assertEqual(len(vagas_filtradas), 1)

if __name__ == '__main__':
    unittest.main()