from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def preencher_formulario(vagas):
    driver = webdriver.Chrome()
    driver.get('https://forms.office.com/r/zfipx2RFsY')
    time.sleep(5)

    for vaga in vagas:
        input_cargo = driver.find_element(By.XPATH, '//input[@aria-label="Texto de linha única" and @placeholder="Insira sua resposta"]')
        input_cargo.send_keys(vaga['cargo'])

        input_cidade = driver.find_elements(By.XPATH, '//input[@aria-label="Texto de linha única" and @placeholder="Insira sua resposta"]')[1]
        input_cidade.send_keys(vaga['localidade'])

        efetividade = vaga['efetividade'].lower()
        if efetividade in ['sim', 'efetivo']:
            driver.find_element(By.XPATH, '//input[@value="Sim"]').click()
        elif efetividade in ['não', 'banco de talentos', 'estágio', 'aprendiz', 'docente']:
            driver.find_element(By.XPATH, '//input[@value="Não"]').click()
        else:
            print(f"Efetividade não reconhecida: {vaga['efetividade']}")

        driver.find_element(By.XPATH, '//button[text()="Enviar"]').click()
        time.sleep(2)
        driver.get('https://forms.office.com/r/zfipx2RFsY')
        time.sleep(5)

    print("Formulário preenchido com sucesso.")
    driver.quit()