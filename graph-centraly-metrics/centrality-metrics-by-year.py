import networkx as nx
import pandas as pd
from itertools import combinations

sbsc_dataset = pd.read_csv("sbsc_dataset_normalized.csv")

def createGraph(datasetInput):
    G = nx.Graph()

    for artigo in pd.unique(datasetInput['title']):
        listaRowsVerdade = datasetInput[datasetInput['title'] == artigo]
        nomesAutores = list(set(listaRowsVerdade['author']))
        listCombinations = list(combinations(nomesAutores, 2))

        for i in listCombinations:
            if G.has_edge(i[0], i[1]):
                source_id = i[0]
                target_id = i[1]
                G.edges[source_id, target_id]['weight'] += 1
                G.nodes[source_id]['affiliation'] = datasetInput.loc[datasetInput['author'] == source_id]['affiliation'].to_list()[0]
                G.nodes[target_id]['affiliation'] = datasetInput.loc[datasetInput['author'] == target_id]['affiliation'].to_list()[0]

            else:
                source_id = i[0]
                target_id = i[1]
                category = listaRowsVerdade['category'].unique().item()
                year = listaRowsVerdade['publish-date'].unique().item()
                language = listaRowsVerdade['language'].unique().item()
                G.add_edge(i[0], i[1], category = category, year = year, language = language, weight=1)
                G.nodes[source_id]['affiliation'] = datasetInput.loc[datasetInput['author'] == source_id]['affiliation'].to_list()[0]
                G.nodes[target_id]['affiliation'] = datasetInput.loc[datasetInput['author'] == target_id]['affiliation'].to_list()[0]

    return G

sbsc_graph = createGraph(sbsc_dataset)


# --------------------------------------------------
# Descobre todos os anos existentes no grafo
# --------------------------------------------------
years = sorted(
    {data["year"] for _, _, data in sbsc_graph.edges(data=True) if "year" in data}
)


# --------------------------------------------------
# Cria subgrafo contendo apenas arestas de um ano
# --------------------------------------------------
def subgraph_by_year(G, year):
    edges = [
        (u, v)
        for u, v, d in G.edges(data=True)
        if d.get("year") == year
    ]
    return G.edge_subgraph(edges).copy()


# --------------------------------------------------
# Retorna Top-k de uma centralidade
# --------------------------------------------------
def top_k(centrality_dict, k=3, reverse=True):
    return sorted(
        centrality_dict.items(),
        key=lambda x: x[1],
        reverse=reverse
    )[:k]


# --------------------------------------------------
# Calcula centralidades por ano
# --------------------------------------------------
results = {}

for year in years:
    Gy = subgraph_by_year(sbsc_graph, year)

    # # ignora grafos muito pequenos
    # if Gy.number_of_nodes() < 3:
    #     continue

    # # garante conectividade (boa prática)
    # if not nx.is_connected(Gy):
    #     giant = max(nx.connected_components(Gy), key=len)
    #     Gy = Gy.subgraph(giant).copy()

    centralities = {
        "degree": nx.degree_centrality(Gy),
        "betweenness": nx.betweenness_centrality(Gy),
        "closeness": nx.closeness_centrality(Gy),
        "eigenvector": nx.eigenvector_centrality(Gy, max_iter=1000)
    }

    results[year] = {
        "degree": top_k(centralities["degree"], k=3, reverse=True),
        "betweenness": top_k(centralities["betweenness"], k=3, reverse=True),
        "closeness": top_k(centralities["closeness"], k=3, reverse=False),
        "eigenvector": top_k(centralities["eigenvector"], k=3, reverse=True),
    }


# --------------------------------------------------
# Impressão dos resultados
# --------------------------------------------------
for year, metrics in results.items():
    print(f"\nAno {year}")
    for metric, ranking in metrics.items():
        print(f"  {metric}:")
        for i, (node, value) in enumerate(ranking, 1):
            print(f"    {i}. {node} ({value:.4f})")

