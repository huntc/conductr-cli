import os
from conductr_cli import terminal, validation
from conductr_cli.exceptions import DockerMachineError
from subprocess import CalledProcessError


@validation.handle_docker_machine_error
def resolve_default_ip():
    def resolve():
        try:
            return with_docker_machine()
        except FileNotFoundError:
            try:
                return with_boot2docker()
            except FileNotFoundError:
                try:
                    return with_hostname()
                except CalledProcessError:
                    return '127.0.0.1'

    return os.getenv('CONDUCTR_IP', resolve())


def with_docker_machine():
    output = terminal.docker_machine_ip('default')
    if output:
        return output
    else:
        raise DockerMachineError('docker-machine host is not running.')


def with_boot2docker():
    return terminal.boot2docker_ip()


def with_hostname():
    return terminal.hostname()

