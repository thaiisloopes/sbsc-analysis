import pandas as pd
import networkx as nx
from itertools import combinations
from networkx.algorithms.community.centrality import girvan_newman
from networkx.algorithms.community import louvain_communities
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.cluster import SpectralClustering
from sklearn.datasets import make_blobs
from collections import defaultdict

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


def degreeCentrality():
    degree_centrality = nx.degree_centrality(sbsc_graph)
    max_degree_centrality = max(degree_centrality, key=degree_centrality.get)
    print(f"No com maior centralidade de grau: {max_degree_centrality}\n")
    print(f"Centralidade de Grau: {degree_centrality}\n")
    
def betweennessCentrality():
    betweenness_centrality = nx.betweenness_centrality(sbsc_graph)
    max_betweenness_centrality = max(betweenness_centrality, key=betweenness_centrality.get)
    print(f"Centralidade de Intermediação (Betweenness): {betweenness_centrality}\n")
    print(f"No com maior centralidade de intermediação: {max_betweenness_centrality}\n")

def closenessCentrality():
    closeness_centrality = nx.closeness_centrality(sbsc_graph)
    max_closeness_centrality = max(closeness_centrality, key=closeness_centrality.get)
    print(f"Centralidade de Proximidade (Closeness): {closeness_centrality}\n")
    print(f"No com maior centralidade de proximidade: {max_closeness_centrality}\n")

def eigenvectorCentrality():
    eigenvector_centrality = nx.eigenvector_centrality(sbsc_graph, tol=1e-03)
    max_eigenvector_centrality = max(eigenvector_centrality, key=eigenvector_centrality.get)
    print(f"Centralidade de Autovetor: {eigenvector_centrality}\n")
    print(f"No com maior centralidade de autovetor: {max_eigenvector_centrality}\n")


def top10_degree_centrality(G):
    degree = nx.degree_centrality(sbsc_graph)

    top10 = sorted(
        degree.items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]

    for i, (author, value) in enumerate(top10, 1):
        print(f"{i}. {author}: {value:.4f}")

def top10_betweenness_centrality(G):
    betweenness = nx.betweenness_centrality(sbsc_graph)

    top10 = sorted(
        betweenness.items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]

    for i, (author, value) in enumerate(top10, 1):
        print(f"{i}. {author}: {value:.4f}")

def top10_closeness_centrality(G):
    closeness = nx.closeness_centrality(G)

    top10 = sorted(
        closeness.items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]

    for i, (author, value) in enumerate(top10, 1):
        print(f"{i}. {author}: {value:.4f}")

def top10_eigenvector_centrality(G):
    eigenvector = nx.eigenvector_centrality(G, max_iter=1000, tol=1e-06)

    top10 = sorted(
        eigenvector.items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]

    for i, (author, value) in enumerate(top10, 1):
        print(f"{i}. {author}: {value:.4f}")

def exportGraph():
    nx.write_gexf(sbsc_graph, 'sbsc_graph.gexf')

print("===============================================\n")
print("CENTRALITY METRICS FOR SBSC GRAPH")
print("===============================================\n")
# degreeCentrality()
# betweennessCentrality()
# closenessCentrality()
# eigenvectorCentrality()

print("===============================================\n")
print("TOP 10 DEGREE CENTRALITY FOR SBSC GRAPH")
print("===============================================\n")
top10_degree_centrality(sbsc_graph)

print("===============================================\n")
print("TOP 10 BETWEENNESS CENTRALITY FOR SBSC GRAPH")
print("===============================================\n")
top10_betweenness_centrality(sbsc_graph)

print("===============================================\n")
print("TOP 10 CLOSENESS CENTRALITY FOR SBSC GRAPH")
print("===============================================\n")
top10_closeness_centrality(sbsc_graph)

print("===============================================\n")
print("TOP 10 EIGENVECTOR CENTRALITY FOR SBSC GRAPH")
print("===============================================\n")
top10_eigenvector_centrality(sbsc_graph)

exportGraph()
