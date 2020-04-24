hciconfig hci0 reset
hcitool -i hci0 cmd 0x08 0x0008 19 02 01 06 03 03 aa fe 11 16 aa fe 10 00 03 70 69 6d 79 6c 69 66 65 75 70 07 00 00 00 00 00 00
hcitool -i hci0 cmd 0x08 0x0006 a0 00 a0 00 03 00 00 00 00 00 00 00 00 07 00
hcitool -i hci0 cmd 0x08 0x000a 01
