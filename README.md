# chronyd_exporter: Chrony exporter for Prometheus node-exporter

Description: Extract chronyd metrics from chronyc -c

Original Author: Aanchal Malhotra <aanch...@bu.edu>

Works with chrony version 2.4 and higher

Posted original from  Watson Ladd Thu, 09 Apr 2020 https://www.mail-archive.com/chrony-users@chrony.tuxfamily.org/msg02179.html

References
* https://listengine.tuxfamily.org/chrony.tuxfamily.org/chrony-users/2016/02/msg00003.html                                                                                                            
* https://github.com/prometheus/node_exporter/issues/1666                                                                                                                                             


# rtc-exporter: detailed RTC metrics for Prometheus node-exporter

Measure the offset of one or more RTC clocks compared to system clock

## update 2023-10-25

Added sourcename to labels - using `chronyc sourcename <address>`.  
Does not seem to have visible impact on system load even on a low spec SBC.

# Also

See also https://github.com/ballestr/gpstime
