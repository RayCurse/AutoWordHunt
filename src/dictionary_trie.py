from pathlib import Path
from pygtrie import CharTrie

print("initializing word dictionary...")
trie = None
_englishWordsFilePath = Path(__file__).parent / "word_list.txt"
with open(_englishWordsFilePath) as englishWordsFile:
    words = map(lambda x: x.rstrip("\r\n").upper(), englishWordsFile)
    trie = CharTrie.fromkeys(words)

if trie is None:
    exit("unable to build trie")
