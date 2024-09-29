import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def coletar_vagas():
    url_vagas = 'https://gruposeb.gupy.io/'
    try:
        response = requests.get(url_vagas)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error("Erro ao acessar o site de vagas: %s", e)
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    vagas = []

    for vaga in soup.select('ul[aria-label="Lista de Vagas"] li[data-testid="job-list__listitem"]'):
        cargo = vaga.select_one('div.sc-f5007364-4').get_text(strip=True)
        localidade = vaga.select_one('div.sc-f5007364-5').get_text(strip=True)
        efetividade = vaga.select_one('div.sc-f5007364-6').get_text(strip=True)

        vagas.append({
            'cargo': cargo,
            'localidade': localidade,
            'efetividade': efetividade
        })

    logger.info("Vagas coletadas: %s", vagas)
    return vagas