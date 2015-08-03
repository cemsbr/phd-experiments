#!/bin/bash
rm ~hadoop/.bash_history
rm /root/.bash_history
aptitude clean
killall -9 bash
