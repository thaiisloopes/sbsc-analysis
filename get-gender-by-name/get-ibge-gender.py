import csv
import gender_guesser.detector as gender

def get_genero_nome(nome: str) -> str:
    """
    Usa a biblioteca gender-guesser para determinar o gênero do primeiro nome.
    Retorna 'Masculino', 'Feminino' ou 'Indefinido'.
    """
    d = gender.Detector(case_sensitive=False)
    resultado = d.get_gender(nome)

    if resultado in ("male", "mostly_male"):
        return "Masculino"
    elif resultado in ("female", "mostly_female"):
        return "Feminino"
    else:
        return "Indefinido"


def processar_csv(arquivo_entrada: str, arquivo_saida: str):
    """
    Lê nomes de um CSV de entrada (coluna 'nome'), usa apenas o primeiro nome
    e grava apenas o gênero em um CSV de saída.
    """
    with open(arquivo_entrada, newline='', encoding='utf-8') as csv_in, \
         open(arquivo_saida, mode='w', newline='', encoding='utf-8') as csv_out:

        leitor = csv.DictReader(csv_in)
        escritor = csv.writer(csv_out)

        # Cabeçalho apenas com a coluna genero
        escritor.writerow(['genero'])

        for linha in leitor:
            nome_completo = linha['nome'].strip()
            primeiro_nome = nome_completo.split()[0]
            genero = get_genero_nome(primeiro_nome)
            escritor.writerow([genero])
            print(f"{nome_completo} -> {primeiro_nome}: {genero}")


if __name__ == "__main__":
    processar_csv("../nomes.csv", "../nomes_genero.csv")
