from coletar_vagas import coletar_vagas
from preencher_formulario import preencher_formulario

def main():
    vagas = coletar_vagas()
    if vagas:
        preencher_formulario(vagas)

if __name__ == "__main__":
    main()