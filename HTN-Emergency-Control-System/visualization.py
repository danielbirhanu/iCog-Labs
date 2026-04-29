def generate_tree(edges, filename="decomposition_tree.txt"):
    tree = {}

    for parent, child in edges:
        tree.setdefault(parent, [])
        tree[parent].append(child)

    def print_tree(node, prefix="", is_last=True, lines=None):
        if lines is None:
            lines = []

        connector = "└── " if is_last else "├── "
        lines.append(prefix + connector + node)

        children = tree.get(node, [])
        new_prefix = prefix + ("    " if is_last else "│   ")

        for index, child in enumerate(children):
            print_tree(
                child,
                new_prefix,
                index == len(children) - 1,
                lines
            )

        return lines

    lines = print_tree("ROOT")

    print("\nDecomposition Tree:")
    for line in lines:
        print(line)

    with open(filename, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))

    print(f"\nText decomposition tree saved as {filename}")