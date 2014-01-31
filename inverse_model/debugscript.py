import sqlite3
from matplotlib import pyplot as plt


cursor=sqlite3.connect('data.db').cursor()
##d=dict()
##for clust in range(72):
##    d[clust]=dict()
##    #for mote in ['lighta','lightb','lightc','lightd']:
##    for mote in ['nasalight3']:
##        #cursor.execute('SELECT average FROM %s WHERE unixtime>=1.338667200e+12 AND unixtime<=1.33922514e+12 AND cluster = %d' %(mote,clust))
##        #cursor.execute('SELECT average FROM %s WHERE unixtime>=1337903405000 AND unixtime<=1338534000000 AND cluster = %d' %(mote,clust))
##        cursor.execute('SELECT unixtime,average FROM %s WHERE unixtime>=1339419600000 AND unixtime<=1340240400000 AND cluster = %d' %(mote,clust))
##        d[clust][mote]=cursor.fetchall()
##        #print len(d[clust][mote])

#unixtime = [1337929200000,1338966000000]#May25toJun5
unixtime = [1339138800000,1340175600000]#Jun8toJun20
#unixtime = [1337929200000,1340262000000]#May25toJun21
#unixtime = [1339138800000,1339570800000]#Jun8toJun13
#unixtime = [1338966000000,1340175600000]#Jun5toJun20
#cursor.execute('SELECT unixtime,average FROM nasalight3 WHERE unixtime>=1339419600000 AND unixtime<=1340240400000')# AND cluster > 0')
#cursor.execute('SELECT unixtime,average FROM nasalight3 WHERE unixtime>=1339419600000 AND unixtime<=1339722000000')# AND cluster > 0')
#cursor.execute('SELECT unixtime,average FROM nasalight3 WHERE unixtime>=1339419600000 AND unixtime<=1339635600000')# AND cluster > 0')
cursor.execute('SELECT unixtime,average,light,processed FROM nasalight7 WHERE unixtime>='+str(unixtime[0])+' AND unixtime<='+str(unixtime[1])+' AND cluster > 0 AND month = 6 and day = 12')
temp = cursor.fetchall()
time = []
average = []
light = []
processed = []
for count in range(len(temp)):
    time.append(temp[count][0])
    light.append(temp[count][2])
    average.append(temp[count][1])
    processed.append(temp[count][3])
plt.figure()
plt.scatter(time,light,c='r')
#plt.scatter(time,average,c='r')
plt.scatter(time,processed,c='g')
plt.show()
plt.close()
