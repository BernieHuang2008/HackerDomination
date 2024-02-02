import os
import docker


def run(image: str, ports: dict):
    client = docker.from_env()
    container = client.containers.run(image, detach=True, ports=ports)
    return container.id


def start_machine(ipv3, port=10122):
    os.system(f"ssh-keygen -R localhost:{str(port)}")
    container_id = run(f"berniehuang2008/hackerdomination:{ipv3}", {22: port})
    return container_id


def stop_machine(container_id):
    client = docker.from_env()
    container = client.containers.get(container_id)
    container.stop()
    container.remove()
