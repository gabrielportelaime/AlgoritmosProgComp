from collections import deque

class TrieNode:
    def __init__(self):
        self.children = {}
        self.fail = None
        self.is_end_of_word = False
        self.keyword = None

class AhoCorasick:
    def __init__(self):
        self.root = TrieNode()

    def add_keyword(self, keyword):
        node = self.root
        for char in keyword:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.keyword = keyword

    def build_failure_links(self):
        queue = deque()
        for child in self.root.children.values():
            child.fail = self.root
            queue.append(child)

        while queue:
            curr_node = queue.popleft()
            for char, child in curr_node.children.items():
                queue.append(child)
                fail_node = curr_node.fail
                while fail_node and char not in fail_node.children:
                    fail_node = fail_node.fail
                child.fail = fail_node.children[char] if fail_node else self.root

    def find_keywords(self, text):
        result = []
        curr_node = self.root
        for i, char in enumerate(text):
            while curr_node and char not in curr_node.children:
                curr_node = curr_node.fail
            if not curr_node:
                curr_node = self.root
                continue
            curr_node = curr_node.children[char]
            if curr_node.is_end_of_word:
                result.append((i - len(curr_node.keyword) + 1, curr_node.keyword))
        return result

# Exemplo de uso:
keywords = ['he', 'she', 'his', 'hers']
text = 'ushers'
ac = AhoCorasick()
for keyword in keywords:
    ac.add_keyword(keyword)
ac.build_failure_links()
matches = ac.find_keywords(text)
for start_index, keyword in matches:
    print(f"Encontrada correspondência: {keyword} em posição {start_index}")