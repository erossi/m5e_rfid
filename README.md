# m5e_rfid
ThingMagic M5e RFID UHF reader/writer

A connection example

```
# Boot (04)
> 04
ff00041d0b
ff1404000007102300010000032014100701070209000000105251

# Get Version (03)
> 03
ff00031d0c
ff1403000007102300010000032014100701070209000000105bd1

# Set the Region 97 (EU=0x02)
> 9702
ff0197024bbf
ff00970000779e

# Get the tag protocol (63)
> 63
ff00631d6c
ff0263000000002143

# Set Current Tag Protocol (93) (GEN2 0x0005)
> 930005
ff02930005517d
ff00930000371a

# and re-get the protocol
> 63
ff00631d6c
ff0263000000052146

# Get the Read TX Power
> 6201
ff016201bebc
ff076200000108fc08fc03e87ac9

# Get Antenna config
> 6101
ff016101bdbc
ff03610000010100215b

# Read a single tag
> 2103e8
ff022103e8d509
ff0e210000e200322fe20df9311328b7e3d100aad0

# Read a single tag without a tag
> 2103e8
ff022103e8d509
ff00210400b483

# Get the power mode
> 68
ff00681d67
ff0168000000a4bf

# Set power mode (to min, it is off, but the tx still the same)
# also it consume a lot less.
> 9803
ff01980344be
ff009800008671

# and check it
> 68
ff00681d67
ff0168000003a4bc

# re-read the tx (read) power (unchanged)
> 6201
ff016201bebc
ff0762[0000][01][08fc][08fc][03e8]7ac9

# set the tx (read) power to the minimum (03e8 from above)
> 9203e8
ff029203e842b1
ff00920000273b

# re-read the tx (read) power (changed to min)
> 6201
ff016201bebc
ff076200000103e808fc03e8fb75

# re-read the tag (with min tx pwr and min consumption) (10cm)
> 2103e8
ff022103e8d509
ff0e210000e200322fe20df9311328b7e3d100aad0

# Read the EPC?
> 21 03e8 00
ff032103e800a5e8
ff0f21000000e200322fe20df9311328b7e3d100a542

# Get the Reader config (max epc lenght)
> 6a0102
ff026a01002e4e
ff036a00000100003e44

# Set the Reader config (max epc lenght) to 496 bits
> 9a 01 02 01
ff039a010201ad5c
ff009a0000a633

# Read the EPC of a locked TAG
# note that the reading is not suppose to be locked by standard,
# locking is on writing.
cmd:                28 (read memory)
Time out:           03e8
Singulation Option: 02 (select singulation on TID)
Read Membank:       01 (EPC)
Read Address:       00000002 (starting from 2 word inside the EPC memory)
Word count:         08 (16 Byte EPC lenght)
Access code:        xxxxxxxx (to be chenaged!)
Singulation addr:   00000000 (TID starting address)
Signulation lenght: 08 bit (1 byte to match to select the tag)
Singulation data:   e2 (select the tag with TID starting with e2)

> 28 03e8 02 01 00000002 08 xxxxxxxx 00000000 01 e2

```

