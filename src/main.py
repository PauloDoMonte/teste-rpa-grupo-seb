import logging
from coletar_vagas import VagaColetor
from preencher_formulario import preencher_formulario

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
def validar_vagas(vagas):
    validas = []
    invalidas = []
    for vaga in vagas:
        if 'cargo' in vaga and 'localidade' in vaga and 'efetividade' in vaga:
            validas.append(vaga)
        else:
            invalidas.append(vaga)
            logging.warning(f"Vaga inválida encontrada: {vaga}")
    return validas, invalidas

def main():
    try:
        coletor = VagaColetor()  # Instanciando a classe VagaColetor
        vagas = coletor.coletar_vagas()  # Chamando o método coletar_vagas

        if vagas:
            validas, invalidas = validar_vagas(vagas)
            if validas:
                logging.info(f"Total de vagas válidas: {len(validas)}")
                preencher_formulario(validas)
            else:
                logging.info("Nenhuma vaga válida encontrada para preencher.")
            if invalidas:
                logging.info(f"Total de vagas inválidas: {len(invalidas)}")
        else:
            logging.info("Nenhuma vaga coletada.")
    except Exception as e:
        logging.error(f"Ocorreu um erro: {str(e)}")

if __name__ == "__main__":
    main()
