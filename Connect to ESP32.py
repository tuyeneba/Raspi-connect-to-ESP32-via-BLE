
import bluetooth
import _thread
import time
  
def receiveMessages():
    strData = ''
    while True:
        data = sock.recv(buffSize)
        if data:
            if data == b'\r':
                print(strData)
            elif data == b'\n':
                strData = ''
            else:
                strData += data.decode('utf-8')
    
def sendMessage():
    myMess = input()
    sock.send('\n' + myMess)
  
def lookUpNearbyBluetoothDevices():
    print("Searching nearby Bluetooth devices...")
    nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True,
                                            flush_cache=True, lookup_class=False)

    print("Found {} devices".format(len(nearby_devices)))

    for scanAddr, scanName in nearby_devices:
        try:
            print("   {} - {}".format(scanAddr, scanName))
        except UnicodeEncodeError:
            print("   {} - {}".format(scanAddr, scanName.encode("utf-8", "replace")))

    
#********** Define ***********#
port = 1
buffSize = 1024
#myDevAddr = 'C8:F0:9E:A3:1B:F2'

#********** Main program ***********#

#lookUpNearbyBluetoothDevices()
while True:
    print('Please scan MAC address...')
    myDevAddr = input()
    sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    service_matches = bluetooth.find_service(address=myDevAddr)

    if len(service_matches) == 0:
        print("Couldn't find the device")
    else:
        try:
            sock.connect((myDevAddr, port))
            print('Connected')
            _thread.start_new_thread(receiveMessages,())
            #_thread.start_new_thread(sendMessage,())
            while True:
                sendMessage()
        except:
            print('Connecting failed, please try again.')
            sock.close()
sock.close()
print ("Done")
