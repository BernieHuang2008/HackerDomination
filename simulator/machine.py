import os
import io
import tarfile
import yaml
import docker


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


def config_machine(container_id, config):
    def bash_run(command):
        print(container.exec_run(["/bin/bash", "-c", command]))

    container = client.containers.get(container_id)

    # init users
    users = config["users"]
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
    tar_stream = io.BytesIO()
    with tarfile.open(fileobj=tar_stream, mode="w") as tar:
        tar.add("game/machines/{}/vm/files/".format(config["host"]["IPv3"]), arcname=".")
    tar_stream.seek(0)
    container.put_archive("/", tar_stream)

    # Init file permission
    for perm in config["files"]["permission"]:
        for fpath in config["files"]["permission"][perm]:
            bash_run(f"chmod {perm} {fpath}")


def start_machine(ipv3, port=10122):
    os.system(f"ssh-keygen -R [localhost]:{str(port)}")

    with open("game/machines/{}/vm/config.yaml".format(ipv3)) as f:
        config = yaml.safe_load(f)

    container_id = run(config["machine"], {22: port}, config["host"])

    config_machine(container_id, config)

    return container_id


def stop_machine(container_id):
    client = docker.from_env()
    container = client.containers.get(container_id)
    container.stop()
    container.remove()


def check(container_id):
    container = client.containers.get(container_id)
    exit_code, output = container.exec_run("/game/checker.sh")

    return exit_code == 0
