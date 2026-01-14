import pandas as pd
import networkx as nx
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
sbsc_compGig = sbsc_graph.subgraph(sorted(nx.connected_components(sbsc_graph))[0])

def getGraphDetails():
    print(f"Numero de nos: {sbsc_graph.number_of_nodes()}\n")
    print(f"Numero de arestas: {sbsc_graph.number_of_edges()}\n")
    print(f"Diametro: {nx.diameter(sbsc_compGig)}\n")
    print(f"Densidade: {nx.density(sbsc_graph)}\n")
    print(f"Coeficiente de Agrupamento Médio: {nx.average_clustering(sbsc_graph)}\n")

def count_nodes_edges_by_year(G, year_attr='year'):
    """
    Imprime o número de nós e arestas por ano,
    considerando apenas nós conectados por arestas naquele ano.
    """

    years = sorted({
        data[year_attr]
        for _, _, data in G.edges(data=True)
        if year_attr in data
    })

    for year in years:
        edges_year = [
            (u, v) for u, v, data in G.edges(data=True)
            if data.get(year_attr) == year
        ]

        num_edges = len(edges_year)

        nodes_year = set()
        for u, v in edges_year:
            nodes_year.add(u)
            nodes_year.add(v)

        num_nodes = len(nodes_year)

        print(f"Ano {year}: {num_nodes} nós, {num_edges} arestas")

print("===============================================")
print("MÉTRICAS GERAIS DO GRAFO COMPLETO\n")
getGraphDetails()
print("===============================================\n\n")
print("NÚMERO DE NÓS E ARESTAS DO GRAFO COMPLETO - POR ANO\n")
count_nodes_edges_by_year(sbsc_graph)
print("==============================================")
