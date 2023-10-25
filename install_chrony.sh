#!/bin/sh
install -m 0744 chronyd_exporter.py /usr/local/bin/
install -m 0644 prometheus-chronyd-exporter.service /etc/systemd/system/
install -m 0644 prometheus-chronyd-exporter.timer   /etc/systemd/system/

systemctl daemon-reload
systemctl enable  prometheus-chronyd-exporter.*
systemctl restart prometheus-chronyd-exporter.*
systemctl status  prometheus-chronyd-exporter.*
