from collections import defaultdict

def dfs1(node, graph, visited, order):
    visited.add(node)
    for next_node in graph.get(node, []):
        if next_node not in visited:
            dfs1(next_node, graph, visited, order)
    order.append(node)

def toposort(graph):
    order = [] 
    visited = set()
    for node in graph: 
        if node not in visited: 
            dfs1(node, graph, visited, order)
    new_order = list(reversed(order))
    # return reversed(order)
    return new_order

def get_transpose(graph):
    transpose = defaultdict(list)
    for key, values in graph.items():
        for v in values:
            transpose[v].append(key)
    return transpose

def dfs2(node, graph, visited, components, i):
    visited.add(node)
    components[node] = i
    for next_node in graph.get(node, []):
        if next_node not in components:
            dfs2(next_node, graph, visited, components, i)

def get_connected_components(graph, order): 
    transpose = get_transpose(graph)
    visited = set()
    components = defaultdict(list)
    i = -1
    for i, node in enumerate(reversed(order)):
        if node not in visited:
            dfs2(node, transpose, visited, components, i)
    return components
    
def negate(x):
    if x[0] == '¬':
        return x[1:]
    else:
        return '¬' + x

def satisfy(variables, clauses): # *args
    graph = defaultdict(list)
    for a, b in clauses:        # args
        graph[negate(a)].append(b)
        graph[negate(b)].append(a)
    order = toposort(dict(graph))
    transpose = get_transpose(graph)
    components = get_connected_components(transpose, order)
    if any(components[v] == components[negate(v)] for v in variables):
        return False
    else:
        return set([
            max(v, negate(v), key=lambda x: components[x]) for v in variables
        ])