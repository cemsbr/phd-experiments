#!/usr/bin/env python3
from expyrimenter.plugins.pushbullet import Pushbullet


filename = 'experiment.log'
minutes = 5
title = 'Experiment'
body = 'Stuck: {} not updated in {:d}min.'.format(filename, minutes)

seconds = minutes * 60
Pushbullet().monitor_file(filename, seconds, title, body)
