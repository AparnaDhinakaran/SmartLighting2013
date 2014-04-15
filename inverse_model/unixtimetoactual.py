import matplotlib 
import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import datetime as dt
import time

n=20
duration=1000
#now=time.mktime(time.localtime())
now = 1388275200000
#insert the actual unixtimes in place of now,now+duration,n in the next line
timestamps=np.linspace(now,now+duration,n)
dates=[dt.datetime.fromtimestamp(ts) for ts in timestamps]
datenums=md.date2num(dates)
#put measured and predicted in place of values1 and values2
values1=np.sin((timestamps-now)/duration*2*np.pi)
values2=np.sin((timestamps-now)/duration*2*np.pi)*2
fig=matplotlib.pyplot.gcf()
fig, ax = plt.subplots()
fig.subplots_adjust(bottom=0.4)
xfmt = md.DateFormatter('%Y-%m-%d %H:%M')
ax.xaxis.set_major_formatter(xfmt)
ax.plot(datenums,values1,label='Measured light',linewidth=3)
ax.plot(datenums,values2,label='Predicted light',linewidth=3)
ax.set_xlabel('Time of day',fontsize=34)
ax.set_ylabel('Illuminance (lux)', fontsize=34)
for tick in ax.yaxis.get_major_ticks():
    tick.label.set_fontsize(24)
for tick in ax.xaxis.get_major_ticks():
    tick.label.set_fontsize(24)
    tick.label.set_rotation(90)
legend = ax.legend(loc='upper right')
for label in legend.get_texts():
    label.set_fontsize(32)
fig.set_size_inches(20,10.5)
plt.show()
