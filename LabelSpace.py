import subprocess
import time
import json
import rumps


SPACE_LABELS = [
    "🟦 SCHOOL",
    "🟩 PERSONAL",
    "🟥 JOB SEARCH",
    "🟨 LASSO"
]

def start_yabai() -> None:
    command = ["/opt/homebrew/bin/yabai", "--verbose"]
    subprocess.Popen(command) # this will open the socket for yabai in the background so that the rest of the script doesnt get held up

def run_yabai() -> str:
    command = ["/opt/homebrew/bin/yabai", "-m", "query", "--spaces"]
    #print(f"running command {' '.join(command)}")
    #print("stdout:",result.stdout)
    #print("stderr:", result.stderr)
    while True:
        result= subprocess.run(command, capture_output=True, text=True)
        if not result.stderr:
            return result.stdout
        
        start_yabai()
        time.sleep(1)
    

def get_screen_index(json_output: str) -> int:
    screens = json.loads(json_output)
    for screen in screens:
        if screen.get("is-visible") :
            #print(screen.get("index"))
            return screen.get("index")
    return -1


def label_screen(index: int) -> str:
    #print(SPACE_LABELS[index-1])
    return SPACE_LABELS[index-1]



app = rumps.App("Loading...")

def update_label(_):
    json_output = run_yabai()
    current_index = get_screen_index(json_output)
    label = label_screen(current_index)
    app.title = label

timer = rumps.Timer(update_label, .05)
timer.start()

app.run()