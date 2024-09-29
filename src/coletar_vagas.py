import requests
from bs4 import BeautifulSoup
import logging
import time
import json
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VagaColetor:
    def __init__(self, url_vagas='https://gruposeb.gupy.io/', tentativas=3, cache_file='vagas_cache.json'):
        self.url_vagas = url_vagas
        self.tentativas = tentativas
        self.cache_file = cache_file
        self.vagas_cache = self.carregar_cache()

    def carregar_cache(self):
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        return []

    def salvar_cache(self):
        with open(self.cache_file, 'w') as f:
            json.dump(self.vagas_cache, f)

    def coletar_vagas(self):
        for tentativa in range(self.tentativas):
            try:
                logger.info("Tentativa %d de acessar %s", tentativa + 1, self.url_vagas)
                response = requests.get(self.url_vagas)
                response.raise_for_status()
                break
            except requests.RequestException as e:
                logger.error("Erro ao acessar o site de vagas: %s", e)
                if tentativa < self.tentativas - 1:
                    logger.info("Tentando novamente em 5 segundos...")
                    time.sleep(5)
                else:
                    logger.error("Todas as tentativas falharam.")
                    return []

        soup = BeautifulSoup(response.text, 'html.parser')
        vagas = []

        for vaga in soup.select('ul[aria-label="Lista de Vagas"] li[data-testid="job-list__listitem"]'):
            cargo = vaga.select_one('div.sc-f5007364-4').get_text(strip=True)
            localidade = vaga.select_one('div.sc-f5007364-5').get_text(strip=True)
            efetividade = vaga.select_one('div.sc-f5007364-6').get_text(strip=True)

            vaga_dados = {
                'cargo': cargo,
                'localidade': localidade,
                'efetividade': efetividade
            }

            if self.validar_vaga(vaga_dados):
                vagas.append(vaga_dados)
            else:
                logger.warning("Vaga inválida encontrada e ignorada: %s", vaga_dados)

        self.vagas_cache.extend(vagas)
        self.salvar_cache()
        logger.info("Vagas coletadas: %s", len(vagas))
        return vagas

    def validar_vaga(self, vaga):
        return all(key in vaga for key in ['cargo', 'localidade', 'efetividade'])

    def filtrar_vagas(self, localidade=None, efetividade=None):
        vagas_filtradas = self.vagas_cache
        if localidade:
            vagas_filtradas = [vaga for vaga in vagas_filtradas if vaga['localidade'] == localidade]
        if efetividade:
            vagas_filtradas = [vaga for vaga in vagas_filtradas if vaga['efetividade'] == efetividade]
        return vagas_filtradas

if __name__ == "__main__":
    coletor = VagaColetor()
    vagas = coletor.coletar_vagas()

    if vagas:
        logger.info("Total de vagas coletadas: %d", len(vagas))
        # Exemplo de filtragem
        vagas_filtradas = coletor.filtrar_vagas(localidade='São Paulo - SP')
        logger.info("Total de vagas filtradas para São Paulo: %d", len(vagas_filtradas))
    else:
        logger.info("Nenhuma vaga coletada.")