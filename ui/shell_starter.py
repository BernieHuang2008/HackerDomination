import tkinter as tk
from tkinter import ttk
import yaml
import subprocess
import threading

shells = {
    "PLee-Unhackable": ["zer.09a.ple"],
}

activated = set()

def init(s):
    """
    Initialize the shell starter.
    """
    global shells
    shells = s

def render():
    """
    Render the shell starter.
    """
    root = tk.Tk()
    root.title("Shell Starter")
    root.geometry("200x200")
    root.resizable(False, False)

    # Choose: which shell
    tk.Label(root, text="Choose a shell:").pack()
    combo = ttk.Combobox(root, values=list(shells.keys()))
    combo.pack()

    # Input: Username
    tk.Label(root, text="Username:").pack()
    username = tk.Entry(root)
    username.pack()

    # Input: Password
    tk.Label(root, text="Password:").pack()
    password = tk.Entry(root)
    password.pack()

    # Error message
    global err
    err = tk.Label(root, text="", fg="red")
    err.pack()

    # Start button
    tk.Button(root, text=">_", command=lambda: start(combo, username, password)).pack()

    # Mainloop
    root.mainloop()


def start(combo, username, password):
    """
    Start the shell.
    """
    shell = combo.get()
    user = username.get()
    pwd = password.get()

    shellcfg = shells[shell]
    shell_ip = shellcfg[0]

    h = hash((shell, user, pwd))

    if h in activated:
        err.config(text="Shell already activated.")
        return
    
    if not checkpwd(shell_ip, user, pwd):
        err.config(text="Invalid username/password.")
        return
    
    activated.add(h)

    # Activate machine
    start_subprocess(["python", f"game/machines/{shell_ip}/start.py", user, pwd], lambda: activated.remove(h))

def start_subprocess(cmd, callback):
    """
    Start a subprocess.
    """
    def run_subprocess():
        subp = subprocess.Popen(cmd, stderr=open("log/vshell-error.log", "w"))
        subp.wait()
        callback()

    thread = threading.Thread(target=run_subprocess)
    thread.start()
    

def checkpwd(ip, user, pwd):
    """
    Check if the username/password is correct.
    """
    with open(f"game/machines/{ip}/vm/os.yaml") as os:
        os = yaml.safe_load(os)
    
    users = os["user"]["users"]

    if user in users and users[user]["password"] == pwd:
        return True


if __name__ == "__main__":
    render()
