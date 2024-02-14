import os
import io
import tarfile
import yaml
import docker
import threading


try:
    client = docker.from_env()
except Exception:
    print("\033[91mError: Docker is not running.\033[0m")
    print("\033[91m       Please start Docker manually.\033[0m")
    exit(1)

if "HackerDominGame" in [network.name for network in client.networks.list()]:
    client.networks.get("HackerDominGame").remove()
network = client.networks.create("HackerDominGame", driver="bridge")


def run(image: str, ports: dict, host: dict):
    container = client.containers.run(
        image,
        detach=True,
        ports=ports,
        hostname=host["Hostname"],
        network="HackerDominGame",
        name=host["IPv3"],
    )
    return container.id


def config_machine(container_id, config, update_label):
    def bash_run(command):
        res = container.exec_run(["/bin/bash", "-c", command])
        # print(command, res)

    container = client.containers.get(container_id)

    # update
    update_label("Updating \"apt\" ...")
    bash_run("apt update")

    # init tools
    update_label("Installing tools ...")
    tools = config.get("tools", [])
    for tool in tools:
        name = tool["name"]
        via = tool["via"]
        if via == "apt":
            bash_run(f"apt install -y {name}")
        if via == "apt-get":
            bash_run(f"apt-get install -y {name}")
        if via == "pip":
            bash_run(f"pip install {name}")
        if via == "pip3":
            bash_run(f"pip3 install {name}")

    # init users
    update_label("Initing user ...")
    users = config.get("users", [])
    for user in users:
        if user["name"] != "root":
            bash_run(f"useradd -ms /bin/bash {user['name']}")
        if "groups" in user:
            for group in user["groups"]:
                bash_run(f"addgroup {group}")
                bash_run(f"adduser {user['name']} {group}")
        if "password" in user:
            bash_run(f"echo '{user['name']}:{user['password']}' | chpasswd")

    # Init file
    update_label("Initing filesystem ...")
    tar_stream = io.BytesIO()
    with tarfile.open(fileobj=tar_stream, mode="w") as tar:
        tar.add(
            "game/machines/{}/vm/files/".format(config["host"]["IPv3"]), arcname="."
        )
    tar_stream.seek(0)
    container.put_archive("/", tar_stream)

    # Init file permission
    for perm in config["files"]["permission"]:
        for fpath in config["files"]["permission"][perm]:
            bash_run(f"chmod {perm} {fpath}")

    update_label("COMMAND:CLOSE")


def start_machine(ipv3, port=10122):
    os.system(f"ssh-keygen -R [localhost]:{str(port)}")

    with open("game/machines/{}/vm/config.yaml".format(ipv3)) as f:
        config = yaml.safe_load(f)

    container_id = run(config["machine"], {22: port}, config["host"])

    update_label = info_tk()
    config_machine(container_id, config, update_label)

    return container_id

def info_tk():
    import tkinter as tk

    root = tk.Tk()
    root.title("Machine Initializing ...")
    root.geometry("300x50")

    tk.Label(root, text="Progress").pack()

    label = tk.Label(root, text="Machine Initializing ...")
    label.pack()

    root.update()
    cnt = 0

    def update_label(text):
        nonlocal cnt
        cnt += 1

        if text == "COMMAND:CLOSE":
            root.destroy()
            return

        label.config(text=f"[{cnt}/4] {text}")
        root.update()

    return update_label

def stop_machine(container_id):
    client = docker.from_env()
    container = client.containers.get(container_id)
    container.stop()
    container.remove()


def check(container_id):
    container = client.containers.get(container_id)
    exit_code, output = container.exec_run("bash /game/checker.sh")

    return exit_code == 0


def init_checker(container_id):
    container = client.containers.get(container_id)
    container.exec_run("bash /game/checker_init.sh")
