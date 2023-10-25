# chronyd_exporter: Chrony exporter for Prometheus node-exporter

Description: Extract chronyd metrics from `chronyc -c`

Original Author: Aanchal Malhotra <aanch...@bu.edu>

Works with chrony version 2.4 and higher

Posted original from  Watson Ladd Thu, 09 Apr 2020 https://www.mail-archive.com/chrony-users@chrony.tuxfamily.org/msg02179.html

References:
* https://listengine.tuxfamily.org/chrony.tuxfamily.org/chrony-users/2016/02/msg00003.html
* https://github.com/prometheus/node_exporter/issues/1666

This exporter, written in Python3, is made to work with the node-exporter text exporter.
I've provided systemd service and a 15s timer units.

The exporter provides all the metrics from chronyc sources, sourcestats and tracking.

Since it uses the node-exporter text, it's pretty light, so it's fine also for small SBCs.

### how to use

This exporter works with the local instance of `chronyd`, via `chronyc`. So it can be used on any host where chronyd is installed, also if it's not configured to serve on the network.

On the other side, if you want to have a good monitoring of time sources, the ideal option is to have a dedicated time monitoring physical host with low load and a stable internal clock (an SBC can do the job). In this way you can indepenently compare e.g. your local GPS stratum 1 with other off-site sources and assess the relative quality.

### Grafana panels

TBD

### Alert rules

TBD

### see also

There are other exporters for chrony
* https://github.com/SuperQ/chrony_exporter standalone exporter in go
* https://github.com/prometheus/node_exporter/blob/master/docs/TIME.md ntp collector, deprecated
* https://github.com/dmitry-ee/time_exporter seems a customised node-exporter with a dedicated chrony collector

You may also be interested in other GPS, NTP and time related things: https://github.com/ballestr/gpstime


## update 2023-10-25

Added sourcename to labels - using `chronyc sourcename <address>`.  
Does not seem to have visible impact on system load even on a low spec SBC.

