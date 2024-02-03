import os
import io
import tarfile
import yaml
import docker
import time


client = docker.from_env()
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
        container.exec_run(["/bin/bash", "-c", command])

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
        tar.add("game/machines/{}/vm/files/".format(config["IPv3"]), arcname=".")
    tar_stream.seek(0)
    container.put_archive("/", tar_stream)


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
