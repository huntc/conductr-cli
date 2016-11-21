# FileNotFoundError is only available on > python 3.3
NOT_FOUND_ERROR = getattr(__builtins__, 'FileNotFoundError', OSError)


class AmbiguousDockerVmError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class DockerMachineNotRunningError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class DockerMachineCannotConnectToDockerError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class VBoxManageNotFoundError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class MalformedBundleError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class BundleResolutionError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class MalformedBundleUriError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class BintrayResolutionError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class InsecureFilePermissions(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class WaitTimeoutError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class InsufficientMemory(Exception):
    def __init__(self, memory_required, memory_free):
        self.memory_required = memory_required
        self.memory_free = memory_free

    def __str__(self):
        return repr("Insufficient memory: Required: {}, Free: {}".format(self.memory_required, self.memory_free))
