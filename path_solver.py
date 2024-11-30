import json
from pysat.solvers import Glucose3
from itertools import product


def find_hamiltonian_from_json(file_path):

    with open(file_path, 'r') as file:
        graph_data = json.load(file)

    vertices = graph_data["vertices"]
    edges = graph_data["edges"]
    search_type = graph_data["type"]  # cycle or path
    n = len(vertices)  # how many vertices we have, also how many positions would we have in a path

    solver = Glucose3()

    def var(v, i): # var(v, i) is Xv,i, where v is a vertex, i is a position
        # encode variable Xv,i into a unique number
        return v * n + i + 1

    # Constraint 1: Every vertex v must be at least once in a path
    for v in range(n):
        solver.add_clause([var(v, i) for i in range(n)])

    # vertex v cannot occupy more than one position in the path
    for i, k in product(range(n), repeat=2):
        if i != k:
            for v in range(n):
                solver.add_clause([-var(v, i), -var(v, k)])

    # Constraint 2: Every position i in the path is occupied
    for i in range(n):
        solver.add_clause([var(v, i) for v in range(n)])

    #...occupied by exactly one vertex
    for i in range(n):
        for v, u in product(range(n), repeat=2):
            if v != u:
                solver.add_clause([-var(v, i), -var(u, i)])

    # Constraint 3: If there is no edge from v, we cannot use it in the Hamiltonian path:
    edges_set = set(tuple(edge) for edge in edges)
    for i in range(n - 1):
        for v, u in product(range(n), range(n)):
            if (vertices[v], vertices[u]) not in edges_set:
                solver.add_clause([-var(v, i), -var(u, i + 1)])

    # Check what to solve for (cycle or path)
    if search_type == "cycle":
        for v, u in product(range(n), range(n)):
            if (vertices[v], vertices[u]) not in edges_set:
                solver.add_clause([-var(v, n - 1), -var(u, 0)])  # v cant be the last vertex if there is no edge to the first vertex u

        if solver.solve():
            model = solver.get_model()
            solver.delete()

            cycle = [-1] * n # an array to store the Hamiltonian cycle.
            for i, v in product(range(n), range(n)):
                if model[var(v, i) - 1] > 0:  # if vertex v is in position i
                    cycle[i] = vertices[v]
            return {"type": "cycle", "result": cycle}

        solver.delete()
        return {"type": "cycle", "result": None}

    elif search_type == "path":
        # solve the SAT problem for a path
        if solver.solve():
            model = solver.get_model()
            solver.delete()

            path = [-1] * n
            for i, v in product(range(n), range(n)):
                if model[var(v, i) - 1] > 0:  # an array to store the Hamiltonian path.
                    path[i] = vertices[v]
            return {"type": "path", "result": path}

        solver.delete()
        return {"type": "path", "result": None}

    else:
        solver.delete()
        raise ValueError("Invalid type specified in the JSON file. Use 'cycle' or 'path'.")
