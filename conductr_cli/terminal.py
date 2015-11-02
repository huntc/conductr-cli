import subprocess


def docker_images(image):
    return subprocess.check_output(['docker', 'images', '--quiet', image]).strip()

def docker_pull(image):
    return subprocess.call(['docker', 'pull', image])

def docker_ps(filter = None):
    filter_arg = ['--filter', filter] if filter else []
    command = ['docker', 'ps', '--quiet'] + filter_arg
    output = subprocess.check_output(command, universal_newlines=True).strip()
    return output.splitlines()

def docker_inspect(id, format = None):
    format_arg = ['--format', format] if format else []
    command = ['docker', 'inspect'] + format_arg + [id]
    return subprocess.check_output(command, universal_newlines=True).strip()

def docker_run(optional_args, image, positional_args):
    command = ['docker', 'run'] + optional_args + [image] + positional_args
    return subprocess.call(['docker', 'run'] + optional_args + [image] + positional_args)

def docker_rm(containers):
    return subprocess.call(['docker', 'rm', '-f'] + containers)

def docker_machine_ip(vm_name):
    command = ['docker-machine', 'ip', vm_name]
    return subprocess.check_output(command, universal_newlines=True).strip()

def boot2docker_ip():
    command = ['boot2docker', 'ip']
    return subprocess.check_output(command, universal_newlines=True).strip()

def hostname():
    return subprocess.check_output(['hostname'], universal_newlines=True).strip()