import unittest
from unittest.mock import patch, MagicMock
import json
from src.preencher_formulario import carregar_vagas, preencher_campo, selecionar_efetividade, preencher_formulario 

class TestFormPreenchimento(unittest.TestCase):

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data='[{"cargo": "Desenvolvedor", "localidade": "São Paulo", "efetividade": "sim"}]')
    def test_carregar_vagas(self, mock_file):
        vagas = carregar_vagas('vagas.json')
        self.assertEqual(len(vagas), 1)
        self.assertEqual(vagas[0]['cargo'], 'Desenvolvedor')

    @patch('selenium.webdriver.Chrome')
    @patch('selenium.webdriver.support.ui.WebDriverWait')
    def test_preencher_campo(self, mock_wait, mock_driver):
        mock_wait.return_value.until.return_value = MagicMock()
        driver = mock_driver.return_value
        wait = mock_wait.return_value

        resultado = preencher_campo(driver, wait, '//input[@placeholder="Insira sua resposta"]', 'Teste')
        self.assertTrue(resultado)

        # Testando o caso de erro
        wait.until.side_effect = TimeoutException
        resultado = preencher_campo(driver, wait, '//input[@placeholder="Insira sua resposta"]', 'Teste')
        self.assertFalse(resultado)

    @patch('selenium.webdriver.Chrome')
    def test_selecionar_efetividade(self, mock_driver):
        driver = mock_driver.return_value

        # Testando seleção de efetividade "sim"
        selecionar_efetividade(driver, 'sim')
        driver.find_element.assert_called_once_with(By.XPATH, '//input[@value="Sim"]')

        # Testando seleção de efetividade "não"
        driver.reset_mock()  # Reseta as chamadas anteriores
        selecionar_efetividade(driver, 'não')
        driver.find_element.assert_called_once_with(By.XPATH, '//input[@value="Não"]')

        # Testando efetividade não reconhecida
        with self.assertLogs('seu_modulo', level='WARNING') as log:
            selecionar_efetividade(driver, 'desconhecido')
            self.assertIn('Efetividade não reconhecida: desconhecido', log.output[0])

    @patch('selenium.webdriver.Chrome')
    @patch('selenium.webdriver.support.ui.WebDriverWait')
    @patch('time.sleep', return_value=None)  # Para evitar esperar durante os testes
    def test_preencher_formulario(self, mock_sleep, mock_wait, mock_driver):
        driver = mock_driver.return_value
        wait = mock_wait.return_value
        wait.until.return_value = MagicMock()

        vagas = [{'cargo': 'Desenvolvedor', 'localidade': 'São Paulo', 'efetividade': 'sim'}]
        preencher_formulario(vagas)

        # Verifica se o formulário foi preenchido corretamente
        self.assertEqual(driver.get.call_count, 2)  # Deve chamar get duas vezes
        self.assertEqual(driver.find_element.call_count, 3)  # Deve tentar preencher 3 campos

if __name__ == '__main__':
    unittest.main()