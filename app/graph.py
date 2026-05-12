from dataclasses import dataclass, field, asdict
import json

@dataclass
class Node:
    id: str
    name: str
    profileurl: str
    avatarurl: str

@dataclass
class Link:
    source: str
    target: str

@dataclass
class Graph:
    nodes: list[Node] = field(default_factory=list)
    links: list[Link] = field(default_factory=list)

    def add_node(self, id: str, name: str, profileurl: str, avatarurl: str) -> None:
        self.nodes.append(Node(id=id, name=name, profileurl=profileurl, avatarurl=avatarurl))

    def add_link(self, source: str, target: str) -> None:
        self.links.append(Link(source=source, target=target))

    def serialize(self) -> dict:
        return asdict(self)

graph = Graph()