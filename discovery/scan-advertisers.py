from bluepy import btle
 
class ScanDelegate(btle.DefaultDelegate):
    def __init__(self, params):
        btle.DefaultDelegate.__init__(self)
        # ... initialise here

    def handleScan(self, dev, isNewDev, isNewData):
        print("dev: ",dev, ", isNewDev: ",isNewDev,", isNewData: ",isNewData)

print("btle version:")
print(btle.sys.version)
print(btle.sys.version_info)
dev = btle.Scanner()
dev.withDelegate( ScanDelegate('params') )
scanEntries = dev.scan(10)

#d.connectable
#d.getValue
#d.rssi
#  d.addr
#d.dataTags
#d.getValueText
#d.scanData                   
#d.addrType
#d.getDescription
#d.iface
#d.updateCount
# d.addrTypes
#d.getScanData
#d.rawData

flags_bits = 'rrrHCNGL'
print("                         RSSI         16b Services               TX Power")
print("     Address       Type   dBm    Flags Inc  Comp        Name     dBm")
for de in scanEntries :
    name = de.scanData.get(9)
    if name :
        name = name.decode()
    else :
        name = ""
    flags = de.scanData.get(1)
    if flags :
        sflags = ''
        flags = int(flags[0])
        for i in range(8) :
            bit = 1 << (7-i)
            if bit & flags :
                sflags += flags_bits[i]
            else :
                sflags += ' '
        flags = sflags
    else :
        flags = '        '
    inc16s = de.scanData.get(2)
    if inc16s :
        inc16s = "%02X%02X"%(inc16s[1],inc16s[0])
        if len(inc16s) > 4 :
            inc16s += "+"
    else :
        inc16s = "    "
    c16s = de.scanData.get(3)
    if c16s :
        c16s = "%02X%02X"%(c16s[1],c16s[0])
        if len(c16s) > 4 :
            c16s += "+"
    else :
        c16s = "    "
    txp = de.scanData.get(10)
    if None != txp :
        txp = "%3d"%(txp[0])
    else :
        txp = "   "
    type = de.addrType
    if de.connectable :
        type = type.upper()
    print("%s %s %4d %s %s %s %15s %s"%(de.addr,type,de.rssi,flags,inc16s,c16s,name,txp))

l = []
for de in scanEntries :
    l.append(de)
