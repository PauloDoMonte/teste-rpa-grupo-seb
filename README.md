# Teste RPA - Grupo SEB

Este repositório contém um projeto de automação de processos robóticos (RPA) desenvolvido como parte do teste técnico para o Grupo SEB. O objetivo deste projeto é demonstrar 
habilidades em automação com python e a utilização de serviços orquestrados por Docker compose.

## Funcionamento

1. **Acesso ao Site de Vagas**:
   - **URL**: [Grupo SEB - Vagas](https://gruposeb.gupy.io/)
   - **Objetivo**: Coletar informações sobre as vagas disponíveis, incluindo:
     - Cargo
     - Localidade
     - Efetividade

2. **Acesso ao Formulário**:
   - **URL**: [Formulário de Inscrição](https://forms.office.com/r/zfipx2RFsY)
   - **Objetivo**: Preencher as informações coletadas e selecionar o flag apropriado.

## Tecnologias usadas:

Este projeto faz uso das seguintes tecnologias:

1. **BeautifulSoup**: Utilizada para extrair dados do site de vagas.
2. **Selenium**: Empregado para automatizar a inserção dos dados no formulário.
3. **Docker**: Orquestração de serviços para garantir um ambiente de execução consistente.
   - **Celery**: Utilizado para agendar a execução das atividades diariamente em horários específicos.
   - **Redis**: Servindo como broker para o Celery, facilitando a comunicação entre tarefas.
   - **Selenium Hub**: Imagem do Selenium que permite a execução de testes em um ambiente Docker.
   - **Chrome**: Imagem do navegador Chrome, controlada pelo Selenium para a automação das interações.

## Instalação

Siga os passos abaixo para instalar e configurar o projeto:

1. Clone o repositório:
   ```bash
   git clone https://github.com/PauloDoMonte/teste-rpa-grupo-seb.git

2. Criar o ambiente virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate

3. Instalar todos os requisitos:
   ```bash
   pip3 install -r requirements.txt

4. Rodar o projeto:
   ```bash
   python3 src/main.py
