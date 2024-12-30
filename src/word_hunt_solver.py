import time
import numpy as np
from pathlib import Path
from pygtrie import CharTrie
from pynput import mouse
from pynput.mouse import Button, Controller

# Build trie
print("initializing word dictionary...")
_trie = None
_englishWordsFilePath = Path(__file__).parent / "word_list.txt"
with open(_englishWordsFilePath) as englishWordsFile:
    words = map(lambda x: x.rstrip("\r\n").upper(), englishWordsFile)
    _trie = CharTrie.fromkeys(words)

if _trie is None:
    exit("unable to build trie")

def findWords(letterTiles):
    seenWords = set()
    paths = list()

    tileOrder = list()
    selectedTiles = set()
    currentStr = list()

    def dfs(letterTile):
        tileOrder.append(letterTile)
        selectedTiles.add(letterTile)
        currentStr.append(letterTile.letter.upper())

        if len(currentStr) >= 3 and _trie.has_key(currentStr) and "".join(currentStr) not in seenWords:
            paths.append(tileOrder[::])
            seenWords.add("".join(currentStr))

        if _trie.has_subtrie(currentStr):
            for edge in letterTile.edges:
                if edge in selectedTiles:
                    continue
                dfs(edge)

        tileOrder.pop()
        selectedTiles.remove(letterTile)
        currentStr.pop()

    for letterTile in letterTiles:
        dfs(letterTile)

    return paths

def _interpolateMouseMovement(x, y, t, updateFreq=240):
    startPos = np.array([_mouseController.position[0], _mouseController.position[1]])
    endPos = np.array([x, y])
    t *= 1e9

    totalTimeElapsed = 0
    while totalTimeElapsed < t:
        t0 = time.time_ns()
        time.sleep(1/updateFreq)
        totalTimeElapsed += time.time_ns() - t0
        x = min(totalTimeElapsed / t, 1)
        pos = (1 - x)*startPos + x*endPos
        _mouseController.press(Button.left)
        _mouseController.position = (pos[0], pos[1])

    _mouseController.position = (endPos[0], endPos[1])

_mouseController = Controller()
_inputStepDuration = .02

def inputPath(path, bbox):
    boardScreenOrigin = np.array([bbox[0], bbox[1]])
    startPos = boardScreenOrigin + path[0].getBoundingBoxCenter()
    _mouseController.position = (startPos[0], startPos[1])

    # Clicking start tile a few times seems to reduce chances of a failed input
    for _ in range(2):
        _mouseController.press(Button.left)
        time.sleep(_inputStepDuration)
        _mouseController.release(Button.left)
        time.sleep(_inputStepDuration)

    _mouseController.press(Button.left)
    time.sleep(_inputStepDuration)

    for letterTile in path[1:]:
        pos = boardScreenOrigin + letterTile.getBoundingBoxCenter()
        _interpolateMouseMovement(pos[0], pos[1], _inputStepDuration)

    _mouseController.release(Button.left)
    time.sleep(_inputStepDuration)
