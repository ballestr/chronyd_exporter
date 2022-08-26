#!/bin/python3
import os
import sys
import time
#import datetime
from datetime import datetime
from math import sqrt
if sys.version_info < (3, 0):
    from cStringIO import StringIO
else:
    from io import StringIO

## avoid time zone mess, always use UTC here
os.environ['TZ'] = 'Etc/UTC'
time.tzset()

# Number of seconds between updates
update_interval = 15

# metrics file to write
workfile="/var/lib/prometheus/node-exporter/rtc.prom"

def rtc_diff(rtc,offset,output,rma,rms):
  t1=time.time()
  wait=1.-(t1%1)+offset
  time_sysr=t1+wait
  time.sleep( wait )
  time_sys0=time.time()
  tstr_rtc=os.popen("hwclock -r --rtc /dev/%s --adjfile=/etc/adjtime.%s"%(rtc,rtc)).read().rstrip()
  time_rtc=datetime.strptime(tstr_rtc, '%Y-%m-%d %H:%M:%S.%f+00:00')
  time_sys1=time.time()
  print ('rtc_rtc_epoch{rtc="%s"} %.6f'%(rtc,time_rtc.timestamp()),file=output)
  ## dtr (delay from reference) jumps even more than dt0 (delay from start of measure), not helpful
  #print ("#%s %.6f %s %.6f"%(rtc,time_sysr,"dtr:",(time_rtc.timestamp()-time_sysr)) ,file=output)
  #print ('rtc_sys_dtr_seconds{rtc="%s"} %.6f'%(rtc,(time_sysr-time_rtc.timestamp())),file=output)
  print ("#%s %.6f %s %.6f"%(rtc,time_sys0,"dt0:",(time_rtc.timestamp()-time_sys0)) ,file=output)
  print ("#%s %.6f %s %s"%(rtc,time_rtc.timestamp(),tstr_rtc,time_rtc) ,file=output)
  print ("#%s %.6f %s %.6f"%(rtc,time_sys1,"dt1:",(time_sys1-time_rtc.timestamp())) ,file=output)
  print ('rtc_sys_dt0_seconds{rtc="%s"} %.6f'%(rtc,(time_sys0-time_rtc.timestamp())),file=output)
  print ('rtc_sys_dt1_seconds{rtc="%s"} %.6f'%(rtc,(time_sys1-time_rtc.timestamp())),file=output)
  print ('rtc_measure_seconds{rtc="%s"} %.6f'%(rtc,(time_sys1-time_sys0)),file=output)
  ## running moving average (RMA)
  ## with a filter for <2*sigma
  ## running moving stddev estimate
  v=time_sys0-time_rtc.timestamp()
  if rma==None :
    rma=v
    print ('#%s rma = %.6f'%(rtc,v))
  else:
    d2=(rma-v)*(rma-v)
    if rms==None :
      rms = d2*1.5 ## guess 1.5 sigma
    if ( d2 < 2*rms ):
      rma=((3-1)*rma+v)/3
      print ('rtc_sys_dtv_seconds{rtc="%s"} %.6f'%(rtc,v),file=output)
    else:
      print ('#%s  %.6f > %.6f OVER 2 SIGMA'%(rtc,abs(rma-v),2*sqrt(rms)),file=output)
      #print ('rtc_sys_dtv_seconds{rtc="%s"} %.6f'%(rtc,v),file=output)
    rms=((6-1)*rms+d2)/6
    #print ('#%s rma %.6f < %.6f'%(rtc,rma,v))
    #print ('#%s rms %.6f < %.6f'%(rtc,sqrt(rms),sqrt(d2)))
    print ('rtc_sys_dtrma_seconds{rtc="%s"} %.6f'%(rtc,rma),file=output)
    print ('rtc_sys_dtrms_seconds{rtc="%s"} %.6f'%(rtc,sqrt(rms)),file=output)
  return (rma,rms)

init=1
rtc0rma=None
rtc0rms=None
rtc1rma=None
rtc1rms=None
while True:
  output = StringIO()
  t0=time.time()
  (rtc1rma,rtc1rms)=rtc_diff("rtc1",0.900,output,rtc1rma,rtc1rms)
  (rtc0rma,rtc0rms)=rtc_diff("rtc0",0.500,output,rtc0rma,rtc0rms)
  if init==1 : 
    rtc1rma=None ## throw it away
    rtc0rma=None ## throw it away
  #print(rtc1rma)
  #print(rtc0rma)

  #print (output.getvalue())
  if init==0 : ## skip first iteration
    with open(workfile,"w") as f:
      print (output.getvalue(),file=f)
  output.close()
  init=0

  ## wait for next step, compensating for the time taken
  ## otherwise we end up with sample aliasing
  t1=time.time()
  time.sleep(update_interval-(t1-t0))

## original shell code
#echo -n "rtc0: "; hwclock -r -f /dev/rtc0 --adjfile=/etc/adjtime.rtc0
#echo -n "sys:  "; date "+%Y-%m-%d %H:%M:%S.%N"
#echo -n "rtc1: "; hwclock -r -f /dev/rtc1 --adjfile=/etc/adjtime.rtc1
#echo -n "sys:  "; date "+%Y-%m-%d %H:%M:%S.%N"
