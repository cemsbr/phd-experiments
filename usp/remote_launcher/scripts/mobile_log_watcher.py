#!/usr/bin/env python3
from expyrimenter.plugins.pushbullet import Pushbullet


filename = 'experiment.log'
timeout = 5 * 60
title = 'Experiment'
body = 'Stuck: {} not updated in 5min.'.format(filename)
Pushbullet().monitor_file(filename, timeout, title, body)
