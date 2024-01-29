import json

SETTINGS = {
    "node_size": 10,
    "node_color": "blue",
    "border_color": "black",
    "edge_color": "black",
    "border_width": 1,
    "edge_width": 1,
    "text_size": 12,
    "text_color": "black",
    "text_family": "Arial",
}


class Node:
    def __init__(self, node):
        self.pos = node["pos"]
        self.properties = node["properties"]

    def __setitem__(self, key, value):
        self.properties[key] = value

    def __getitem__(self, key):
        return self.properties[key]

    def json(self):
        return {"pos": self.pos, "properties": self.properties}


class Edge:
    def __init__(self, edge):
        self.source = edge["source"]
        self.target = edge["target"]

    def json(self):
        return {"source": self.source, "target": self.target}


class Graph:
    def __init__(self, nodes={}, edges=[]):
        self.nodes = nodes
        self.edges = edges

    @classmethod
    def from_json(cls, file):
        with open(file, "r") as f:
            graph = json.load(f)

        nodes = graph["nodes"]
        edges = graph["edges"]

        nodes = {n: Node(o) for n, o in nodes.items()}
        edges = [Edge(e) for e in edges]

        return cls(nodes, edges)

    def save(self, file):
        with open(file, "w") as f:
            json.dump(self.json(), f)

    def json(self):
        return {
            "nodes": {n: o.json() for n, o in self.nodes.items()},
            "edges": [e.json() for e in self.edges],
        }

    def draw(self, canvas=None, clearprev=True, offset=(0, 0), scale=1):
        if canvas is None:
            canvas = self.canvas
        else:
            self.canvas = canvas

        if clearprev:
            canvas.delete("all")

        # Draw edges first
        for edge in self.edges:
            source = self.nodes[edge.source]
            target = self.nodes[edge.target]
            canvas.create_line(
                source.pos[0] * scale + offset[0],
                source.pos[1] * scale + offset[1],
                target.pos[0] * scale + offset[0],
                target.pos[1] * scale + offset[1],
                width=SETTINGS["edge_width"],
                fill=SETTINGS["edge_color"],
            )

        # Draw nodes second
        for name, node in self.nodes.items():
            c = "custom" in node.properties

            if c:
                SETTINGS.update(node.properties["custom"])

            r = SETTINGS["node_size"] / 2
            ts = SETTINGS["text_size"]
            tf = SETTINGS["text_family"]
            sc = SETTINGS["border_color"]
            if node.properties.get("capital", False) and not c:
                color = "yellow"
            else:
                color = SETTINGS["node_color"]

            canvas.create_oval(
                (node.pos[0] - r) * scale + offset[0],
                (node.pos[1] - r) * scale + offset[1],
                (node.pos[0] + r) * scale + offset[0],
                (node.pos[1] + r) * scale + offset[1],
                fill=color,
                outline=sc,
                width=SETTINGS["border_width"],
            )
            canvas.create_text(
                node.pos[0] * scale + offset[0],
                (node.pos[1] + r + ts) * scale + offset[1],
                text=name,
                fill=SETTINGS["text_color"],
                font=(tf, ts * scale),
            )

        canvas.update()

    def add_node(self, node: str, pos: list):
        self.nodes[node] = Node({"pos": pos, "properties": {}})

    def remove_node(self, node: str):
        # Remove all edges that contain the node
        self.edges = [e for e in self.edges if node not in [e.source, e.target]]
        # Remove the node
        self.nodes.pop(node)

    def add_edge(self, source: str, target: str):
        self.edges.append(Edge({"source": source, "target": target}))


def find_node(g: Graph, x, y) -> str:
    r = SETTINGS["node_size"] / 2
    nodes = []
    for name, node in g.nodes.items():
        if abs(x - node.pos[0]) <= 2 * r and abs(y - node.pos[1]) <= 2 * r:
            nodes.append(name)

    if len(nodes) == 1:
        return nodes[0]
    elif len(nodes) > 1:
        # select the node with the smallest distance
        min_dist = float("inf")
        min_node = None
        for node in nodes:
            dist = abs(x - g.nodes[node].pos[0]) + abs(y - g.nodes[node].pos[1])
            if dist < min_dist:
                min_dist = dist
                min_node = node
        return min_node
    else:
        return None
