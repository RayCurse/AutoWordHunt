import time
import numpy as np
from dictionary_trie import trie
from pynput import mouse
from pynput.mouse import Button, Controller

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

        if len(currentStr) >= 3 and trie.has_key(currentStr) and "".join(currentStr) not in seenWords:
            paths.append(tileOrder[::])
            seenWords.add("".join(currentStr))

        if trie.has_subtrie(currentStr):
            unselectedTiles = [tile for tile in letterTiles if tile not in selectedTiles]
            for nextTile in unselectedTiles:
                dfs(nextTile)

        tileOrder.pop()
        selectedTiles.remove(letterTile)
        currentStr.pop()

    for letterTile in letterTiles:
        dfs(letterTile)

    return paths

_mouseController = Controller()
_inputStepDuration = .02

def inputPath(path, bbox, enterButtonBBox):
    boardScreenOrigin = np.array([bbox[0], bbox[1]])
    enterButtonPos = np.array([(enterButtonBBox[0] + enterButtonBBox[2])//2, (enterButtonBBox[1] + enterButtonBBox[3])//2])

    for letterTile in path:
        pos = boardScreenOrigin + letterTile.getBoundingBoxCenter()
        _mouseController.position = (pos[0], pos[1])
        time.sleep(_inputStepDuration)
        _mouseController.press(Button.left)
        time.sleep(_inputStepDuration)
        _mouseController.release(Button.left)
        time.sleep(_inputStepDuration)

    _mouseController.position = boardScreenOrigin + enterButtonPos
    time.sleep(_inputStepDuration)
    _mouseController.press(Button.left)
    time.sleep(_inputStepDuration)
    _mouseController.release(Button.left)
    time.sleep(_inputStepDuration)
