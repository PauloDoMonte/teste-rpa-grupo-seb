import json
import logging
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
def carregar_vagas(arquivo):
    with open(arquivo, 'r') as f:
        return json.load(f)

def preencher_campo(driver, wait, xpath, valor):
    try:
        campo = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        campo.send_keys(valor)
    except (NoSuchElementException, TimeoutException) as e:
        logging.error(f"Erro ao preencher o campo {xpath}: {str(e)}")
        return False
    return True

def selecionar_efetividade(driver, efetividade):
    try:
        if efetividade in ['sim', 'efetivo']:
            driver.find_element(By.XPATH, '//input[@value="Sim"]').click()
        elif efetividade in ['não', 'banco de talentos', 'estágio', 'aprendiz', 'docente']:
            driver.find_element(By.XPATH, '//input[@value="Não"]').click()
        else:
            logging.warning(f"Efetividade não reconhecida: {efetividade}")
    except NoSuchElementException as e:
        logging.error(f"Erro ao selecionar efetividade: {str(e)}")

def preencher_formulario(vagas, tempo_espera=10):
    driver = webdriver.Chrome()
    driver.get('https://forms.office.com/r/zfipx2RFsY')
    wait = WebDriverWait(driver, tempo_espera)

    inicio = datetime.now()
    logging.info(f"Início do preenchimento: {inicio.strftime('%Y-%m-%d %H:%M:%S')}")

    registros_preenchidos = 0

    try:
        for indice, vaga in enumerate(vagas):
            logging.info(f"Preenchendo vaga {indice + 1}/{len(vagas)}: {vaga['cargo']}")
            if not preencher_campo(driver, wait, '//input[@aria-label="Texto de linha única" and @placeholder="Insira sua resposta"]', vaga['cargo']):
                continue
            if not preencher_campo(driver, wait, '//input[@aria-label="Texto de linha única" and @placeholder="Insira sua resposta"]', vaga['localidade']):
                continue

            efetividade = vaga['efetividade'].lower()
            selecionar_efetividade(driver, efetividade)

            try:
                driver.find_element(By.XPATH, '//button[text()="Enviar"]').click()
                time.sleep(2)
                driver.get('https://forms.office.com/r/zfipx2RFsY')
                registros_preenchidos += 1
            except NoSuchElementException as e:
                logging.error(f"Erro ao enviar o formulário: {str(e)}")

    except WebDriverException as e:
        logging.error(f"Ocorreu um erro: {str(e)}")
        fechamento = datetime.now()
        logging.info(f"Navegador fechado em: {fechamento.strftime('%Y-%m-%d %H:%M:%S')}")
        logging.info(f"Total de registros preenchidos até o momento: {registros_preenchidos}")

    fim = datetime.now()
    logging.info(f"Término do preenchimento: {fim.strftime('%Y-%m-%d %H:%M:%S')}")
    duracao = fim - inicio
    logging.info(f"Duração total: {str(duracao)}")

    logging.info("Formulário preenchido com sucesso.")
    driver.quit()

if __name__ == "__main__":
    vagas = carregar_vagas('vagas.json')
    preencher_formulario(vagas)