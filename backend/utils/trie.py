class TrieNode:
    def __init__(self, c):
        self.data = c
        self.isEnd = False
        self.children = {}
        self.is_band = False
        self.is_album = False
        self.is_song = False
        self.original_data = None


class Trie:
    def __init__(self):
        self.root = TrieNode('')

    def insert_band(self, band_name):
        node = self.root
        for ch in band_name.lower():
            if ch not in node.children:
                node.children[ch] = TrieNode(ch)
            node = node.children[ch]
        node.isEnd = True
        node.is_band = True
        node.original_data = band_name

    def insert_album(self, band_name, album_title):
        band_node = self._find_band_node(band_name.lower())
        if band_node:
            node = band_node
            for ch in album_title.lower():
                if ch not in node.children:
                    node.children[ch] = TrieNode(ch)
                node = node.children[ch]
            node.isEnd = True
            node.is_album = True
            node.original_data = album_title

    def insert_song(self, band_name, album_title, song_title):
        album_node = self._find_album_node(
            band_name.lower(), album_title.lower())
        if album_node:
            node = album_node
            for ch in song_title.lower():
                if ch not in node.children:
                    node.children[ch] = TrieNode(ch)
                node = node.children[ch]
            node.isEnd = True
            node.is_song = True
            node.original_data = song_title

    def build_trie(self, data):
        for band in data:
            band_name = band['name']
            self.insert_band(band_name)
            for album in band.get('albums', []):
                album_title = album['title']
                self.insert_album(band_name, album_title)
                for song in album.get('songs', []):
                    song_title = song['title']
                    self.insert_song(band_name, album_title, song_title)

    def autocomplete_bands(self, prefix):
        res = []
        node = self.root
        for ch in prefix.lower():
            if ch in node.children:
                node = node.children[ch]
            else:
                return res
        self._find_bands(node, res)
        return res

    def autocomplete_albums(self, band_name, prefix):
        res = []
        band_node = self._find_band_node(band_name.lower())
        if band_node:
            node = band_node
            for ch in prefix.lower():
                if ch in node.children:
                    node = node.children[ch]
                else:
                    return res
            self._find_albums(node, res)
        return res

    def autocomplete_songs(self, band_name, album_title, prefix):
        res = []
        album_node = self._find_album_node(
            band_name.lower(), album_title.lower())
        if album_node:
            node = album_node
            for ch in prefix.lower():
                if ch in node.children:
                    node = node.children[ch]
                else:
                    return res
            self._find_songs(node, res)
        return res

    def _find_bands(self, node, res):
        if node.isEnd and node.is_band:
            res.append(node.original_data)
        for child in node.children.values():
            self._find_bands(child, res)

    def _find_albums(self, node, res):
        if node.isEnd and node.is_album:
            res.append(node.original_data)
        for child in node.children.values():
            self._find_albums(child, res)

    def _find_songs(self, node, res):
        if node.isEnd and node.is_song:
            res.append(node.original_data)
        for child in node.children.values():
            self._find_songs(child, res)

    def _find_band_node(self, band_name):
        node = self.root
        for ch in band_name:
            if ch in node.children:
                node = node.children[ch]
            else:
                return None
        return node if node.is_band else None

    def _find_album_node(self, band_name, album_title):
        band_node = self._find_band_node(band_name)
        if not band_node:
            return None
        node = band_node
        for ch in album_title:
            if ch in node.children:
                node = node.children[ch]
            else:
                return None
        return node if node.is_album else None


if __name__ == "__main__":
    import json

    with open("data.json") as f:
        music_data = json.load(f)

    t = Trie()
    t.build_trie(music_data)

    print(t.autocomplete_bands("rad"))  # ["Radiohead"]
    print(t.autocomplete_albums("radiohead", "the k"))  # ["The King of Limbs"]
    print(t.autocomplete_songs("radiohead",
          "the king of limbs", "b"))  # ["Bloom"]
