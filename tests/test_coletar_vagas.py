import unittest
from unittest.mock import patch, Mock
from src.coletar_vagas import coletar_vagas

class TestColetarVagas(unittest.TestCase):

    @patch('src.coletar_vagas.requests.get')
    def test_coletar_vagas_success(self, mock_get):
        # Simulando uma resposta bem-sucedida da requisição
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '''
        <ul aria-label="Lista de Vagas">
            <li data-testid="job-list__listitem">
                <div class="sc-f5007364-4">Agente Escolar</div>
                <div class="sc-f5007364-5">Maceió - AL</div>
                <div class="sc-f5007364-6">Efetivo</div>
            </li>
            <li data-testid="job-list__listitem">
                <div class="sc-f5007364-4">Agente Escolar</div>
                <div class="sc-f5007364-5">São Paulo - SP</div>
                <div class="sc-f5007364-6">Efetivo</div>
            </li>
            <li data-testid="job-list__listitem">
                <div class="sc-f5007364-4">Analista Administrativo</div>
                <div class="sc-f5007364-5">São Paulo - SP</div>
                <div class="sc-f5007364-6">Efetivo</div>
            </li>
            <li data-testid="job-list__listitem">
                <div class="sc-f5007364-4">Consultor Comercial - Trabalho Presencial (Salvador/BA)</div>
                <div class="sc-f5007364-5">Salvador - BA</div>
                <div class="sc-f5007364-6">Efetivo</div>
            </li>
        </ul>
        '''
        mock_get.return_value = mock_response

        # Chama a função que está sendo testada
        vagas = coletar_vagas()

        # Verifica se as vagas foram coletadas corretamente
        self.assertEqual(len(vagas), 4)
        self.assertEqual(vagas[0]['cargo'], 'Agente Escolar')
        self.assertEqual(vagas[0]['localidade'], 'Maceió - AL')
        self.assertEqual(vagas[0]['efetividade'], 'Efetivo')
        self.assertEqual(vagas[1]['cargo'], 'Agente Escolar')
        self.assertEqual(vagas[1]['localidade'], 'São Paulo - SP')
        self.assertEqual(vagas[1]['efetividade'], 'Efetivo')
        self.assertEqual(vagas[2]['cargo'], 'Analista Administrativo')
        self.assertEqual(vagas[2]['localidade'], 'São Paulo - SP')
        self.assertEqual(vagas[2]['efetividade'], 'Efetivo')
        self.assertEqual(vagas[3]['cargo'], 'Consultor Comercial - Trabalho Presencial (Salvador/BA)')
        self.assertEqual(vagas[3]['localidade'], 'Salvador - BA')
        self.assertEqual(vagas[3]['efetividade'], 'Efetivo')

    @patch('src.coletar_vagas.requests.get')
    def test_coletar_vagas_failure(self, mock_get):
        # Simulando uma resposta de erro da requisição
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        # Chama a função que está sendo testada
        vagas = coletar_vagas()

        # Verifica se a função retorna uma lista vazia em caso de erro
        self.assertEqual(vagas, [])

if __name__ == '__main__':
    unittest.main()