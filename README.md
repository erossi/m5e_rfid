# m5e_rfid
ThingMagic M5e RFID UHF reader/writer

A connection example

# Boot 04
> ff00041d0b
ff1404000007102300010000032014100701070209000000105251

# Version 03
> FF 00 03 1D 0c
ff1403000007102300010000032014100701070209000000105bd1

# Set the Region 97 (EU=0x02)
> FF 01 97 02 4B BE (datasheet errato)
> 019702
ff0197024bbf
ff00970000779e

# Get the tag protocol (63)
> 0063
ff00631d6c
ff0263000000002143

# Set Current Tag Protocol (93) (GEN2 0x0005)
> 02930005
ff02930005517d
ff00930000371a

# and re-get the protocol
> 0063
ff00631d6c
ff0263000000052146

# Get the Read TX Power
> 016201
ff016201bebc
ff076200000108fc08fc03e87ac9

# Get Antenna config
> 016101
ff016101bdbc
ff03610000010100215b

# Read a single tag
> 022103e8
ff022103e8d509
ff0e210000e200322fe20df9311328b7e3d100aad0

# Read a single tag without a tag
> 022103e8
ff022103e8d509
ff00210400b483

# Get the power mode
> 0068
ff00681d67
ff0168000000a4bf

# Set power mode (to min, it is off, but the tx still the same)
# also it consume a lot less.
> 019803
ff01980344be
ff009800008671

# and check it
> 0068
ff00681d67
ff0168000003a4bc

# re-read the tx (read) power (unchanged)
> 016201
ff016201bebc
ff0762[0000][01][08fc][08fc][03e8]7ac9

# set the tx (read) power to the minimum (03e8 from above)
> 029203e8
ff029203e842b1
ff00920000273b

# re-read the tx (read) power (changed to min)
> 016201
ff016201bebc
ff076200000103e808fc03e8fb75

# re-read the tag (with min tx pwr and min consumption) (10cm)
> 022103e8
ff022103e8d509
ff0e210000e200322fe20df9311328b7e3d100aad0

