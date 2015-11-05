import argcomplete
import argparse
from conductr_cli.sandbox_common import CONDUCTR_DEV_IMAGE, HOST_IP
from conductr_cli import sandbox_run, sandbox_stop


def build_parser():
    # Main argument parser
    parser = argparse.ArgumentParser('sandbox')
    subparsers = parser.add_subparsers(title='commands',
                                       help='Use one of the following sub commands')

    # Sub-parser for `run` sub-command
    run_parser = subparsers.add_parser('run',
                                       help='Run ConductR sandbox cluster',
                                       usage='%(prog)s IMAGE_VERSION [ARGS]',
                                       formatter_class=argparse.RawTextHelpFormatter)
    run_parser.add_argument('image_version',
                            nargs='?',
                            help='Version of the ConductR docker image to use.\n'
                                 'To obtain the current version and additional information, please visit the \n'
                                 'http://www.typesafe.com/product/conductr/developer page on Typesafe.com.')
    run_parser.add_argument('-r', '--conductr-role',
                            dest='conductr_roles',
                            action='append',
                            nargs='*',
                            default=[],
                            help='Set additional roles allowed by each ConductR node. Defaults to [].',
                            metavar='')
    run_parser.add_argument('-d', '--debug-port',
                            type=int,
                            default=5005,
                            help='Debug port to be made public by each of the ConductR containers. Defaults to 5005.',
                            metavar='')
    run_parser.add_argument('-e', '--env',
                            dest='envs',
                            action='append',
                            default=[],
                            help='Set additional environment variables for each ConductR container. Defaults to [].',
                            metavar='')
    run_parser.add_argument('-i', '--image',
                            default=CONDUCTR_DEV_IMAGE,
                            help='Docker image to use.\n'
                                 'Defaults to `{}`.'.format(CONDUCTR_DEV_IMAGE),
                            metavar='')
    run_parser.add_argument('-l', '--log-level',
                            default='info',
                            help='Log level of ConductR which can be one of `debug`, `info`, `warning`. '
                                 'Defaults to `info`.\n'
                                 'You can observe ConductRs logging via the `docker logs` command. \n'
                                 'For example `docker logs -f cond-0` will follow the logs of the first '
                                 'ConductR container.',
                            metavar='')
    run_parser.add_argument('-n', '--nr-of-containers',
                            type=int,
                            default=1,
                            help='Number of ConductR nodes. Defaults to 1.',
                            metavar='')
    run_parser.add_argument('-p', '--port',
                            dest='ports',
                            action='append',
                            type=int,
                            default=[],
                            help='Set additional ports to be made public by each of the ConductR containers.',
                            metavar='')
    features = ['visualization', 'logging', 'monitoring']
    run_parser.add_argument('-f', '--feature',
                            dest='features',
                            action='append',
                            default=[],
                            help='Features to be enabled.\n'
                                 'Available features: ' + ', '.join(features),
                            choices=features,
                            metavar='')
    run_parser.set_defaults(func=sandbox_run.run)

    # Sub-parser for `debug` sub-command
    debug_parser = subparsers.add_parser('debug',
                                         help='Not supported. Use `sbt-conductr-sandbox` instead')
    debug_parser.set_defaults(func='debug')

    # Sub-parser for `stop` sub-command
    stop_parser = subparsers.add_parser('stop',
                                        help='Stop ConductR sandbox cluster')
    stop_parser.set_defaults(func=sandbox_stop.stop)

    return parser


def run():
    # Validate HOST_IP
    if not HOST_IP:
        return
    # Parse arguments
    parser = build_parser()
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    # Print help or execute subparser function
    if vars(args).get('func') is None:
        parser.print_help()
    # Exit with sandbox debug error message
    elif vars(args).get('func') == 'debug':
        parser.exit('Debugging a ConductR cluster is not supported by the `conductr-cli`.\n'
                    'Use the sbt plugin `sbt-conductr-sandbox` instead.')
    # Validate image_version
    elif vars(args).get('func').__name__ == 'run' and not args.image_version:
        parser.exit('The version of the ConductR Docker image must be set.\n'
                    'Please visit https://www.typesafe.com/product/conductr/developer '
                    'to obtain the current version information.')
    # Call sandbox function
    else:
        args.func(args)


if __name__ == '__main__':
    run()
