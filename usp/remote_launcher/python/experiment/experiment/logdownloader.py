from expyrimenter.core import Shell, Executor
from pathlib import Path


class LogDownloader:
    def __init__(self, launcher_host, master,
                 slaves=None,
                 local_root='/tmp/logs',
                 executor=None):
        self._local_root = local_root
        self.executor = executor if executor else Executor()

        self._cmd_tpl = "ssh {} 'cd {}; tar cjf - {}' | " \
                "tar xjkf - -C %s/{}" % local_root

        self._download_list = [{
            'host': launcher_host,
            'rmt_root': '/home/hadoop/exp04/remote_launcher',
            'rmt_files': 'experiment.log',
            'title': 'experiment.log',
            'lcl_dir': 'launcher'
        }]
        for host in slaves + [master]:
            self._download_list.extend([{
                'host': host,
                'rmt_root': '/home/hadoop/spark/spark/logs',
                'rmt_files': '*',
                'title': 'spark logs',
                'lcl_dir': 'spark-logs/' + host
            }, {
                'host': host,
                'rmt_root': '/home/hadoop/hadoop/hadoop/logs',
                'rmt_files': '*',
                'title': 'hadoop logs',
                'lcl_dir': 'hadoop-logs/' + host
            }, {
                'host': host,
                'rmt_root': '/home/hadoop/exp04/outputs',
                'rmt_files': '*',
                'title': 'output folder',
                'lcl_dir': '.'
            }])

    def download(self):
        self._check_dir()
        for d in self._download_list:
            cmd = self._cmd_tpl.format(d['host'], d['rmt_root'],
                                       d['rmt_files'], d['lcl_dir'])
            title = 'download {} from {}'.format(d['title'], d['host'])
            shell = Shell(cmd, stdout=True, title=title)
            self.executor.run(shell)

    def _check_dir(self):
        """Target dir must not exist. If it does, throws FileExistsError"""
        root = Path(self._local_root)
        root.mkdir(parents=True)
        for dir in [d['lcl_dir'] for d in self._download_list]:
            if dir != '.':
                path = '{}/{}'.format(self._local_root, dir)
                Path(path).mkdir(parents=True)
