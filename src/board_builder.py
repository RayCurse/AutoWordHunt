import cv2
import numpy as np
import easyocr
reader = easyocr.Reader(["en"])

class LetterTile:
    def __init__(self, letter, boundingBox):
        self.letter = letter.upper()
        self.edges = set()
        self.boundingBox = boundingBox

    def getBoundingBoxCenter(self):
        return np.array([
            (self.boundingBox[0] + self.boundingBox[2])//2,
            (self.boundingBox[1] + self.boundingBox[3])//2])

uppercaseLetters = "".join(chr(i) for i in range(65, 91)) + "|1l0"

def getLetterTiles(img):
    imgArr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
    imgArr = cv2.threshold(imgArr, 20, 255, cv2.THRESH_BINARY_INV)[1]

    contours, _ = cv2.findContours(imgArr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    letterTiles = set()
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        padding = int(0.3*h)
        letterImg = cv2.copyMakeBorder(imgArr[y:y+h, x:x+w], padding, padding, padding, padding, cv2.BORDER_CONSTANT, value=(0, 0, 0))
        letterImg = cv2.resize(letterImg, None, fx = 2, fy = 2, interpolation = cv2.INTER_CUBIC)
        letterImg = cv2.bitwise_not(letterImg)
        letterImg = cv2.GaussianBlur(letterImg, (7,7), 0)
        results = reader.readtext(letterImg, allowlist=uppercaseLetters, low_text=0.1, text_threshold=0.3)
        c = ""
        if len(results) > 0:
            c = results[0][1]

        if len(c) > 0:
            c = c[0]

            # Correct confusions that ocr can make
            if c == "|" or c == "1" or c == "l":
                c = "I"

            if c == "0" or c == "o":
                c = "O"

            if c.isalpha():
                letterTiles.add(LetterTile(c[0], (x, y, x + w - 1, y + h - 1)))

    return letterTiles

def _rayBoxIntersection(origin, direction, box):
    # tests for intersection between ray (origin and direction) and axis aligned box (4-tuple of minX, minY, maxX, maxY)
    if direction[0] == 0 and direction[1] == 0:
        return False

    # if x direction is 0, switch the x and y coords of the system (this doesn't change the final answer)
    if direction[0] == 0:
        direction = np.array([direction[1], direction[0]])
        origin = np.array([origin[1], origin[0]])
        box = (box[1], box[0], box[3], box[2])

    k1 = (box[0] - origin[0])/direction[0]
    k2 = (box[2] - origin[0])/direction[0]
    if k1 < 0 and k2 < 0:
        return False

    p1 = origin + max(k1, 0)*direction
    p2 = origin + max(k2, 0)*direction
    return min(p1[1], p2[1]) <= box[3] and max(p1[1], p2[1]) >= box[1]

def _getNeighborInDirection(letterTile, letterTiles, direction):
    minDist = float("inf")
    neighbor = None
    for otherLetterTile in letterTiles:
        if otherLetterTile == letterTile:
            continue
        if _rayBoxIntersection(letterTile.getBoundingBoxCenter(), direction, otherLetterTile.boundingBox):
            dist = np.linalg.norm(otherLetterTile.getBoundingBoxCenter() - letterTile.getBoundingBoxCenter())
            if dist < minDist:
                minDist = dist
                neighbor = otherLetterTile

    return neighbor

def arrangeBoard(letterTiles):
    gridSpacing = float("inf")

    sideDirections = [np.array([1, 0]), np.array([0, 1]), np.array([-1, 0]), np.array([0, -1])]
    diagonalDirections = [np.array([1, 1]), np.array([-1, 1]), np.array([-1, -1]), np.array([1, -1])]

    for lt1 in letterTiles:
        for lt2 in letterTiles:
            if lt1 == lt2:
                continue
            dist = np.linalg.norm(lt1.getBoundingBoxCenter() - lt2.getBoundingBoxCenter())
            gridSpacing = min(gridSpacing, dist)

    for letterTile in letterTiles:
        for direction in sideDirections:
            neighbor = _getNeighborInDirection(letterTile, letterTiles, direction)
            if neighbor is None or np.linalg.norm(neighbor.getBoundingBoxCenter() - letterTile.getBoundingBoxCenter()) > 2*gridSpacing:
                continue
            letterTile.edges.add(neighbor)

        for direction in diagonalDirections:
            neighbor = _getNeighborInDirection(letterTile, letterTiles, direction)
            if neighbor is None or np.linalg.norm(neighbor.getBoundingBoxCenter() - letterTile.getBoundingBoxCenter()) > 2*np.sqrt(2)*gridSpacing:
                continue
            letterTile.edges.add(neighbor)

def findWord(img, word):
    for (bbox, text, confidence) in reader.readtext(np.array(img), detail=1):
        if text.lower() == word.lower():
            return bbox

    return None
