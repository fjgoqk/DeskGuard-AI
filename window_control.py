import subprocess

def cover_mode():
    script_hide = '''
    tell application "System Events"
        keystroke "h" using {command down}
        delay 0.1
        keystroke "h" using {command down}
    end tell
    '''
    subprocess.run(["osascript", "-e", script_hide], capture_output=True)

    script_vscode = '''
    tell application "Visual Studio Code"
        activate
        delay 0.2
    end tell
    '''
    subprocess.run(["osascript", "-e", script_vscode], capture_output=True)