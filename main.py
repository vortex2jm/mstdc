import networkx as nx
import matplotlib.pyplot as plt

def mstdc(G, d_constraint):
  T = nx.Graph()

  start_g_node = next(iter(G.nodes))
  T.add_node(start_g_node)

  limit_rate = (len(G.edges)*2)  
  loop_counter = 0
  
  while len(T) < len(G):
    # If infinite loop
    if loop_counter > limit_rate:
      print('Could not generate a MST with this diameter constraint!')
      exit(0)

    adj_edge = None
    for u in T.nodes:
      for v in G.neighbors(u):
        if v not in T.nodes:
          if not adj_edge:
            adj_edge = (u, v)

    u, v = adj_edge
    T.add_node(v)
    T.add_edge(u, v)

    if nx.diameter(T) > d_constraint:
      T.remove_edge(u, v)
      T.remove_node(v)
    
    loop_counter += 1
  return T


if __name__ == '__main__':
  G = nx.read_gml("topo/Xeex.gml", label="label")
  d_constraint = 8
  T = mstdc(G, d_constraint)
  print("Generating figure...")
  plt.figure(figsize=(15, 8))
  pos = nx.spring_layout(T)
  nx.draw(T, pos, with_labels=True, edge_color="black", width=0.5, node_color="red", node_size=1000)
  plt.savefig(f'figures/mstdc.png')
  plt.close()
