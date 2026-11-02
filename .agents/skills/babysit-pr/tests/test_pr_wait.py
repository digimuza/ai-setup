import runpy
import unittest
from pathlib import Path
from unittest.mock import patch

Watcher = runpy.run_path(str(Path(__file__).parents[1] / 'scripts/pr-wait'))['Watcher']


class ReadinessTests(unittest.TestCase):
    def watcher(self, until, checks):
        with patch.object(Watcher, 'load', return_value=None):
            watcher = Watcher('example/repo', 1, until, 5)
        watcher.required = set()
        watcher.save = lambda: None
        watcher.say = lambda line: None
        watcher.fetch_checks = lambda: checks
        watcher.fetch_pr = lambda: {
            'state': 'OPEN', 'url': 'https://example.com/1',
            'baseRefName': 'sandbox', 'headRefOid': 'abc123456',
            'viewer': 'viewer', 'comments': {'nodes': []},
            'reviews': {'nodes': []}, 'reviewThreads': {'nodes': []},
            'mergeStateStatus': 'CLEAN',
        }
        return watcher

    def test_empty_checks_become_green_only_after_stable_poll(self):
        watcher = self.watcher('green', {})
        watcher.poll()
        with self.assertRaises(SystemExit) as result:
            watcher.poll()
        self.assertEqual(result.exception.code, 0)

    def test_unsuccessful_bot_cannot_make_ready(self):
        for bucket in ('fail', 'cancel', 'skipping', 'pending'):
            with self.subTest(bucket=bucket):
                watcher = self.watcher('ready', {
                    'CI': {'bucket': 'pass', 'link': ''},
                    'Greptile': {'bucket': bucket, 'link': ''},
                })
                watcher.poll()
                watcher.poll()

    def test_successful_bot_can_make_ready(self):
        watcher = self.watcher('ready', {
            'CI': {'bucket': 'pass', 'link': ''},
            'Greptile': {'bucket': 'pass', 'link': ''},
        })
        watcher.poll()
        with self.assertRaises(SystemExit) as result:
            watcher.poll()
        self.assertEqual(result.exception.code, 0)


if __name__ == '__main__':
    unittest.main()