## Sample output
```
root@bananapi:~/chronyd_exporter# ./chronyd_exporter.py 
# HELP chronyd_freq_skew_ppm chronyd metric for freq_skew_ppm
# TYPE chronyd_freq_skew_ppm gauge
chronyd_freq_skew_ppm{remote="GPS1",sourcename="GPS1"} 2.410000
chronyd_freq_skew_ppm{remote="PPS1",sourcename="PPS1"} 0.007000
chronyd_freq_skew_ppm{remote="127.0.0.1",sourcename="127.0.0.1"} 2000.000000
chronyd_freq_skew_ppm{remote="2606:4700:f1::1",sourcename="time.cloudflare.com"} 0.042000
chronyd_freq_skew_ppm{remote="2a03:2880:ff0c::123",sourcename="time2.facebook.com"} 0.083000
chronyd_freq_skew_ppm{remote="2a03:2880:ff09::123",sourcename="time4.facebook.com"} 0.106000
chronyd_freq_skew_ppm{remote="2a03:2880:ff0a::123",sourcename="time5.facebook.com"} 0.052000
chronyd_freq_skew_ppm{remote="85.199.214.100",sourcename="0.europe.pool.ntp.org"} 0.125000
chronyd_freq_skew_ppm{remote="144.76.59.106",sourcename="0.europe.pool.ntp.org"} 0.204000
chronyd_freq_skew_ppm{remote="2a01:260:4057:4::cc",sourcename="3.pool.chrony.eu"} 0.079000
# HELP chronyd_freq_ppm chronyd metric for freq_ppm
# TYPE chronyd_freq_ppm gauge
chronyd_freq_ppm{remote="GPS1",sourcename="GPS1"} 2.183000
chronyd_freq_ppm{remote="PPS1",sourcename="PPS1"} -0.000000
chronyd_freq_ppm{remote="127.0.0.1",sourcename="127.0.0.1"} 0.000000
chronyd_freq_ppm{remote="2606:4700:f1::1",sourcename="time.cloudflare.com"} 0.116000
chronyd_freq_ppm{remote="2a03:2880:ff0c::123",sourcename="time2.facebook.com"} 0.066000
chronyd_freq_ppm{remote="2a03:2880:ff09::123",sourcename="time4.facebook.com"} -0.013000
chronyd_freq_ppm{remote="2a03:2880:ff0a::123",sourcename="time5.facebook.com"} 0.065000
chronyd_freq_ppm{remote="85.199.214.100",sourcename="0.europe.pool.ntp.org"} -0.019000
chronyd_freq_ppm{remote="144.76.59.106",sourcename="0.europe.pool.ntp.org"} -0.039000
chronyd_freq_ppm{remote="2a01:260:4057:4::cc",sourcename="3.pool.chrony.eu"} 0.081000
# HELP chronyd_std_dev_seconds chronyd metric for std_dev_seconds
# TYPE chronyd_std_dev_seconds gauge
chronyd_std_dev_seconds{remote="GPS1",sourcename="GPS1"} 0.000737
chronyd_std_dev_seconds{remote="PPS1",sourcename="PPS1"} 0.000004
chronyd_std_dev_seconds{remote="127.0.0.1",sourcename="127.0.0.1"} 4.000000
chronyd_std_dev_seconds{remote="2606:4700:f1::1",sourcename="time.cloudflare.com"} 0.000451
chronyd_std_dev_seconds{remote="2a03:2880:ff0c::123",sourcename="time2.facebook.com"} 0.000692
chronyd_std_dev_seconds{remote="2a03:2880:ff09::123",sourcename="time4.facebook.com"} 0.000294
chronyd_std_dev_seconds{remote="2a03:2880:ff0a::123",sourcename="time5.facebook.com"} 0.000555
chronyd_std_dev_seconds{remote="85.199.214.100",sourcename="0.europe.pool.ntp.org"} 0.000072
chronyd_std_dev_seconds{remote="144.76.59.106",sourcename="0.europe.pool.ntp.org"} 0.000125
chronyd_std_dev_seconds{remote="2a01:260:4057:4::cc",sourcename="3.pool.chrony.eu"} 0.000439
# HELP chronyd_peer_status chronyd metric for peer_status
# TYPE chronyd_peer_status gauge
chronyd_peer_status{remote="GPS1",sourcename="GPS1",stratum="0",mode="reference clock"} 2.000000
chronyd_peer_status{remote="PPS1",sourcename="PPS1",stratum="0",mode="reference clock"} 4.000000
chronyd_peer_status{remote="127.0.0.1",sourcename="127.0.0.1",stratum="0",mode="server"} 1.000000
chronyd_peer_status{remote="2606:4700:f1::1",sourcename="time.cloudflare.com",stratum="3",mode="server"} 1.000000
chronyd_peer_status{remote="2a03:2880:ff0c::123",sourcename="time2.facebook.com",stratum="1",mode="server"} 2.000000
chronyd_peer_status{remote="2a03:2880:ff09::123",sourcename="time4.facebook.com",stratum="1",mode="server"} 2.000000
chronyd_peer_status{remote="2a03:2880:ff0a::123",sourcename="time5.facebook.com",stratum="1",mode="server"} 2.000000
chronyd_peer_status{remote="85.199.214.100",sourcename="0.europe.pool.ntp.org",stratum="1",mode="server"} 1.000000
chronyd_peer_status{remote="144.76.59.106",sourcename="0.europe.pool.ntp.org",stratum="2",mode="server"} 1.000000
chronyd_peer_status{remote="2a01:260:4057:4::cc",sourcename="3.pool.chrony.eu",stratum="2",mode="server"} 1.000000
# HELP chronyd_offset_seconds chronyd metric for offset_seconds
# TYPE chronyd_offset_seconds gauge
chronyd_offset_seconds{remote="GPS1",sourcename="GPS1"} 0.000922
chronyd_offset_seconds{remote="PPS1",sourcename="PPS1"} -0.000002
chronyd_offset_seconds{remote="127.0.0.1",sourcename="127.0.0.1"} 0.000000
chronyd_offset_seconds{remote="2606:4700:f1::1",sourcename="time.cloudflare.com"} 0.000534
chronyd_offset_seconds{remote="2a03:2880:ff0c::123",sourcename="time2.facebook.com"} 0.007808
chronyd_offset_seconds{remote="2a03:2880:ff09::123",sourcename="time4.facebook.com"} -0.002181
chronyd_offset_seconds{remote="2a03:2880:ff0a::123",sourcename="time5.facebook.com"} 0.004912
chronyd_offset_seconds{remote="85.199.214.100",sourcename="0.europe.pool.ntp.org"} -0.002631
chronyd_offset_seconds{remote="144.76.59.106",sourcename="0.europe.pool.ntp.org"} -0.000552
chronyd_offset_seconds{remote="2a01:260:4057:4::cc",sourcename="3.pool.chrony.eu"} -0.000286
# HELP chronyd_peer_reachable chronyd metric for peer_reachable
# TYPE chronyd_peer_reachable gauge
chronyd_peer_reachable{remote="GPS1",sourcename="GPS1",stratum="0",mode="reference clock"} 1.000000
chronyd_peer_reachable{remote="PPS1",sourcename="PPS1",stratum="0",mode="reference clock"} 1.000000
chronyd_peer_reachable{remote="127.0.0.1",sourcename="127.0.0.1",stratum="0",mode="server"} 1.000000
chronyd_peer_reachable{remote="2606:4700:f1::1",sourcename="time.cloudflare.com",stratum="3",mode="server"} 1.000000
chronyd_peer_reachable{remote="2a03:2880:ff0c::123",sourcename="time2.facebook.com",stratum="1",mode="server"} 1.000000
chronyd_peer_reachable{remote="2a03:2880:ff09::123",sourcename="time4.facebook.com",stratum="1",mode="server"} 1.000000
chronyd_peer_reachable{remote="2a03:2880:ff0a::123",sourcename="time5.facebook.com",stratum="1",mode="server"} 1.000000
chronyd_peer_reachable{remote="85.199.214.100",sourcename="0.europe.pool.ntp.org",stratum="1",mode="server"} 1.000000
chronyd_peer_reachable{remote="144.76.59.106",sourcename="0.europe.pool.ntp.org",stratum="2",mode="server"} 1.000000
chronyd_peer_reachable{remote="2a01:260:4057:4::cc",sourcename="3.pool.chrony.eu",stratum="2",mode="server"} 1.000000
# HELP chronyd_tracking_source enum for tracking_source
# TYPE chronyd_tracking_source gauge
chronyd_tracking_source{value="PPS1"} 1
# HELP chronyd_tracking_stratum chronyd metric for tracking_stratum
# TYPE chronyd_tracking_stratum gauge
chronyd_tracking_stratum 1.000000
# HELP chronyd_tracking_ref_time chronyd metric for tracking_ref_time
# TYPE chronyd_tracking_ref_time gauge
chronyd_tracking_ref_time 1698220152.765097
# HELP chronyd_tracking_system_time chronyd metric for tracking_system_time
# TYPE chronyd_tracking_system_time gauge
chronyd_tracking_system_time 0.000000
# HELP chronyd_tracking_last_offset chronyd metric for tracking_last_offset
# TYPE chronyd_tracking_last_offset gauge
chronyd_tracking_last_offset -0.000000
# HELP chronyd_tracking_rms_offset chronyd metric for tracking_rms_offset
# TYPE chronyd_tracking_rms_offset gauge
chronyd_tracking_rms_offset 0.000000
# HELP chronyd_tracking_frequency_error chronyd metric for tracking_frequency_error
# TYPE chronyd_tracking_frequency_error gauge
chronyd_tracking_frequency_error 64.815000
# HELP chronyd_tracking_frequency_residual chronyd metric for tracking_frequency_residual
# TYPE chronyd_tracking_frequency_residual gauge
chronyd_tracking_frequency_residual -0.000000
# HELP chronyd_tracking_frequency_skew chronyd metric for tracking_frequency_skew
# TYPE chronyd_tracking_frequency_skew gauge
chronyd_tracking_frequency_skew 0.007000
# HELP chronyd_tracking_root_delay chronyd metric for tracking_root_delay
# TYPE chronyd_tracking_root_delay gauge
chronyd_tracking_root_delay 0.000000
# HELP chronyd_tracking_root_dispersion chronyd metric for tracking_root_dispersion
# TYPE chronyd_tracking_root_dispersion gauge
chronyd_tracking_root_dispersion 0.000017
# HELP chronyd_tracking_update_interval chronyd metric for tracking_update_interval
# TYPE chronyd_tracking_update_interval gauge
chronyd_tracking_update_interval 16.200000
# HELP chronyd_tracking_leap_status enum for tracking_leap_status
# TYPE chronyd_tracking_leap_status gauge
chronyd_tracking_leap_status{value="Normal"} 1
```

# rtc-exporter: detailed RTC metrics for Prometheus node-exporter

Measure the offset of one or more RTC clocks compared to system clock.  
I should probably split it to a separate repo.

