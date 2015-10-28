from expyrimenter.core import Shell, Executor
from pathlib import Path


class LogDownloader:
    def __init__(self, launcher_host, master, dir_exp,
                 slaves=None,
                 local_root='/tmp/logs',
                 executor=None):
        """
        :param str dir_exp: Relative to home folder
        """
        self._local_root = local_root
        self.executor = executor if executor else Executor()

        self._cmd_tpl = "ssh {} 'cd {}; tar cjf - {}' | " \
                "tar xjkf - -C %s/{}" % local_root

        self._download_list = [{
            'host': launcher_host,
            'rmt_root': '/home/hadoop/%s/remote_launcher' % dir_exp,
            'rmt_files': 'experiment*.log',
            'title': 'experiment.log',
            'lcl_dir': 'launcher'
        }, {
            'host': master,
            'rmt_root': '/home/hadoop/hibench/hibench',
            'rmt_files': 'report',
            'title': 'output folder',
            'lcl_dir': 'hibench'
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
                'rmt_root': '/home/hadoop/%s/outputs' % dir_exp,
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
        for _dir in (d['lcl_dir'] for d in self._download_list):
            if _dir != '.':
                path = '{}/{}'.format(self._local_root, _dir)
                Path(path).mkdir(parents=True)
