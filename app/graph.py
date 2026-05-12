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
        node = Node(id=id, name=name, profileurl=profileurl, avatarurl=avatarurl)

        if node not in self.nodes:
            self.nodes.append(node)

    def add_link(self, source: str, target: str) -> None:
        link = Link(source=source, target=target)

        if link not in self.links:
            self.links.append(link)

    def serialize(self) -> dict:
        return asdict(self)

graphs: dict[str, Graph] = {}