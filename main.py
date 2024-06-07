import math
import networkx as nx
import matplotlib.pyplot as plt

def prim_with_diameter_constraint(G, diameter_constraint):
    # Inicializando a árvore geradora mínima e o diâmetro atual
    T = nx.Graph()
    current_diameter = 0

    # Adicionando um nó arbitrário ao grafo T
    start_node = next(iter(G.nodes))
    T.add_node(start_node)

    # Caso ultrapasse = loop infinito
    limit_rate = len(G.edges)
    
    loop_counter = 0
    while len(T) < len(G):
        if loop_counter > limit_rate:
            print('Could not generate a MST with this diameter constraint!')
            exit(0)

        # Encontrando a aresta de menor peso que conecta um nó em T a um nó fora de T
        min_edge = None
        for u in T.nodes:
            for v in G.neighbors(u):
                if v not in T.nodes:
                    if min_edge is None or G[u][v]['weight'] < G[min_edge[0]][min_edge[1]]['weight']:
                        min_edge = (u, v)

        # Adicione o nó e a aresta mínima ao grafo T
        u, v = min_edge
        T.add_node(v)
        T.add_edge(u, v, weight=G[u][v]['weight'])

        # Atualizando o diâmetro atual
        current_diameter = nx.diameter(T)

        # Verificando se o diâmetro excede a restrição
        if current_diameter > diameter_constraint:
            # Se exceder, remove a aresta adicionada mais recentemente e o nó correspondente
            T.remove_edge(u, v)
            T.remove_node(v)
        
        loop_counter += 1
        
    return T

#==========================#
def calc_weight(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

#==========================#
def set_weight(G):
    for u, v in G.edges:
        if 'weight' not in G[u][v]:
            G[u][v]['weight'] = 1


#==========================#
if __name__ == '__main__':
    G = nx.read_gml("topo/Sprint.gml", label="id")

    diameter_constraint = 5 # Restrição de diâmetro

    # Define todos os pesos das arestas para 1
    set_weight(G) 

    T = prim_with_diameter_constraint(G, diameter_constraint)
    # print("Árvore Geradora Mínima com Restrição de Diâmetro:", T.edges)

    print("Generating figure...")
    plt.figure(figsize=(15, 8))
    pos = nx.spring_layout(T)
    nx.draw(T, pos, with_labels=True, edge_color="black", width=0.5, node_color="red", node_size=1000)
    plt.savefig(f'figures/agmrd.png')
    plt.close()
