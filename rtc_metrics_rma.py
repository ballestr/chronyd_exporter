#!/bin/python3
## RTC metrics exporter
## version with Running Moving Average already calculated
## because excluding samples outside 2 sigma seems impossible to do with Prometheus rules

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
#workfile="/dev/stdout" # for test/debug

class RTC:
  def __init__(self,dev):
    self.dev=dev
    self.rma=None
    self.rms=None
    self.getname()
  def getname(self):
    try:
      with open("/sys/class/rtc/%s/name"%(self.dev)) as file :
        self.fullname=file.read().rstrip()
      self.name=self.fullname.split(None,1)[0]
      self.present=True
      print("/dev/%s is %s"%(self.dev,self.name))
    except:
      self.name=None
      self.present=False
      print("/dev/%s is %s"%(self.dev,self.name))

def rtc_diff(rtc,name,offset,output,rma,rms):
  t1=time.time()
  wait=1.-(t1%1)+offset
  time_sysr=t1+wait
  time.sleep( wait )
  time_sys0=time.time()
  tstr_rtc=os.popen("hwclock -r --rtc /dev/%s --adjfile=/etc/adjtime.%s"%(rtc,rtc)).read().rstrip()
  time_rtc=datetime.strptime(tstr_rtc, '%Y-%m-%d %H:%M:%S.%f+00:00')
  time_sys1=time.time()
  labels='rtc="%s",name="%s"'%(rtc,name)
  print ('rtc_rtc_epoch{%s} %.6f'%(labels,time_rtc.timestamp()),file=output)
  ## dtr (delay from reference) jumps even more than dt0 (delay from start of measure), not helpful
  #print ("#%s %.6f %s %.6f"%(rtc,time_sysr,"dtr:",(time_rtc.timestamp()-time_sysr)) ,file=output)
  #print ('rtc_sys_dtr_seconds{%s} %.6f'%(labels,(time_sysr-time_rtc.timestamp())),file=output)
  print ("#%s sys0:%.6f %s %.6f"%(rtc,time_sys0,"dt0:",(time_rtc.timestamp()-time_sys0)) ,file=output)
  print ("#%s rtc: %.6f str=%s v=%s"%(rtc,time_rtc.timestamp(),tstr_rtc,time_rtc) ,file=output)
  print ("#%s sys1:%.6f %s %.6f"%(rtc,time_sys1,"dt1:",(time_sys1-time_rtc.timestamp())) ,file=output)
  print ('rtc_sys_dt0_seconds{%s} %.6f'%(labels,(time_sys0-time_rtc.timestamp())),file=output)
  print ('rtc_sys_dt1_seconds{%s} %.6f'%(labels,(time_sys1-time_rtc.timestamp())),file=output)
  print ('rtc_measure_seconds{%s} %.6f'%(labels,(time_sys1-time_sys0)),file=output)
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
      print ('rtc_sys_dtv_seconds{%s} %.6f'%(labels,v),file=output)
    else:
      print ('#%s  %.6f > %.6f OVER 2 SIGMA'%(rtc,abs(rma-v),2*sqrt(rms)),file=output)
      #print ('rtc_sys_dtv_seconds{%s} %.6f'%(labels,v),file=output)
    rms=((6-1)*rms+d2)/6
    #print ('#%s rma %.6f < %.6f'%(rtc,rma,v))
    #print ('#%s rms %.6f < %.6f'%(rtc,sqrt(rms),sqrt(d2)))
    print ('rtc_sys_dtrma_seconds{%s} %.6f'%(labels,rma),file=output)
    print ('rtc_sys_dtrms_seconds{%s} %.6f'%(labels,sqrt(rms)),file=output)
  return (rma,rms)

#### main

print("Write to %s"%workfile)
#with open("/sys/class/rtc/rtc0/name") as file :
#  rtc0name=file.read().rstrip()
#with open("/sys/class/rtc/rtc1/name") as file :
#  rtc1name=file.read().rstrip()

rtc0=RTC("rtc0")
rtc1=RTC("rtc1")

init=1
rtc0rma=None
rtc0rms=None
rtc1rma=None
rtc1rms=None
while True:
  output = StringIO()
  t0=time.time()
  if (rtc1.present):
        (rtc1rma,rtc1rms)=rtc_diff("rtc1",rtc1.name,0.900,output,rtc1rma,rtc1rms)
  (rtc0rma,rtc0rms)=rtc_diff("rtc0",rtc0.name,0.500,output,rtc0rma,rtc0rms)
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
