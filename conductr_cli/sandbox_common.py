from conductr_cli import host, terminal


HOST_IP = host.resolve_default_ip()
CONDUCTR_NAME_PREFIX = 'cond-'
CONDUCTR_PORTS = { 5601,  # conductr-kibana bundle
                   9004,  # ConductR internal akka remoting
                   9005,  # ConductR controlServer
                   9006,  # ConductR bundleStreamServer
                   9200,  # conductr-elasticsearch bundle
                   9999 } # visualizer bundle
CONDUCTR_DEV_IMAGE = 'typesafe-docker-registry-for-subscribers-only.bintray.io/conductr/conductr'
LATEST_CONDUCTR_VERSION = '1.0.12'


def resolve_running_docker_containers():
    """Resolve running docker containers.
       Return the running container names (e.g. cond-0) in ascending order"""
    container_ids = terminal.docker_ps(filter = 'name={}'.format(CONDUCTR_NAME_PREFIX))
    container_names = [terminal.docker_inspect(id, '{{.Name}}')[1:] for id in container_ids]
    return sorted(container_names)