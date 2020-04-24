from bluepy import btle
 
class MyDelegate(btle.DefaultDelegate):
    def __init__(self, params):
        btle.DefaultDelegate.__init__(self)
        # ... initialise here

    def handleNotification(self, cHandle, data):
        print("cHandle: ",cHandle, ", data: ",data);
        # ... perhaps check cHandle
        # ... process 'data'

print("btle version:")
print(btle.sys.version)
print(btle.sys.version_info)
print("Connecting...")
#dev = btle.Peripheral("00:0b:57:93:36:19")
dev = btle.Peripheral("51:20:39:38:17:41",addrType='random')
#dev = btle.Peripheral("00:0b:57:ef:33:ca")
stat = dev.status()
print("Connected to %s (%s), security level %s"%(dev.addr,dev.addrType,stat['sec']))
dev.setDelegate( MyDelegate('params') )
#dev.setSecurityLevel('medium')

print("Services...")
for svc in dev.services:
    print(str(svc))
max = 0

desc = dev.getDescriptors()
chars = dev.getCharacteristics()

combined = []
while 1 :
    if len(chars) and len(desc) :
        if chars[0].handle < desc[0].handle :
            combined.append(chars.pop(0))
        else :
            combined.append(desc.pop(0))
    elif len(chars) :
        combined.append(chars.pop(0))
    elif len(desc) :
        combined.append(desc.pop(0))
    else : break

last_ch = None
ch_read = None
ch_write = None
ch_indicate = None
ccc_indicate = None

for attr in combined :
    if btle.Descriptor == type(attr) :
        if btle.UUID(0x2901) == attr.uuid :
            s = ", %s"%(attr.read().decode())
            if 'Read' == s[2:] :
                ch_read = last_ch
            elif 'Write'== s[2:] :
                ch_write = last_ch
            elif 'Notify' == s[2:] :
                ch_notify = last_ch
            elif 'Indicate' == s[2:] :
                ch_indicate = last_ch
                ccc_indicate = last_ccc
        else :
            s = ''
            if btle.UUID(0x2902) == attr.uuid :
                last_ccc = attr
        print("  ",attr," handle: %04x%s"%(attr.handle,s))
    else :
        last_ch = attr
        print(attr,"handle: %04x, properties: %s"%(attr.handle,attr.propertiesToString()))

if ccc_indicate :
    print('Writing CCC')
    ccc_indicate.write(b'\x02',1)
    
if ch_write :
    print('Writing')
    ch_write.write(b'Hello, World',1)

if ch_read :
    print('Reading')
    res = ch_read.read()
    print('Read "%s"'%(res.decode()))

print(dev.status())
dev.disconnect()
