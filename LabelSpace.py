import subprocess
import time
import json
SPACE_LABELS = [
    "SCHOOL",
    "JOB SEARCH",
    "LASSO",
    "PERSONAL"
]
def start_yabai() -> None:
    command = ["/opt/homebrew/bin/yabai", "--verbose"]
    subprocess.Popen(command) # this will open the socket for yabai in the background so that the rest of the script doesnt get held up

def run_yabai() -> str:
    command = ["/opt/homebrew/bin/yabai", "-m", "query", "--spaces"]
    print(f"running command {' '.join(command)}")
    result= subprocess.run(command, capture_output=True, text=True)
    #print("stdout:",result.stdout)
    #print("stderr:", result.stderr)
    while (result.stderr):
        start_yabai()
        time.sleep(1)
        run_yabai()
    return result.stdout

def get_screen_index(json_output: str) -> int:
    screens = json.loads(json_output)
    for screen in screens:
        if screen.get("is-visible") :
            print(screen.get("index"))
            return screen.get("index")
    return -1


def label_screen(index: int) -> str:
    print(SPACE_LABELS[index-1])
    return SPACE_LABELS[index-1]


if __name__ == '__main__':
    
     # wait a second for the socket to spin up
    json_output: str = run_yabai() # returns screen index as json
    current_index: int = get_screen_index(json_output) # finds the current screen
    label_screen(current_index)