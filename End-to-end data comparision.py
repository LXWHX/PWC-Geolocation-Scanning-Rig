import os
import re
import json
import jsonpath
jsonloca = 'E:/4806project/raw/1666189803.json' #This is rig's data payload in json format
csvloca = 'bluetooth_le_1665098014407.csv'#This is ble payload in csv format
txtloca = 'wifidata.txt'#This is wifi paylaod in ext format
print("\n")
cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
print("----------------Begin payload analysis---------------")
print("Files in %r: %s" % (cwd, files))
file =open(csvloca,'r')
lines=file.readlines()
file.close()
row=[]
rows=[]
maccolumn=[]# colum of mac address
firstrssi=[]#colum of first seen rssi value
lastrssi=[]#colum of last seen rssi value
avgrssi=[]
for line in lines:
    row.append(line.split(','))

#print(row[0])#print 1st row
for col in row:
    maccolumn.append(eval(col[0]))
for col in row:
    firstrssi.append(eval(col[3]))
for col in row:
    lastrssi.append(eval(col[5]))
print("This is ble mac: \n")
maccolumn = maccolumn[1:] # cut first item
print(maccolumn)#
print("This is ble frssi: \n")
firstrssi = firstrssi[1:] # cut first item
print(firstrssi)#
print("This is ble lrssi: \n")
lastrssi = lastrssi[1:] # cut first item
print(lastrssi)#
print("This is average ble rssi: \n")
for i in range(len(firstrssi)):
    avgrssi.append((int(firstrssi[i])+int(lastrssi[i]))/2)
print(avgrssi)#
print("\n")
print("BLE process done!")
print("\n")

wifida = []
ssid =[]
macid =[]
wifiraw = []
wifistrength=[]
wififreq = []
file1 = open(txtloca,'r')  #open wifi data
file_data = file1.readlines() #read all lines
for row in file_data:
    tmp_list = row.split('|') #split data by |
    #tmp_list[-1] = tmp_list[-1].replace('\n',',') #去掉换行符
    wifida.append(tmp_list) #append all data in list format
for col in wifida:
    ssid.append(col[1])
for col in wifida:
    macid.append(col[2])
for col in wifida:
    wifiraw.append(col[3])
#print(wifida)#Print all wifi data
print("This is app Wifi mac: \n")
macid = macid[1:] # cut first item
print(macid)
print("This is app Wifi rssi : \n")
wifiraw = wifiraw[1:] # cut first item
for str in wifiraw:
    wifistrength.append(int(str[:-3]))

#print(wifiraw)#raw data with dBm behind
print(wifistrength)

print("\n")
print("WiFi process done!")
print("\n")
totalmac=[]
totalrssi=[]
totalmac = macid + maccolumn
totalrssi = wifistrength + avgrssi

if len(totalmac) != len(macid) + len(maccolumn):
    print("mac length of app data donot match!!!!!!!!!!!")
elif len(totalrssi) != len(wifistrength) + len(avgrssi):
    print("mac length of app data donot match!!!!!!!!!!!")
else:
    print("\n")
    print("length of total totalmac and totalrssi checked!")
    print("\n")
appdictionary = dict(zip(totalmac, totalrssi))

#file2 = open('E:/4806project/raw/634737a307b83644.json', 'r')
with open(jsonloca) as f:
  rigdatapayload = json.load(f)

print(type(rigdatapayload))  # Output: dict
print(rigdatapayload.keys())
print("This is mac in Rig's data payload mac: \n")
macraw = jsonpath.jsonpath(rigdatapayload,'$..mac') #
#print(macraw)
mac_list =[]
for ele in macraw:
    str_list = list(ele)
    str_list.insert(2, ':')
    str_list.insert(5, ':')
    str_list.insert(8, ':')
    str_list.insert(11, ':')
    str_list.insert(14, ':')
    str_2 = "".join(str_list)
    mac_list.append(str_2)
print(mac_list)
print("This is rssi in Rig's data payload rssi: \n")
rssi_list = jsonpath.jsonpath(rigdatapayload,'$..rssi_avg') #
print(rssi_list)

rigdictionary = dict(zip(mac_list, rssi_list))

# key in both dict

print ("Common mac address:")
print(appdictionary.keys() & rigdictionary.keys())

print("Uncommon mac address:")
# keys not in both dict

print(appdictionary.keys() ^ rigdictionary.keys())

# keys in rig dict but not in app dict
print("Mac address obtained in rig but not on android device:")
print(rigdictionary.keys()- appdictionary.keys())

# same signals with diff rssi value
diff = appdictionary.keys() & rigdictionary
# same signals and their value
diff_vals = [(k, appdictionary[k], rigdictionary[k]) for k in diff if appdictionary[k] != rigdictionary[k]]
same_vals = [(k, appdictionary[k], rigdictionary[k]) for k in diff if appdictionary[k] == rigdictionary[k]]
print("Same mac address with different rssi values:")
print(diff_vals)
print("Same mac address with same rssi values:")
print(same_vals)
