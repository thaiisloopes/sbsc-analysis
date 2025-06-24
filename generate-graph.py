import pandas as pd
import networkx as nx
from itertools import combinations
from networkx.algorithms.community.centrality import girvan_newman
from networkx.algorithms.community import louvain_communities
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sbsc_dataset = pd.read_csv("sbsc_dataset.csv")

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

            else:
                category = listaRowsVerdade['category'].unique().item()
                year = listaRowsVerdade['publish-date'].unique().item()
                language = listaRowsVerdade['language'].unique().item()
                G.add_edge(i[0], i[1], category = category, year = year, language = language, weight=1)

    return G

sbsc_graph = createGraph(sbsc_dataset)
sbsc_compGig = sbsc_graph.subgraph(sorted(nx.connected_components(sbsc_graph))[0])

def getGraphDetails():
    print(f"Numero de nos: {sbsc_graph.number_of_nodes()}\n")
    print(f"Numero de arestas: {sbsc_graph.number_of_edges()}\n")
    print(f"Diametro: {nx.diameter(sbsc_compGig)}\n")
    print(f"Densidade: {nx.density(sbsc_graph)}\n")
    print(f"Coeficiente de Agrupamento Médio: {nx.average_clustering(sbsc_graph)}\n")

    number_of_cliques = nx.number_of_cliques(sbsc_graph)
    max_number_of_cliques = max(number_of_cliques)
    print(f"Numero maximo de cliques: {number_of_cliques}\n")
    print(f"No com maior numero de cliques: {max_number_of_cliques}\n")

    node_clique_number = nx.node_clique_number(sbsc_graph)
    max_node_clique_number = max(node_clique_number)
    print(f"Tamanho do maior clique: {node_clique_number}\n")
    print(f"No com maior tamanho de clique: {max_node_clique_number}\n")

    #### DÚVIDA: Qual a diferença entre number_of_cliques e node_clique_number?

def getCentralityMetrics():
    degree_centrality = nx.degree_centrality(sbsc_graph)
    max_degree_centrality = max(degree_centrality, key=degree_centrality.get)
    print(f"Centralidade de Grau: {degree_centrality}\n")
    print(f"No com maior centralidade de grau: {max_degree_centrality}\n")

    betweenness_centrality = nx.betweenness_centrality(sbsc_graph)
    max_betweenness_centrality = max(betweenness_centrality, key=betweenness_centrality.get)
    print(f"Centralidade de Intermediação (Betweenness): {betweenness_centrality}\n")
    print(f"No com maior centralidade de intermediação: {max_betweenness_centrality}\n")

    closeness_centrality = nx.closeness_centrality(sbsc_graph)
    max_closeness_centrality = max(closeness_centrality, key=closeness_centrality.get)
    print(f"Centralidade de Proximidade (Closeness): {closeness_centrality}\n")
    print(f"No com maior centralidade de proximidade: {max_closeness_centrality}\n")

    eigenvector_centrality = nx.eigenvector_centrality(sbsc_graph, tol=1e-03)
    max_eigenvector_centrality = max(eigenvector_centrality, key=eigenvector_centrality.get)
    print(f"Centralidade de Autovetor: {eigenvector_centrality}\n")
    print(f"No com maior centralidade de autovetor: {max_eigenvector_centrality}\n")

def girvanNewmanCommunityDetection():
    sbsc_girvan_newman_communities = girvan_newman(sbsc_graph)

    node_groups = []
    for community in next(sbsc_girvan_newman_communities):
        node_groups.append(list(community))

    print(f"Girvan-Newman communities: {node_groups}\n")

def louvainCommunityDetection():
    sbsc_louvain_communities = nx.algorithms.community.louvain.louvain_communities(sbsc_graph, weight='weight', resolution=0.7)

    for community in range(len(sbsc_louvain_communities)):
        louvain_communities = sbsc_louvain_communities[community]
    for author in louvain_communities:
        sbsc_graph.nodes[author]['group_louvain'] = community

    print("Louvain communities: \n\n")
    for community in sbsc_louvain_communities:
        print(len(community), community)    

def plotCollaborationMatrix():
    degree_list = list(nx.degree(sbsc_graph))
    authors = {}

    for t in degree_list:
        authors[t[0]] = t[1]

    authors_dictionary = dict(sorted(authors.items(), key=lambda item: item[1]))

    important_people = []
    for author in authors_dictionary:
        if authors_dictionary[author] > 13:
            important_people.append(author)

    mtrx = nx.to_pandas_adjacency(sbsc_graph, dtype=int)
    mtrx_sub = mtrx.loc[important_people]
    mtrx_sub = mtrx_sub.loc[:, important_people]

    mask = np.triu(np.ones_like(mtrx_sub, dtype=bool))
    extremes = mtrx_sub.values.max(), mtrx_sub.values.min()

    plt.figure(dpi = 200)
    cmap = sns.color_palette('colorblind', 10)
    p = sns.heatmap(mtrx_sub,
                    cbar=False, yticklabels=True, fmt='', mask=mask, square=True,
                    xticklabels=True, vmin=0, vmax=7, center=3.5, annot=True,
                    annot_kws={'size': 6, 'alpha': 0.75}, linecolor='white', cmap=cmap)
    p.set_xticklabels(p.get_xticklabels(), fontsize=4, rotation=55, horizontalalignment='right', rotation_mode='anchor')
    p.set_yticklabels(p.get_yticklabels(), fontsize=4)
    plt.show()

def exportGraph():
    nx.write_gexf(sbsc_graph, 'sbsc_graph.gexf')

print("===============================================\n")
# getGraphDetails()
print("===============================================\n\n\n\n")
getCentralityMetrics()
print("===============================================\n\n\n\n")
# girvanNewmanCommunityDetection()
# louvainCommunityDetection()
print("===============================================\n\n\n\n")
# plotCollaborationMatrix()
print("===============================================\n\n\n\n")
# exportGraph()
