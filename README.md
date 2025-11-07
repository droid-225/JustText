# Just Text

A small text-based adventure / roguelite built with Pygame.

---

## Requirements

- Python 3.10 or newer (code uses modern type syntax).
- Pygame (tested with pygame 2.x).

Optional (development): a virtual environment (venv).

---

## Quick setup (Windows / PowerShell)

Open PowerShell in the project folder (`c:\Users\aryan\Desktop\Progammin\Python\JustText`) and run:

```powershell
# create and activate a venv (optional but recommended)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# install pygame
pip install pygame
```

If you prefer not to use a virtual env, just run `pip install pygame` globally.

---

## Run the game

From the project root (where `main.py` lives):

```powershell
python -u "c:\Users\aryan\Desktop\Progammin\Python\JustText\main.py"
```

The window is resizable and the game content will scale while preserving aspect ratio.

---

## Controls

- Number keys (1..5) — select options shown on-screen
- ESC — back / exit menu
- I — open Inventory
- U — open Stats
- TAB — in some screens (Inventory, Shop) toggles categories or tabs
- When you enter the Wilds you will travel and encounter events; choose numeric options to interact

Note: the project uses `VideoResize` handling; resizing the window keeps the aspect ratio of the logical game surface (700×500) and centers the view with black letterbox bars.

---

## Project structure (high level)

- `main.py` — entrypoint and game loop; contains window creation, scaling logic and screen manager wiring.
- `justtext/` — core package
  - `screens/` — various screen modules (wilds, shop, combat, inventory, etc.)
  - `components/` — UI components and systems (options, footer, event/ entity systems)
  - `util/` — helper modules (text renderer, item utils, leveling)
  - `state.py` — game state saving/loading and runtime state object
  - `assets/` — fonts and icon
- `saves/` — JSON save slots (slot1.json, slot2.json, slot3.json)

---

## Saving and load slots

Saves are stored as `saves/slot1.json`, `saves/slot2.json`, `saves/slot3.json`. Game state is automatically saved when switching screens that persist or on quit (unless viewing transient screens like Inventory/Stats).

---

## Assets & icon

- The project expects assets under `assets/` (fonts & icon). The window icon is loaded from `assets/icon/icon.png`. Use a square PNG (32×32 recommended) for best results.
- To change the icon, replace `assets/icon/icon.png` or update the path used in `main.py`.

---

## Notes for developers

- The game currently renders to a fixed logical resolution (700×500). This keeps layout code simple. If you want crisp text at larger sizes, consider adapting `util/text.py` to recreate fonts at a scaled size on VIDEORESIZE events.
- `state.py` uses modern typing (union operator `|`) and requires Python 3.10+.
- To add new entities, edit `justtext/components/entity_system.py` and reference them from `wilds` or other screens.

---

## Troubleshooting

- If Pygame cannot initialize the display, ensure your environment has access to a graphical display and that `pygame` is correctly installed in the active Python environment.
- If fonts aren't found, `justtext/assets/fonts/` will fall back to a system font. Add the `pixelpurl.ttf` file into `assets/fonts/` if you want the pixel font used by the project.

---

## License & Contributing

This project is a personal project. If you plan to contribute, please open issues / PRs in the repository. Include a short description of the change and tests where appropriate.

---