from unittest import TestCase
from conductr_cli.test.cli_test_case import CliTestCase, strip_margin
from conductr_cli import conduct_logs

try:
    from unittest.mock import patch, MagicMock  # 3.3 and beyond
except ImportError:
    from mock import patch, MagicMock


class TestConductLogsCommand(CliTestCase):

    default_args = {
        'ip': '127.0.0.1',
        'port': '9005',
        'api_version': '1.0',
        'bundle': 'ab8f513',
        'lines': 1,
        'date': True,
        'utc': True
    }

    default_url = 'http://127.0.0.1:9005/bundles/ab8f513/logs?count=1'

    def test_no_logs(self):
        http_method = self.respond_with(text='{}')
        stdout = MagicMock()

        with patch('requests.get', http_method), patch('sys.stdout', stdout):
            conduct_logs.logs(MagicMock(**self.default_args))

        http_method.assert_called_with(self.default_url)
        self.assertEqual(
            strip_margin("""|TIME  HOST  LOG
                            |"""),
            self.output(stdout))

    def test_multiple_events(self):
        http_method = self.respond_with(text="""[
            {
                "timestamp":"2015-08-24T01:16:22.327Z",
                "host":"10.0.1.232",
                "message":"[WARN] [04/21/2015 12:54:30.079] [doc-renderer-cluster-1-akka.remote.default-remote-dispatcher-22] Association with remote system has failed."
            },
            {
                "timestamp":"2015-08-24T01:16:25.327Z",
                "host":"10.0.1.232",
                "message":"[WARN] [04/21/2015 12:54:36.079] [doc-renderer-cluster-1-akka.remote.default-remote-dispatcher-26] Association with remote system has failed."
            }
        ]""")
        stdout = MagicMock()

        with patch('requests.get', http_method), patch('sys.stdout', stdout):
            conduct_logs.logs(MagicMock(**self.default_args))

        http_method.assert_called_with(self.default_url)
        self.assertEqual(
            strip_margin("""|TIME                  HOST        LOG
                            |2015-08-24T01:16:22Z  10.0.1.232  [WARN] [04/21/2015 12:54:30.079] [doc-renderer-cluster-1-akka.remote.default-remote-dispatcher-22] Association with remote system has failed.
                            |2015-08-24T01:16:25Z  10.0.1.232  [WARN] [04/21/2015 12:54:36.079] [doc-renderer-cluster-1-akka.remote.default-remote-dispatcher-26] Association with remote system has failed.
                            |"""),
            self.output(stdout))

    def test_failure_invalid_address(self):
        http_method = self.raise_connection_error('test reason', self.default_url)
        stderr = MagicMock()

        with patch('requests.get', http_method), patch('sys.stderr', stderr):
            conduct_logs.logs(MagicMock(**self.default_args))

        http_method.assert_called_with(self.default_url)
        self.assertEqual(
            self.default_connection_error.format(self.default_url),
            self.output(stderr))
