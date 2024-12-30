import screen_grabber
import board_builder
import word_hunt_solver
import sys
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
board_builder.arrangeBoard(letterTiles)

imageDraw = ImageDraw(image)
for letterTile in letterTiles:
    txtSize = max(int(0.03*image.size[1]), 1)
    imageDraw.rectangle(letterTile.boundingBox, outline=(255, 0, 0), width=2)
    imageDraw.text((letterTile.boundingBox[0], letterTile.boundingBox[1] - int(1.2*txtSize)), letterTile.letter, fill=(255, 0, 0), font_size=txtSize)
image.save(str(debugPath / "ocr.png"))

for letterTile in letterTiles:
    p0 = letterTile.getBoundingBoxCenter()
    for otherLetterTile in letterTile.edges:
        p1 = otherLetterTile.getBoundingBoxCenter()
        imageDraw.line((p0[0], p0[1], p1[0], p1[1]), fill=(255, 0, 0), width=1)
image.save(str(debugPath / "tileConnections.png"))

# Solve the word hunt game
print("finding words...")
paths = word_hunt_solver.findWords(letterTiles)
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
    word_hunt_solver.inputPath(path, bbox)
print()

if terminatePathInput:
    print("stopped automatic input")

print("done!")
