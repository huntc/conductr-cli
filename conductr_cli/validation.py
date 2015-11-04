import json
import sys
import urllib
import arrow
import os

from pyhocon.exceptions import ConfigException
from requests import status_codes
from requests.exceptions import ConnectionError, HTTPError
from urllib.error import URLError
from zipfile import BadZipFile
from conductr_cli import terminal
from conductr_cli.exceptions import DockerMachineError, Boot2DockerError
from subprocess import CalledProcessError


def error(message, *objs):
    """print to stderr"""
    print('ERROR: {}'.format(message.format(*objs)), file=sys.stderr)


def warning(message, *objs):
    print('WARNING: {}'.format(message.format(*objs)), file=sys.stdout)


def connection_error(err):
    error('Unable to contact ConductR.')
    error('Reason: {}'.format(err.args[0]))
    error('Make sure it can be accessed at {}'.format(err.request.url))


def pretty_json(s):
    s_json = json.loads(s)
    print(json.dumps(s_json, sort_keys=True, indent=2, separators=(',', ': ')))


def handle_connection_error(func):
    def handler(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ConnectionError as err:
            connection_error(err)  # ConnectionError doesn't have an args property

    # Do not change the wrapped function name,
    # so argparse configuration can be tested.
    handler.__name__ = func.__name__

    return handler


def handle_http_error(func):
    def handler(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPError as err:
            error('{} {}', err.response.status_code, err.response.reason)
            if err.response.text != '':
                error(err.response.text)

    # Do not change the wrapped function name,
    # so argparse configuration can be tested.
    handler.__name__ = func.__name__

    return handler


def handle_invalid_config(func):
    def handler(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ConfigException as err:
            error('Unable to parse bundle.conf.')
            error('{}.', err.args[0])

    # Do not change the wrapped function name,
    # so argparse configuration can be tested.
    handler.__name__ = func.__name__

    return handler


def handle_no_file(func):
    def handler(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except urllib.error.HTTPError as err:
            error('Resource not found: {}', err.url)
        except URLError as err:
            error('File not found: {}', err.args[0])

    # Do not change the wrapped function name,
    # so argparse configuration can be tested.
    handler.__name__ = func.__name__

    return handler


def handle_bad_zip(func):
    def handler(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BadZipFile as err:
            error('Problem with the bundle: {}', err.args[0])

    # Do not change the wrapped function name,
    # so argparse configuration can be tested.
    handler.__name__ = func.__name__

    return handler


def raise_for_status_inc_3xx(response):
    """
    raise status when status code is 3xx
    """

    response.raise_for_status()
    if response.status_code >= 300:
        raise HTTPError(status_codes._codes[response.status_code], response=response)  # FIXME: _codes is protected


def handle_docker_vm_error(func):
    def handler(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except DockerMachineError:
            error('Docker VM has not been started.')
            error('Use `docker-machine start default` to start the VM.')
        except Boot2DockerError:
            error('Docker VM has not been started.')
            error('Use `boot2docker up` to start the VM.')

    # Do not change the wrapped function name,
    # so argparse configuration can be tested.
    handler.__name__ = func.__name__

    return handler


def handle_docker_errors(func):
    def resolve_envs():
        env_lines = []
        try:
            env_lines = terminal.docker_machine_env('default')
            print("Retrieved docker environment variables with `docker-machine env default`")
        except FileNotFoundError:
            try:
                env_lines = terminal.boot2docker_shellinit()
                print('Retrieved docker environment variables with `boot2docker shellinit`')
                warning('boot2docker is deprecated. Upgrade to docker-machine.')
            except FileNotFoundError:
                return []
        return [resolve_env(line) for line in env_lines if line.startswith('export')]
    def resolve_env(line):
        key = line.partition(' ')[-1].partition('=')[0]
        value = line.partition(' ')[-1].partition('=')[2].strip('"')
        return key, value
    def set_env(key, value):
        print('Set environment variable: {}="{}"'.format(key, value))
        os.environ[key] = value
    def handler(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except CalledProcessError:
            print('Docker could not connect to the docker VM.')
            print('It looks like the docker environment variables are not set. Let me try to set them..')
            [set_env(env[0], env[1]) for env in resolve_envs()]
            try:
                terminal.docker_ps()
                print('The Docker environment variables have been set for this command.')
                warning('To set the docker environment variables for each terminal session follow the instructions of the command:')
                warning('`docker-machine env default`')
                print('Continue processing..')
                return func(*args, **kwargs)
            except CalledProcessError:
                error('Docker could not be configured automatically.')
                error('Please set the docker environment variables.')
        except FileNotFoundError:
            error('`docker` command has not been found.')
            error('The sandbox need Docker to run the ConductR nodes in virtual containers.')
            error('Please install Docker first: https://www.docker.com')

    # Do not change the wrapped function name,
    # so argparse configuration can be tested.
    handler.__name__ = func.__name__

    return handler


def format_timestamp(timestamp, args):
    date = arrow.get(timestamp)

    if args.date and args.utc:
        return date.to('UTC').strftime('%Y-%m-%dT%H:%M:%SZ')
    elif args.date:
        return date.to('local').strftime('%c')
    elif args.utc:
        return date.to('UTC').strftime('%H:%M:%SZ')
    else:
        return date.to('local').strftime('%X')
