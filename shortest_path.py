import networkx as nx
from pulp import *

# Given a directed graph where edges have non-negative weights attached to them,
# and a starting vertex in this graph, computes the lengths of the shortest paths from 
# s to all vertices in the graph using linear programming. 
# The edges in G must have float valued attributes called "weight". 
def shortest_path(G : nx.DiGraph, s : int):

  # Initialize empty LP
  sp_LP = LpProblem("shortest_path_LP", LpMaximize)

  if s not in G.nodes:
    raise Exception(f"{s} is not a node in the given graph.")
  
  vertex_vars = {v : LpVariable(str(v), lowBound=0) for v in G.nodes}
  
  # Objective
  sp_LP += lpSum(vertex_vars.values())

  # First vertex has distance 0 to itself
  sp_LP += vertex_vars[s] == 0

  for (u, v) in G.edges:
    sp_LP += vertex_vars[v] <= vertex_vars[u] + G.edges[(u, v)]["weight"]

  sp_LP.solve()

  res = [(v, vertex_vars[v].value()) for v in G.nodes]
  res.sort(key=lambda x: x[0])

  return res

if __name__ == "__main__":
  # Create example graph
  G = nx.DiGraph()

  nodes = range(10)
  edges = [(0, 1, 9), 
           (0, 2, 12),
           (1, 4, 12),
           (2, 4, 10),
           (2, 5, 3),
           (3, 1, 7),
           (3, 6, 1),
           (4, 3, 6),
           (4, 7, 9),
           (4, 5, 2),
           (5, 4, 4),
           (6, 8, 5),
           (6, 7, 1),
           (7, 5, 5),
           (7, 3, 5),
           (7, 8, 3),
           (7, 9, 5),
           (8, 3, 5),
           (8, 6, 3),
           (8, 9, 1)]
  
  G.add_nodes_from(nodes)
  G.add_edges_from([(u, v, {"weight" : w}) for (u, v, w) in edges])

  sp_vals = shortest_path(G, 0)

  print(sp_vals)