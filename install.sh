install -m 0744 chronyd_exporter.py /usr/local/bin/
install -m 0644 prometheus-chronyd-exporter.service /etc/systemd/system/
install -m 0644 prometheus-chronyd-exporter.timer   /etc/systemd/system/

install -m 0744 rtc_metrics_rma.py /usr/local/bin/
install -m 0644 prometheus-rtc-exporter.service     /etc/systemd/system/

systemctl daemon-reload
systemctl enable --now prometheus-chronyd-exporter.*
systemctl status prometheus-chronyd-exporter.*
systemctl enable --now prometheus-rtc-exporter.*
systemctl status prometheus-rtc-exporter.*
