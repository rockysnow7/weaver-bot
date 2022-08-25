import enchant

from typing import Generator
from anytree import Node


ALPHABET = "abcdefghijklmnopqrstuvwxyz"


class Player:
    def __init__(self) -> None:
        self.dictionary = enchant.Dict("en_US")

    def get_valid_changes(self, word: str) -> Generator[str, None, None]:
        word = list(word)
        for i in range(len(word)):
            for c in ALPHABET:
                if c == word[i]:
                    continue

                w = [c for c in word]
                w[i] = c
                w = "".join(w)

                if self.dictionary.check(w):
                    yield w

    def get_parents(self, node: Node) -> list[Node]:
        nodes = [node]
        while not nodes[-1].is_root:
            nodes.append(nodes[-1].parent)

        return reversed(nodes[1:])

    def populate_leaf_nodes(self, node: Node, nodes: list[Node]) -> list[Node]:
        if not node.children:
            nodes.append(node)
        else:
            for child in node.children:
                self.populate_leaf_nodes(child, nodes)

    def add_leaves(self, node: Node) -> None:
        if not node.children:
            parent_words = [n.name for n in self.get_parents(node)]

            children_words = []
            for word in self.get_valid_changes(node.name):
                if word not in parent_words:
                    children_words.append(word)
            node.children = [Node(word) for word in children_words]
        else:
            for child in node.children:
                self.add_leaves(child)

    def pprint_path(self, words: list[str]) -> None:
        for word in words:
            print(word)

    def play(self, start_word: str, end_word: str) -> int:
        path = []

        root = Node(start_word)
        for _ in range(10):
            self.add_leaves(root)

            leaf_nodes = []
            self.populate_leaf_nodes(root, leaf_nodes)

            found = False
            for node in leaf_nodes:
                if node.name == end_word:
                    path = list(self.get_parents(node)) + [node]

                    found = True
                    break
            if found:
                break

        path = [node.name for node in path]
        if path:
            self.pprint_path(path)
        else:
            print("no path found")

        return len(path)
