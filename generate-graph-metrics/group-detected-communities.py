import pandas as pd

df = pd.read_csv('nodes_with_communities.csv')

comunidades = df.groupby('modularity_class')['Label'].apply(list)
# comunidades = df.groupby('0')['Label'].apply(list)

comunidades_ordenadas = comunidades.sort_values(key=lambda x: x.str.len(), ascending=False)

for classe, membros in comunidades_ordenadas.items():
    print(f"Comunidade {classe} ({len(membros)} membros)")