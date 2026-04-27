"""
Trie (Prefix Tree)

All operations are O(L) time where L = length of the word.
Space: O(N * L) where N = number of words inserted.

Covers:
  1. Basic Trie — insert, search, startsWith
  2. Word Search II pattern — search with '.' wildcard
  3. Count words with given prefix
  4. Delete a word
"""


# ── 1. Basic Trie ─────────────────────────────────────────────────────────────

class TrieNode:
    def __init__(self):
        self.children: dict[str, "TrieNode"] = {}
        self.is_end = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self._find(word)
        return node is not None and node.is_end

    def starts_with(self, prefix: str) -> bool:
        return self._find(prefix) is not None

    def _find(self, prefix: str) -> TrieNode | None:
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    def count_words_with_prefix(self, prefix: str) -> int:
        node = self._find(prefix)
        if node is None:
            return 0
        return self._count_words(node)

    def _count_words(self, node: TrieNode) -> int:
        count = 1 if node.is_end else 0
        for child in node.children.values():
            count += self._count_words(child)
        return count

    def delete(self, word: str) -> bool:
        return self._delete(self.root, word, 0)

    def _delete(self, node: TrieNode, word: str, depth: int) -> bool:
        if depth == len(word):
            if not node.is_end:
                return False
            node.is_end = False
            return len(node.children) == 0   # safe to delete this node

        ch = word[depth]
        if ch not in node.children:
            return False

        should_delete_child = self._delete(node.children[ch], word, depth + 1)
        if should_delete_child:
            del node.children[ch]
            return not node.is_end and len(node.children) == 0

        return False


# ── 2. Word Dictionary with Wildcard ('.' matches any letter) ─────────────────
# LeetCode 211 — Design Add and Search Words Data Structure

class WordDictionary:
    def __init__(self):
        self.root = TrieNode()

    def add_word(self, word: str) -> None:
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word: str) -> bool:
        return self._dfs(self.root, word, 0)

    def _dfs(self, node: TrieNode, word: str, i: int) -> bool:
        if i == len(word):
            return node.is_end
        ch = word[i]
        if ch == ".":
            return any(self._dfs(child, word, i + 1) for child in node.children.values())
        if ch not in node.children:
            return False
        return self._dfs(node.children[ch], word, i + 1)


# ── Tests ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("── Basic Trie ──")
    trie = Trie()
    for word in ["apple", "app", "application", "apt", "bat"]:
        trie.insert(word)

    print(trie.search("apple"))        # True
    print(trie.search("app"))          # True
    print(trie.search("ap"))           # False
    print(trie.starts_with("ap"))      # True
    print(trie.starts_with("bat"))     # True
    print(trie.starts_with("cat"))     # False
    print(trie.count_words_with_prefix("app"))  # 3 (app, apple, application)

    trie.delete("app")
    print(trie.search("app"))          # False
    print(trie.search("apple"))        # True  (unaffected)

    print("\n── Wildcard Search ──")
    wd = WordDictionary()
    wd.add_word("bad")
    wd.add_word("dad")
    wd.add_word("mad")
    print(wd.search("pad"))    # False
    print(wd.search("bad"))    # True
    print(wd.search(".ad"))    # True
    print(wd.search("b.."))    # True
