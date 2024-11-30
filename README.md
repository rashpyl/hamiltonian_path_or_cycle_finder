# Documentation 
## Problem description
**Hamiltonian Path**: A path that visits each vertex in a graph exactly once.

**Hamiltonian Cycle**: A cycle that visits each vertex in a graph exactly once and returns to the starting vertex.

**Given a graph $G=(V,E)$** where:
$V$ is the set of vertices. $E$ is the set of edges.

We want to determine if there exists a Hamiltonian path or cycle.

## Encoding
The problem is encoded using boolean variable: $X_{v, i}$, which is true if vertex $v$ is at position $i$ in the path (or cycle), where $v \in V$ and $i \in \{1, 2, \dots, |V|\}$.

To represent the decision problem if there is a solution to the finding if the Hamiltonian path exists, we use the following constraints:

1. **Every vertex v must be once in a path, but vertex $v$ cannot occupy more than one position in the path**:

- **If vertex $v$ is at position $i$, it cannot be at position $j$, different from $i$.**:

    $X_{v,1} \implies (\neg X_{v,2} \land \neg X_{v,3} \land \neg X_{v,4} \land \dots \land \neg X_{v,n})$

    Expand implication:

    $(\neg X_{v,1} \lor \neg X_{v,2}) \land (\neg X_{v,1} \lor \neg X_{v,3}) \land \dots \land (\neg X_{v,1} \lor \neg X_{v,n})$

    This is equivalent to:

    $\bigwedge_{i \neq j} (\neg X_{v,i} \lor \neg X_{v,j})$
   
- **Vertex v must be at least at one position**:

    $X_{v,1} \lor X_{v,2} \lor X_{v,3} \lor \dots \lor X_{v,n}$


   Where $i=0$ means that there is no position in a graph.   

2. **Every position in the path is occupied by exactly one vertex**:  

   For each position $i$ in the **path**:

- **At least one vertex occupies the position**:

   $X_{1,i} \lor X_{2,i} \lor X_{3,i} \lor \dots \lor X_{n,i}$

   

- **At most one vertex occupies the position**:

   For each position $i$ in the **path**, and for any pair of vertices $u \neq v$:


   $\bigwedge_{u \neq v} (\neg X_{u,i} \lor \neg X_{v,i})$


3. **If there is no edge from $u$ to $v$, we cannot use $uv$ edge in the Hamiltonian path (or cycle)**:

    $\neg X_{u,i} \lor \neg X_{v,i+1}$

    For all $i$ $\in$ $\{1, 2, \dots, |V| - 1\}$ and $(u, v)$ $\notin$ $E$.


4. **Add an edge from the last position back to the first (for the Hamiltonian cycle)**:

    For $(u, v) \in E$:

    $\neg X_{u,|V|} \lor \neg X_{v,1} \lor E(u, v)$


## Input format

The input JSON contains the following structure:
- `vertices`: A list of graph vertices (e.g., `[1, 2, 3, 4]`).
- `edges`: A list of edges in the graph, represented as pairs of vertices (e.g., `[[1, 2], [2, 3]]`). **Each edge is directed, so `[1, 2]` and `[2, 1]` are distinct edges.**
- `type`: Specifies the type of task. `"cycle"` means finding a Hamiltonian cycle, and `"path"` means finding a Hamiltonian path.

### Output format

The output is a dictionary:
- If a solution exists, it returns a list of vertices in the order of the path or cycle in standard output.
- If no solution exists, it returns `No Hamiltonian path exists` or `No Hamiltonian cycle exists`.

## Description of included examples

1. **`input.json`**:
   - A small graph with 4 vertices and a closed cycle.
   - A simple, human-analyzable instance.

2. **`input2.json`**:
   - A small graph with 4 vertices, where a necessary edge is missing to form a cycle.
   - Demonstrates a scenario where no solution exists.

3. **`input3.json`**:
   - A graph with 100 vertices, where each vertex has at least 30 edges (including back edges).
   - This example took 3 seconds to run on Apple Macbook 2021 with M1 Pro chip. 

## Conclusion

This script is capable of solving both small and large instances of Hamiltonian cycles and paths. During testing, it successfully handled graphs with 100 vertices and many edges.
