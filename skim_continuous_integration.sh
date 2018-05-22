#!/bin/bash
echo "stopping systemd_monitor.service"
systemctl stop systemd_monitor.service
echo "stopping skim.service"
systemctl stop skim
echo "Running git pull"
cd /opt/skim/
/usr/bin/git pull
/usr/bin/git reset --hard master
/usr/bin/git pull
echo "starting systemd_monitor.service"
systemctl start systemd_monitor.service
