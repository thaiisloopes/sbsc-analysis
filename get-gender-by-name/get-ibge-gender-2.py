import csv
from collections import defaultdict

def carregar_base_ibge(arquivo_ibge: str) -> dict:
    """
    Carrega a base do IBGE e retorna um dicionário nome -> genero mais frequente.
    """
    nomes_dict = defaultdict(lambda: {"M": 0, "F": 0})

    with open(arquivo_ibge, newline='', encoding="utf-8") as csvfile:
        leitor = csv.DictReader(csvfile, delimiter=";")
        for linha in leitor:
            nome = linha["NOME"].strip().capitalize()
            sexo = linha["SEXO"].strip()
            freq = int(linha["FREQ"])
            nomes_dict[nome][sexo] += freq

    # define gênero predominante
    resultado = {}
    for nome, contagem in nomes_dict.items():
        if contagem["M"] > contagem["F"]:
            resultado[nome] = "Masculino"
        elif contagem["F"] > contagem["M"]:
            resultado[nome] = "Feminino"
        else:
            resultado[nome] = "Indefinido"

    return resultado


def processar_csv(arquivo_entrada: str, arquivo_saida: str, base_ibge: dict):
    """
    Lê nomes do arquivo de entrada, consulta gênero na base IBGE
    e grava no arquivo de saída (nome, genero).
    """
    with open(arquivo_entrada, newline='', encoding="utf-8") as csv_in, \
         open(arquivo_saida, mode="w", newline='', encoding="utf-8") as csv_out:

        leitor = csv.DictReader(csv_in)
        campos_saida = ["nome", "genero"]
        escritor = csv.DictWriter(csv_out, fieldnames=campos_saida)
        escritor.writeheader()

        for linha in leitor:
            nome_completo = linha["nome"].strip()
            primeiro_nome = nome_completo.split()[0].capitalize()
            genero = base_ibge.get(primeiro_nome, "Indefinido")
            escritor.writerow({"nome": nome_completo, "genero": genero})
            print(f"{nome_completo} -> {primeiro_nome}: {genero}")


if __name__ == "__main__":
    # Substitua pelo nome real do CSV baixado do IBGE
    base_ibge = carregar_base_ibge("ibge-nomes.csv")
    processar_csv("nomes.csv", "nomes_genero.csv", base_ibge)
