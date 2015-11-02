from conductr_cli import conduct_url, validation
import requests


@validation.handle_connection_error
@validation.handle_http_error
def unload(args):
    """`conduct unload` command"""

    path = 'bundles/{}'.format(args.bundle)
    url = conduct_url.url(path, args)
    response = requests.delete(url)
    validation.raise_for_status_inc_3xx(response)

    if args.verbose:
        validation.pretty_json(response.text)

    print('Bundle unload request sent.')
    print('Print ConductR info with: conduct info{}'.format(args.cli_parameters))
