import pandas as pd
import unidecode

preposicoes = {"de", "da", "do", "das", "dos"}

def formatar_nome(nome):
    nome = unidecode.unidecode(str(nome).strip().lower())
    
    partes = [parte for parte in nome.split() if parte not in preposicoes]

    if len(partes) <= 2:
        return " ".join(partes)

    primeiro = partes[0]
    ultimo = partes[-1]
    meios = " ".join([f"{p[0]}." for p in partes[1:-1]])

    return f"{primeiro} {meios} {ultimo}"

df = pd.read_csv("nomes.csv")

df["nome"] = df["nome"].apply(formatar_nome)

df.to_csv("nomes_formatados.csv", index=False)

print("Nomes formatados salvos em nomes_formatados.csv")
