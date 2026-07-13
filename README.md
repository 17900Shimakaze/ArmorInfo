# ArmorInfo

ArmorInfo shows the armor values of your current ship, or the ship you are
watching in observer mode, in a movable battle HUD window.

## Features

- Drag the window while the battle cursor is active.
- Hold Shift while dragging to snap the window to a grid.
- Change the window scale and background opacity from its settings button.
- Lock dragging or reset the saved position from the same settings panel.
- Position and appearance settings persist between battles.

## Requirements

- [DraggableUnbound2](https://github.com/AndrewTaro/DraggableUnbound2)
- [TTaroModConfig](https://github.com/AndrewTaro/TTaroModConfig)

Both requirements must be installed. ArmorInfo reuses their runtime UI
components, but it does not require any manual edits to TTaroModConfig.

## Install

1. Install DraggableUnbound2 and TTaroModConfig.
2. Copy ArmorInfo's `gui` and `PnFMods` folders, plus `PnFModsLoader.py`, into
   `(wows)/bin/(latest_number)/res_mods/`.
3. Start the game. The bundled ModsInstaller manifest adds ArmorInfo to the
   battle HUD automatically; do not edit `gui/battle_elements.xml` manually.
