import sys, platform
print('Python %s [%d bit]' % (
	platform.python_version(),
	64 if sys.maxsize > 2**32 else 32
))