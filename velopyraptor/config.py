import platform

# If true indicates 64 bit architecture, false indicates 32 bit
_64BIT = platform.architecture()[0] == '64bit'

if _64BIT:
    dtype = "uint64"
    alignment = 8
else:
    dtype = "uint32"
    alignment = 4
