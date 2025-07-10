import subprocess
import time
import json
import rumps
from pathlib import Path

# ⬇️ PyObjC imports to make window stay on top
import objc
from Cocoa import NSWindow

# Config file
CONFIG_PATH = Path.home() / ".labelspace.json"

# Defaults
DEFAULT_ICON = "⚪️"
DEFAULT_LABEL = "Unlabeled"

# Label presets for dropdown
LABEL_PRESETS = [
    "School",
    "Projects",
    "Work",
    "Fun",
    "Browsing",
    "Writing"
]

# Emoji + color icons
ICON_OPTIONS = {
    "📚 Book": "📚",
    "🧪 Lab": "🧪",
    "💼 Work": "💼",
    "🎮 Gaming": "🎮",
    "🌐 Internet": "🌐",
    "📝 Writing": "📝",
    "🎧 Music": "🎧",
    "📊 Charts": "📊",
    "🧠 Brain": "🧠",
    "📺 Media": "📺",
    "🟢 Green": "🟢",
    "🔴 Red": "🔴",
    "🔵 Blue": "🔵",
    "🟡 Yellow": "🟡",
    "🟣 Purple": "🟣",
    "⚪️ Gray": "⚪️"
}

# Load/save config
def load_config():
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    return {}

def save_config(data):
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f, indent=2)

# Get yabai space info
def run_yabai():
    command = ["/opt/homebrew/bin/yabai", "-m", "query", "--spaces"]
    while True:
        result = subprocess.run(command, capture_output=True, text=True)
        if not result.stderr:
            return json.loads(result.stdout)
        subprocess.Popen(["/opt/homebrew/bin/yabai", "--verbose"])
        time.sleep(1)

# Get current space ID
def get_current_space_id(spaces):
    for space in spaces:
        if space.get("has-focus"):
            return str(space.get("id"))
    return None

# Main app class
class LabelSpaceApp(rumps.App):
    def __init__(self):
        super().__init__("LabelSpace", icon=None)
        self.config = load_config()
        self.last_space_id = None
        self.timer = rumps.Timer(self.update_label, 0.5)
        self.timer.start()

        # Label picker menu
        self.label_menu = rumps.MenuItem("Label current space", callback=None)
        for preset in LABEL_PRESETS:
            self.label_menu.add(rumps.MenuItem(preset, callback=self.set_label_preset))
        self.label_menu.add(rumps.MenuItem("Other...", callback=self.set_label_custom))

        # Icon picker menu
        self.icon_menu = rumps.MenuItem("Pick space icon", callback=None)
        for label, emoji in ICON_OPTIONS.items():
            self.icon_menu.add(rumps.MenuItem(f"{emoji} {label.split(' ', 1)[-1]}", callback=self.set_icon))

        self.menu = [self.label_menu, self.icon_menu]

    def update_label(self, _):
        spaces = run_yabai()
        current_id = get_current_space_id(spaces)
        if not current_id:
            self.title = "?"
            return

        self.last_space_id = current_id

        # Set safe defaults
        self.config.setdefault(current_id, {})
        self.config[current_id].setdefault("label", DEFAULT_LABEL)
        self.config[current_id].setdefault("icon", DEFAULT_ICON)
        save_config(self.config)

        label = self.config[current_id]["label"]
        icon = self.config[current_id]["icon"]
        self.title = f"{icon} {label}"

    def set_label_preset(self, sender):
        if not self.last_space_id:
            return
        self.config[self.last_space_id].setdefault("icon", DEFAULT_ICON)
        self.config[self.last_space_id]["label"] = sender.title
        save_config(self.config)
        self.update_label(None)

    def set_label_custom(self, _):
        if not self.last_space_id:
            return

        window = rumps.Window(
            message="Enter custom label:",
            title="Label This Space",
            default_text="",
            ok="OK",
            cancel="Cancel"
        )
        window.width = 300
        window.height = 40
        window.icon = None  # Hide rocket

        # Force window to float above other apps
        try:
            nswin = window._nswindow
            nswin.setLevel_(NSWindow.NSFloatingWindowLevel)
        except Exception:
            pass

        response = window.run()
        if response.clicked and response.text.strip():
            self.config[self.last_space_id].setdefault("icon", DEFAULT_ICON)
            self.config[self.last_space_id]["label"] = response.text.strip()
            save_config(self.config)
            self.update_label(None)

    def set_icon(self, sender):
        if not self.last_space_id:
            return
        emoji = sender.title.split()[0]
        self.config[self.last_space_id].setdefault("label", DEFAULT_LABEL)
        self.config[self.last_space_id]["icon"] = emoji
        save_config(self.config)
        self.update_label(None)

# Run the app
if __name__ == "__main__":
    LabelSpaceApp().run()

