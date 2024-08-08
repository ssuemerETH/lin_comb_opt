import networkx as nx
from pulp import *

# Given a task graph where nodes represent tasks that each take a certain amount of time,
# determines the minimal time to complete all tasks. We assume that a task can be started only
# when all its predecessor tasks have been completed. Uses linear programming to solve the problem.

# G must be a directed acyclic graph (DAG) with positive float valued vertex attributes called time
def minimal_makespan(G : nx.DiGraph):

  # Define empty LP
  ms_LP = LpProblem("makespan_LP", LpMinimize)

  z = LpVariable("z", lowBound=0)
  vertex_vars = {v : LpVariable(str(v), lowBound=0) for v in G.nodes}

  # Objective
  ms_LP += z

  for v in G.nodes:
    ms_LP += z >= vertex_vars[v] + G.nodes[v]["time"]
  
  for (u, v) in G.edges:
    ms_LP += vertex_vars[v] >= vertex_vars[u] + G.nodes[u]["time"]
  
  ms_LP.solve()

  return value(ms_LP.objective)

if __name__ == "__main__":
  # Construct example test graph.
  G = nx.DiGraph()

  times = [4, 7, 5, 3, 10, 1, 6, 2, 1]

  nodes = [(i, {"time" : times[i - 1]}) for i in range(1, 10)]
  G.add_nodes_from(nodes)

  edges = [(1, 2), (1, 3), (2, 4), (2, 6), (3, 4), (3, 5), (4, 7), (5, 8), (6, 7), (6, 9), (7, 8), (7, 9)]
  G.add_edges_from(edges)

  # Should be 22.
  val = minimal_makespan(G)
  print(f"Minimal makespan for this graph is: {val}")




