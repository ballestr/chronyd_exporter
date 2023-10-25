# Real Time Clocks

Sys filesystem: `/sys/class/rtc/*/name`

- `rtc_cmos 00:05` onboard standard mini-PC
- `rk808-rtc` onboard Odroid M1 (RK3568B2aarch64 Cortex-A55)
- `sunxi-rtc 1c20d00.rtc` onboard BananaPI M1+ (A20 armv7l CPU)
- `rtc-ds1307 2-0068` on DS3231 GPIO hat, mounted on the BananaPI

The metrics script `rtc_metrics_rma.py` compares the RTC with the system clock.
Looking at that over a long term (at least a few hours) allows to figure out drift and correlations with temperature etc.
This of course assuming that the system clock is well kept with UTC.

The data is written to the standard location for the node-exporter text exporter, every 15s.

## data format

`# cat /var/lib/prometheus/node-exporter/rtc.prom`
```
rtc_rtc_epoch{rtc="rtc0",name="rk808-rtc"} 1698054787.813095
#rtc0 sys0:1698054787.501549 dt0: 0.311546
#rtc0 rtc: 1698054787.813095 str=2023-10-23 09:53:07.813095+00:00 v=2023-10-23 09:53:07.813095
#rtc0 sys1:1698054787.694634 dt1: -0.118461
rtc_sys_dt0_seconds{rtc="rtc0",name="rk808-rtc"} -0.311546
rtc_sys_dt1_seconds{rtc="rtc0",name="rk808-rtc"} -0.118461
rtc_measure_seconds{rtc="rtc0",name="rk808-rtc"} 0.193085
rtc_sys_dtv_seconds{rtc="rtc0",name="rk808-rtc"} -0.311546
rtc_sys_dtrma_seconds{rtc="rtc0",name="rk808-rtc"} -0.313023
rtc_sys_dtrms_seconds{rtc="rtc0",name="rk808-rtc"} 0.001926
```

### Grafana display
RTC drift (derivative) in PPM per second, typically within -10~10 ppm range for a good RTC:
```
deriv(rtc_sys_dtrma_seconds{instance=~"$node.*"}[${interval}])*1000000
```

What is more important actually is that it does not oscillate too much: a stable drift can be compensated well by `adjtime`, but an unstable drift is pretty much hopeless.

## notes

### long time to read
Note that reading the RTC can be very slow, up to one second to wait for the clock tick, e.g.
```
# time hwclock -r --rtc /dev/rtc0 -v
hwclock from util-linux 2.37.2
System Time: 1698055073.746184
Using the rtc interface to the clock.
Assuming hardware clock is kept in UTC time.
Waiting for clock tick...
...got clock tick
Time read from Hardware Clock: 2023/10/23 09:57:55
Hw clock time : 2023/10/23 09:57:55 = 1698055075 seconds since 1969
Time since last adjustment is 1698055075 seconds
Calculated Hardware Clock drift is 0.000000 seconds
2023-10-23 09:57:54.044374+00:00

real	0m0.960s
user	0m0.001s
sys		0m0.006s
```

### large offset

If you have a very large offset (multiple of 3600), check if the RTC timezone is UTC, using `hwclock` or `timedatectl`.  
And fix it, you aren't running WindowsNT, are you? ;-)

### adjtime settings

See https://man7.org/linux/man-pages/man5/adjtime_config.5.html 

You can have a dedicated adjtime file for each RTC, like
```
root@bananapi:~# cat /etc/adjtime.rtc1 
-1.091315 1698042311 0.000000
1698042311
UTC
```

The metrics script will use it when calling `hwclock`.

And, if the RTC is not being used and updated by the NTP client, a daily cron to keep it updated, e.g.
```
root@bananapi:~# cat /etc/cron.daily/rtc1_update_drift 
#!/bin/bash
(
hwclock -v --systohc --update-drift --rtc /dev/rtc1 --adjfile=/etc/adjtime.rtc1
) | logger -t rtc
```

If the RTC is updated by the NTP client (e.g. `rtcsync` in `chrony.conf`), `adjtime` will not be able to do its job.
Ref also the 11 minute kernel time sync https://man7.org/linux/man-pages/man8/hwclock.8.html

### chronyd and multiple RTCs

It seems that chronyd is not able to use the second RTC? I have an old comment in the config file on the BananaPI:
```
# This directive enables kernel synchronisation (every 11 minutes) of the
# real-time clock. Note that it can’t be used along with the 'rtcfile' directive.
rtcsync
## do not use optional BananaPI RTC, does not work
#rtcdevice /dev/rtc1
#rtcfile /var/lib/chrony/rtc
```
