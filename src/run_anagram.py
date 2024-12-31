import sys
import screen_grabber
import board_builder
import anagram_solver
from operator import itemgetter
from PIL.ImageDraw import ImageDraw
from pathlib import Path
from pynput import mouse

# Set up debug directory
debugPath = Path(__file__).parent.parent / "debug"
debugPath.mkdir(exist_ok=True)
for f in debugPath.glob("*"):
    f.unlink()

# Get screenshot and position of gameboard on the iPhone Mirroring window
input("ready to take screenshot (press enter to continue)")
image, bbox = screen_grabber.promptScreenshot()
image.save(str(debugPath / "screenshot.png"))

# Build model of the letter tiles and game board
print("scanning image...")
letterTiles = board_builder.getLetterTiles(image)
enterButtonBB = board_builder.findWord(image, "ENTER")
if enterButtonBB is None:
    print("could not find enter button")
    exit(1)
enterButtonBB = (
    min(map(itemgetter(0), enterButtonBB)),
    min(map(itemgetter(1), enterButtonBB)),
    max(map(itemgetter(0), enterButtonBB)),
    max(map(itemgetter(1), enterButtonBB)))

imageDraw = ImageDraw(image)
imageDraw.rectangle(enterButtonBB, outline=(255, 0, 0), width=2)
for letterTile in letterTiles:
    txtSize = max(int(0.03*image.size[1]), 1)
    imageDraw.rectangle(letterTile.boundingBox, outline=(255, 0, 0), width=2)
    imageDraw.text((letterTile.boundingBox[0], letterTile.boundingBox[1] - int(1.2*txtSize)), letterTile.letter, fill=(255, 0, 0), font_size=txtSize)

image.save(str(debugPath / "ocr.png"))

# Solve the anagram game
paths = anagram_solver.findWords(letterTiles)
paths.sort(key=len, reverse=True)
with open(debugPath / "found_words.txt", "w") as file:
    for path in paths:
        word = "".join(tile.letter for tile in path)
        file.write(word + "\n")

# Kill switch for automatic input
terminatePathInput = False
def onClick(x, y, button, pressed):
    global terminatePathInput
    if not (button == mouse.Button.right and pressed == True):
        return
    terminatePathInput = True
    return False
mouse.Listener(on_click=onClick).start()

# Input words
print("inputting words (right click to stop)...")
for path in paths:
    if terminatePathInput:
        break
    currentWord = "".join(tile.letter for tile in path)
    print("\r\033[2K\033[1G", end="")
    print(currentWord, end="")
    sys.stdout.flush()
    anagram_solver.inputPath(path, bbox, enterButtonBB)
print()

if terminatePathInput:
    print("stopped automatic input")

print("done!")
