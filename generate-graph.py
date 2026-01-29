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

def top10_closeness_centrality(G):
    closeness = nx.closeness_centrality(G)

    top10 = sorted(
        closeness.items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]

    for i, (author, value) in enumerate(top10, 1):
        print(f"{i}. {author}: {value:.4f}")

def closeness_centrality_like_gephi(G):
    closeness = {}

    for component in nx.connected_components(G):
        # Subgrafo do componente
        G_sub = G.subgraph(component)

        # Closeness normalizada dentro do componente
        sub_closeness = nx.closeness_centrality(G_sub)

        # Armazenar resultados
        closeness.update(sub_closeness)

    return closeness

def top10_closeness_like_gephi(G):
    closeness = closeness_centrality_like_gephi(G)

    top10 = sorted(
        closeness.items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]

    for i, (author, value) in enumerate(top10, 1):
        print(f"{i}. {author}: {value:.4f}")

def girvanNewmanCommunityDetection():
    sbsc_girvan_newman_communities = girvan_newman(sbsc_graph)

    node_groups = []
    for community in next(sbsc_girvan_newman_communities):
        node_groups.append(list(community))

    print(f"Girvan-Newman communities: {node_groups}\n")

def louvainCommunityDetection():
    sbsc_louvain_communities = nx.algorithms.community.louvain.louvain_communities(sbsc_graph, weight='weight', resolution=1.0)

    for community in range(len(sbsc_louvain_communities)):
        louvain_communities = sbsc_louvain_communities[community]
    for author in louvain_communities:
        sbsc_graph.nodes[author]['group_louvain'] = community

    print("Louvain communities: \n\n")
    print(f"Quantidade de comunidades: {len(sbsc_louvain_communities)}\n")
    for community in sbsc_louvain_communities:
        print(len(community), community)    

def louvain_communities_and_its_authors():
    # 1. Detecta comunidades com Louvain
    sbsc_louvain_communities = nx.algorithms.community.louvain.louvain_communities(
        sbsc_graph,
        weight='weight',
        resolution=1.0
    )

    # 2. Ordena as comunidades por tamanho (ordem decrescente)
    sbsc_louvain_communities = sorted(
        sbsc_louvain_communities,
        key=len,
        reverse=True
    )

    # 3. Estrutura para armazenar comunidades e seus autores
    louvain_communities_dict = {}

    # 4. Atribui rótulos e mantém os nós por comunidade
    for community_id, community in enumerate(sbsc_louvain_communities):
        louvain_communities_dict[community_id] = list(community)

        for author in community:
            sbsc_graph.nodes[author]['group_louvain'] = community_id

    # 5. Relatório
    print("Louvain communities (ordenadas por tamanho):\n")
    print(f"Quantidade de comunidades: {len(louvain_communities_dict)}\n")

    for community_id, authors in louvain_communities_dict.items():
        print(f"Comunidade {community_id} ({len(authors)} nós):")
        print(authors)
        print("-" * 60)

    # 6. Retorna a estrutura para uso posterior
    return louvain_communities_dict

def louvain_communities_count(G, weight=None, resolution=1.0):
    if G.number_of_nodes() < 2:
        return 0

    communities = nx.algorithms.community.louvain.louvain_communities(
        G,
        weight=weight,
        resolution=resolution
    )
    return len(communities)

def louvain_communities_count_by_year(G, weight=None, resolution=1.0):
    result = {
        "total": louvain_communities_count(G, weight, resolution)
    }

    # Subgrafos por ano
    edges_by_year = defaultdict(list)

    for u, v, data in G.edges(data=True):
        if 'year' in data:
            edges_by_year[data['year']].append((u, v, data))

    for year, edges in sorted(edges_by_year.items()):
        G_year = nx.Graph()
        G_year.add_edges_from(edges)

        result[year] = louvain_communities_count(G_year, weight, resolution)


    for year, count in result.items():
        print(f"{year}: {count} comunidades")

def getComponentGigiantAnalysisByYear():
    # Lista dos anos presentes nas arestas
    anos = set(nx.get_edge_attributes(sbsc_graph, 'year').values())

    resumo = []

    for ano in sorted(anos):
        # Filtra arestas do ano
        arestas_ano = [(u, v) for u, v, d in sbsc_graph.edges(data=True) if d.get('year') == ano]
        
        # Cria subgrafo com essas arestas
        G_ano = nx.Graph()
        G_ano.add_edges_from(arestas_ano)
         
        # Adiciona nós isolados que possam existir no ano
        autores_ano = set()
        for u, v in arestas_ano:
            autores_ano.update([u, v])
        G_ano.add_nodes_from(autores_ano)

        total_autores = G_ano.number_of_nodes()
        
        if total_autores == 0:
            tamanho_gigante = 0
            proporcao = 0.0
        else:
            # Encontra componente gigante
            componentes = nx.connected_components(G_ano)
            gigante = max(componentes, key=len)
            tamanho_gigante = len(gigante)
            proporcao = tamanho_gigante / total_autores

        resumo.append({
            'ano': ano,
            'autores_totais': total_autores,
            'tamanho_gigante': tamanho_gigante,
            'proporcao': proporcao
        })

    componentes = nx.connected_components(sbsc_graph)
    maior_componente = max(componentes, key=len)
    tamanho_gigante_completo = len(maior_componente)
    resumo.append({
        'ano': 'Completo',
        'autores_totais': sbsc_graph.number_of_nodes(),
        'tamanho_gigante': tamanho_gigante_completo,
        'proporcao': tamanho_gigante_completo / sbsc_graph.number_of_nodes()
    })

    # Exibe os resultados formatados
    for r in resumo:
        print(f"Ano: {r['ano']}")
        print(f"Autores totais: {r['autores_totais']}")
        print(f"Tamanho do componente gigante: {r['tamanho_gigante']}")
        print(f"Proporção: {r['proporcao'] * 100:.2f}%\n")

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

# count_nodes_edges_by_year(sbsc_graph)
print("===============================================\n\n\n\n")
getCentralityMetrics()
# top10_closeness_centrality(sbsc_graph)
# top10_closeness_like_gephi(sbsc_graph)
print("===============================================\n\n\n\n")
# girvanNewmanCommunityDetection()
# louvainCommunityDetection()
# louvain_communities_and_its_authors()
# louvain_communities_count_by_year(sbsc_graph)

# getComponentGigiantAnalysisByYear()
print("===============================================\n\n\n\n")
# plotCollaborationMatrix()
print("===============================================\n\n\n\n")
exportGraph()
