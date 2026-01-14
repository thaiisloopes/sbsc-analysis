import pandas as pd

# Caminho do arquivo Excel
arquivo_excel = "../sbsc_dataset.xlsx"

# Ler todas as abas do arquivo
abas = pd.read_excel(arquivo_excel, sheet_name=None)

# Concatenar os DataFrames de todas as abas
df_consolidado = pd.concat(abas.values(), ignore_index=True)

# Exportar para CSV
df_consolidado.to_csv("../sbsc_dataset.csv", index=False, encoding="utf-8-sig")

print("Arquivo CSV consolidado gerado com sucesso!")
