#!/bin/sh
install -m 0744 rtc_metrics_rma.py /usr/local/bin/
install -m 0644 prometheus-rtc-exporter.service     /etc/systemd/system/

systemctl daemon-reload
systemctl enable  prometheus-rtc-exporter.*
systemctl restart prometheus-rtc-exporter.*
systemctl status  prometheus-rtc-exporter.*
