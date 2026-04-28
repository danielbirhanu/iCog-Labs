from graphviz import Digraph


def generate_tree(edges, filename="decomposition_tree"):
    dot = Digraph(comment="HTN Decomposition Tree")

    for parent, child in edges:
        dot.node(parent)
        dot.node(child)
        dot.edge(parent, child)

    dot.render(filename, format="png", cleanup=True)
    print(f"Decomposition tree saved as {filename}.png")