import json

SETTINGS = {
    "node_size": 10,
    "node_color": "blue",
    "edge_color": "black",
    "edge_width": 1,
    "text_size": 12,
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

    def draw(self, canvas=None):
        if canvas is None:
            canvas = self.canvas
        else:
            self.canvas = canvas

        # Clear the canvas
        canvas.delete("all")

        # Draw edges first
        for edge in self.edges:
            source = self.nodes[edge.source]
            target = self.nodes[edge.target]
            canvas.create_line(
                source.pos[0], source.pos[1], target.pos[0], target.pos[1]
            )

        # Draw nodes second
        for name, node in self.nodes.items():
            r = SETTINGS["node_size"] / 2
            ts = SETTINGS["text_size"]
            if "capital" in node.properties and node['capital'] is True:
                color = "yellow"
            else:
                color = SETTINGS["node_color"]
            canvas.create_oval(
                node.pos[0] - r,
                node.pos[1] - r,
                node.pos[0] + r,
                node.pos[1] + r,
                fill=color,
            )
            canvas.create_text(node.pos[0], node.pos[1] + r + ts, text=name)

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
