import os
import json
import pyglet
from pyglet.gl import *
from pyglet.window import key, mouse

# --- CONFIGURATION & SETTINGS ---
SETTINGS_FILE = "settings.json"
WORLD_FILE = "world_save.json"

default_settings = {
    "volume": 0.8,
    "sensitivity": 0.15,
    "controls": {"FORWARD": "W", "BACKWARD": "S", "LEFT": "A", "RIGHT": "D"}
}

def load_json(filepath, default):
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    return default

settings = load_json(SETTINGS_FILE, default_settings)

# --- GAME ENGINE WINDOW ---
class MinecraftClone(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Game State
        self.gamemode = "CREATIVE" # Switchable to "SURVIVAL"
        self.player_pos = [0.0, 2.0, 0.0]
        self.player_rot = [0.0, 0.0]
        
        # World Data Structure (Preloaded with Chaos Cubed placeholders)
        # 1 = Sulfur Block, 2 = Cinnabar, 3 = Potent Sulfur
        self.world = load_json(WORLD_FILE, {
            "0,0,0": 1, "1,0,0": 2, "0,0,1": 3, "0,1,0": 1
        })
        
        # Input state tracker
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        
        pyglet.clock.schedule_interval(self.update, 1.0 / 60.0)
        self.init_gl()

    def init_gl(self):
        glClearColor(0.5, 0.69, 1.0, 1.0) # Sky Blue
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)

    def save_progress(self):
        with open(WORLD_FILE, "w") as f:
            json.dump(self.world, f)
        print("Progress saved locally.")

    # --- INPUT AND SETTINGS HANDLERS ---
    def on_mouse_motion(self, x, y, dx, dy):
        sens = settings["sensitivity"]
        self.player_rot[0] += dx * sens
        self.player_rot[1] += dy * sens
        self.player_rot[1] = max(-90, min(90, self.player_rot[1]))

    def on_key_press(self, symbol, modifiers):
        # Toggle Gamemode
        if symbol == key.G:
            self.gamemode = "SURVIVAL" if self.gamemode == "CREATIVE" else "CREATIVE"
            print(f"Gamemode changed to: {self.gamemode}")
        # Manual Save Hook
        elif symbol == key.F5:
            self.save_progress()

    # --- GAME LOOP & UPDATE ---
    def update(self, dt):
        # Core player physics, movement logic, and gamemode speed handling goes here
        pass

    def draw_block(self, x, y, z, block_type):
        # OpenGL Immediate mode rendering logic for individual block vertices
        pass

    def on_draw(self):
        self.clear()
        # Matrix setups and scene rendering pipeline
        pass

if __name__ == "__main__":
    window = MinecraftClone(width=854, height=480, caption="Chaos Cubed Project", resizable=True)
    pyglet.app.run()
