import numpy as np
import matplotlib.pyplot as plt

f = open("/data/lab8_5.64-8.04-1.52.mbd")
#mumuderler
dic = {}
list_key = []
for i in f:
    data = i.split(',')
    timeStamp = data[0]
    sensor_mac = data[1]
    transmitter_mac = data[2]
    rssi = data[3]

    thistuple = (sensor_mac,transmitter_mac,rssi)
    dic[timeStamp] = thistuple[0],thistuple[1],thistuple[2]

f.close()

def toFigure(rssi):
    int_rssi = [int(i) for i in rssi]
    max_rssi = max(int_rssi)
    min_rssi = min(int_rssi)
    axe_x = np.arange(min_rssi,max_rssi,1)
    axe_y = [0]*len(axe_x)

    j = 0
    for i in axe_x:
        if i in int_rssi:
            axe_y[j] = int_rssi.count(i)
            j += 1
        else:
            j += 1
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    ax.bar(axe_x,axe_y)
    plt.show()

devices = [('001583e5b269','f963ea9bb3ea'),('001583e5a5bd','f963ea9bb3ea'),('001a7dda710b','f963ea9bb3ea'),('001583e5a3c0','f963ea9bb3ea'),('001a7dda710b','e78f135624ce'),('001583e5a3c0','e78f135624ce'),('001583e5a5bd','e78f135624ce'),('001583e5b269','e78f135624ce')]
'''
def new_dic(dictionary,devices):
    dic2 = {}
    visited = []
    visited2 = []
    mac_tuple_list = []
    mac_tuple_list2 = []

    for k in devices:
        for i in dictionary:
            data2 = dictionary[i]
            mac_tuple = data2[0],data2[1]
            mac_tuple_list.append(mac_tuple)

            if k not in visited2:
                visited2.append(k)
                for i in dictionary:
                    mac_tuple_list2.append(data2[2])
            if k in mac_tuple_list:
                visited.append(k)
                toFigure(mac_tuple_list2)
'''
            


listofTuples = []
visitedTuples = []
rssi_list = []
def new_dic(dictionary,devices):
    for i in dictionary:
        data = dictionary[i]
        mac = data[0],data[1]
        rssi = data[2]
        mac_rssi = (mac,rssi)
        listofTuples.append(mac_rssi)
    for k in devices:
        for j in listofTuples:
            if k == j[0]:
                rssi_list.append(j[1])
        toFigure(rssi_list)

new_dic(dic,devices)
