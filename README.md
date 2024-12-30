# Auto Word Hunt Player
Script that automatically solves and plays GamePigeon's word hunt game. Uses [iPhone Mirroring](https://support.apple.com/en-us/120421) to view and play the game, so a supported MacOS and iPhone are required.

https://github.com/user-attachments/assets/823496bd-6a73-480e-8aff-dea3e4801bd6

## Requirements
* Your system meets the [iPhone Mirroring system requirements](https://support.apple.com/en-us/120421#requirements)
* Python 3
* Basic CLI knowledge

## Installation
1. Download this repo
2. `cd` into the root directory of this repo
3. Run `pip install -r requirements.txt`

## Usage
1. `cd` into the root directory of this repo
2. Run `python src/run.py`
3. Open word hunt on iPhone Mirroring
4. Begin the game
5. Navigate back to the CLI and press enter
6. Hold mouse down and drag to select the area of the screen containing only the word hunt board (just the letter grid and nothing else)
   <details>
     <summary>Example screenshot</summary>
     <img src="https://github.com/user-attachments/assets/fb075d35-801a-4dec-87c7-a7e8a4c872d4" />
   </details>

## Notes
* Right click to terminate the automatic input at any time
* The script requires screenshotting your entire screen and controlling the mouse
  * May require relevant permissions and settings to be configured when running for the first time
* Don't move the iPhone Mirroring window as the auto input assumes the grid is in the same place on the screen as it was when it was selected
