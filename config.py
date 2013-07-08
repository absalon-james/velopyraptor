import platform

# If true indicates 64 bit architecture, false indicates 32 bit
_64BIT = platform.architecture()[0] == '64bit'
