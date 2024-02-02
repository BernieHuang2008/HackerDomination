import os, sys
import docker
import subprocess


def run(image: str, ports: dict):
    client = docker.from_env()
    container = client.containers.run(image, detach=True, ports=ports)
    return container.id


def start_machine(user, ipv3, port=10122):
    os.system(f"ssh-keygen -R localhost:{str(port)}")
    container_id = run(f"berniehuang2008/hackerdomination:{ipv3}", {22: port})

    # Open a new shell/cmd window and run the SSH command
    if sys.platform == "win32":
        subprocess.Popen(
            f'start cmd /k "ssh {user}@localhost -p {str(port)} && docker stop {container_id} && exit"',
            shell=True,
        )


if __name__ == "__main__":
    start_machine("guest", "zer.09a.ple")
