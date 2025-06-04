import subprocess
import time
import json

def start_yabai() -> None:
    command = ["/opt/homebrew/bin/yabai", "--verbose"]
    subprocess.Popen(command) # this will open the socket for yabai in the background so that the rest of the script doesnt get held up

def run_yabai() -> str:
    command = ["/opt/homebrew/bin/yabai", "-m", "query", "--spaces"]
    print(f"running command {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True)
    print("stdout:",result.stdout)
    print("stderr:", result.stderr)
    return result.stdout

def get_screen_index(json_output: str) -> int:
    screens = json.loads(json_output)
    for screen in screens:
        if screen.get("is-visible") :
            print(screen.get("index"))
            return screen.get("index")
    return -1

if __name__ == '__main__':
    start_yabai()
    time.sleep(1) # wait a second for the socket to spin up
    json_output = run_yabai()
    get_screen_index(json_output)