#!/usr/bin/env python3
#
# Description: Extract chronyd metrics from chronyc -c.
# Author: Aanchal Malhotra <aanch...@bu.edu>
#
# Works with chrony version 2.4 and higher
##
## Original from
## https://www.mail-archive.com/chrony-users@chrony.tuxfamily.org/msg02179.html
## Ref
## https://listengine.tuxfamily.org/chrony.tuxfamily.org/chrony-users/2016/02/msg00003.html
## https://github.com/prometheus/node_exporter/issues/1666

import subprocess
import sys

chrony_sourcestats_cmd = ['chronyc', '-c', 'sourcestats']
chrony_source_cmd = ['chronyc', '-c', 'sources']
chrony_tracking_cmd = ['chronyc', '-c', 'tracking']

metrics_fields = [
    "Name/IP Address",
    "NP",
    "NR",
    "Span",
    "Frequency",
    "Freq Skew",
    "Offset",
    "Std Dev"]

status_types = {'x': 0, '?': 1, '-': 2, '+': 3, '*': 4}

metrics_source = {
    "*": "synchronized (system peer)",
    "+": "synchronized",
    "?": "unreachable",
    "x": "Falseticker",
    "-": "reference clock"}

metrics_mode = {
    '^': "server",
    '=': "peer",
    "#": "reference clock"}


def get_cmdoutput(command):
    proc = subprocess.Popen(command, stdout=subprocess.PIPE)
    out, err = proc.communicate()
    return_code = proc.poll()
    if return_code:
        raise RuntimeError('Call to "{}" returned error: \
    {}'.format(command, return_code))
    return out.decode("utf-8")


def printPrometheusformat(metric, values):
    print("# HELP chronyd_%s chronyd metric for %s" % (metric, metric))
    print("# TYPE chronyd_%s gauge" % (metric))
    for labels in values:
        if labels is None:
            print("chronyd_%s %f" % (metric, values[labels]))
        else:
            print("chronyd_%s{%s} %f" % (metric, labels, values[labels]))

def printPrometheusscalar(metric, value):
    print("# HELP chronyd_%s chronyd metric for %s" %(metric, metric))
    print("# TYPE chronyd_%s gauge" %(metric))
    print ("chronyd_%s %f" % (metric, value))

def printPrometheusEnum(metric, name):
    print("# HELP chronyd_%s enum for %s" %(metric, metric))
    print("# TYPE chronyd_%s gauge" %(metric))
    print("chronyd_%s{value=\"%s\"} 1"%(metric, name))

def weight(value):
    val_int = int(value, 8)
    return bin(val_int).count('1')/8.0

def main(argv):
    peer_status_metrics = {}
    peer_reach_metrics = {}
    offset_metrics = {}
    freq_skew_metrics = {}
    freq_metrics = {}
    std_dev_metrics = {}
    chrony_sourcestats = get_cmdoutput(chrony_sourcestats_cmd)
    for line in chrony_sourcestats.split('\n'):
        if (len(line)) > 0:
            x = line.split(',')
            common_labels = "remote=\"%s\"" % (x[0])
            freq_metrics[common_labels] = float(x[4])
            freq_skew_metrics[common_labels] = float(x[5])
            std_dev_metrics[common_labels] = float(x[7])

    printPrometheusformat('freq_skew_ppm', freq_skew_metrics)
    printPrometheusformat('freq_ppm', freq_metrics)
    printPrometheusformat('std_dev_seconds', std_dev_metrics)

    chrony_source = get_cmdoutput(chrony_source_cmd)
    for line in chrony_source.split('\n'):
        if (len(line)) > 0:
            x = line.split(',')
            stratum = x[3]
            reach = x[5]
            mode = metrics_mode[x[0]]
            common_labels = "remote=\"%s\"" % (x[2])
            peer_labels = "%s,stratum=\"%s\",mode=\"%s\"" % (
                common_labels,
                stratum,
                mode,
            )
            peer_status_metrics[peer_labels] = float(status_types[x[1]])
            peer_reach_metrics[peer_labels] = weight(reach)
            offset_metrics[common_labels] = float(x[8])

    printPrometheusformat('peer_status', peer_status_metrics)
    printPrometheusformat('offset_seconds', offset_metrics)
    printPrometheusformat('peer_reachable', peer_reach_metrics)

    chrony_tracking_stats = get_cmdoutput(chrony_tracking_cmd).rstrip()
    fields = chrony_tracking_stats.split(",")
    printPrometheusEnum("tracking_source", fields[1])
    printPrometheusscalar("tracking_stratum", float(fields[2]))
    printPrometheusscalar("tracking_ref_time", float(fields[3]))
    printPrometheusscalar("tracking_system_time", float(fields[4]))
    printPrometheusscalar("tracking_last_offset" , float(fields[5]))
    printPrometheusscalar("tracking_rms_offset", float(fields[6]))
    printPrometheusscalar("tracking_frequency_error", float(fields[7]))
    printPrometheusscalar("tracking_frequency_residual", float(fields[8]))
    printPrometheusscalar("tracking_frequency_skew", float(fields[9]))
    printPrometheusscalar("tracking_root_delay", float(fields[10]))
    printPrometheusscalar("tracking_root_dispersion", float(fields[11]))
    printPrometheusscalar("tracking_update_interval", float(fields[12]))
    printPrometheusEnum("tracking_leap_status", fields[13])

if __name__ == "__main__":
    main(sys.argv[1:])
