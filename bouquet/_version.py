
MAJOR = 0
MINOR = 3
MICRO = 0
RELEASE = True

__version__ = '%d.%d.%d' % (MAJOR, MINOR, MICRO)

if not RELEASE:
    __version__ += '.dev0'
