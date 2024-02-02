import sys
import tkinter as tk
from tkinter import ttk
import json
import subprocess
import simulator.machine as machine

shells = {
    "PLee-Unhackable": ["zer.09a.ple"],
}

unused_port = 10021
activated_windows = set()
activated_machines = {}


def init(s={}):
    """
    Initialize the shell starter.
    """
    global shells
    shells = s
    global unused_port, activated_windows, activated_machines
    unused_port = 10021
    activated_windows = set()
    activated_machines = {}


def render():
    """
    Render the shell starter.
    """
    try:
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

        # Error message
        global err
        err = tk.Label(root, text="", fg="red")
        err.pack()

        # Start button
        tk.Button(
            root, text=">_", command=lambda: start(combo, username)
        ).pack()

        # Submit button
        tk.Button(
            root, text="Submit", command=lambda: check(combo)
        ).pack()

        root.bind("<Destroy>", lambda _: root.quit())
        root.bind("<Escape>", lambda _: [root.destroy(), root.quit()])

        # Mainloop
        root.mainloop()
    finally:
        close()
        init()


def close():
    """
    Close the shell starter.
    """
    for ipv3, (port, container_ip) in activated_machines.items():
        machine.stop_machine(container_ip)


def start(combo, username):
    """
    Start the shell.
    """
    shell = combo.get()
    user = username.get()

    shellcfg = shells[shell]
    shell_ip = shellcfg[0]

    # Machine
    if shell_ip not in activated_machines:
        global unused_port
        unused_port += 1
        machine_port = unused_port

        container_ip = machine.start_machine(shell_ip, machine_port)
        activated_machines[shell_ip] = [machine_port, container_ip]
    else:
        machine_port, container_ip = activated_machines[shell_ip]

    # Shell
    h = hash((shell, user))

    if h in activated_windows:
        err.config(text="Shell already activated.")
        return

    if not checkpwd(shell_ip, user):
        err.config(text="Invalid user.")
        return

    activated_windows.add(h)

    # Activate shell
    if sys.platform == "win32":
        subprocess.Popen(
            f'start cmd /k "ssh {user}@localhost -p {machine_port} && exit"',
            shell=True,
        )


def check(combo):
    """
    Run checker
    """
    shell = combo.get()
    shellcfg = shells[shell]
    shell_ip = shellcfg[0]
    _, container_id = activated_machines[shell_ip]
    
    if machine.check(container_id):
        err.config(text="Passed.")
    else:
        err.config(text="Failed.")


def checkpwd(ip, user):
    """
    Check if the username/password is correct.
    """
    with open(f"game/machines/{ip}/info.json") as info:
        info = json.load(info)

    users = info["users"]

    if user in users:
        return True
