import subprocess


def docker_images(image):
    return subprocess.check_output(['docker', 'images', '--quiet', image]).strip()


def docker_pull(image):
    return subprocess.call(['docker', 'pull', image])


def docker_ps(ps_filter=None):
    ps_filter_arg = ['--filter', ps_filter] if ps_filter else []
    command = ['docker', 'ps', '--quiet'] + ps_filter_arg
    output = subprocess.check_output(command, universal_newlines=True).strip()
    return output.splitlines()


def docker_inspect(container_id, inspect_format=None):
    format_arg = ['--format', inspect_format] if inspect_format else []
    command = ['docker', 'inspect'] + format_arg + [container_id]
    return subprocess.check_output(command, universal_newlines=True).strip()


def docker_run(optional_args, image, positional_args):
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
    return subprocess.check_output(['hostname'], universal_newlines=True).strip() # FIXME: Needs to work for Windows
