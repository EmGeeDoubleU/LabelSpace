import subprocess
import time

def start_yabai() -> None:
    command = ["/opt/homebrew/bin/yabai", "--verbose"]
    subprocess.Popen(command) # this will open the socket for yabai in the background so that the rest of the script doesnt get held up

def run_yabai() -> None:
    command = ["/opt/homebrew/bin/yabai", "-m", "query", "--spaces"]
    print(f"running command {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True)
    print("stdout:",result.stdout)
    print("stderr:", result.stderr)


if __name__ == '__main__':
    start_yabai()
    time.sleep(1) # wait a second for the socket to spin up
    run_yabai()