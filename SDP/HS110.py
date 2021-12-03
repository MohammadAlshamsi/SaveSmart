import asyncio
import time
from kasa import SmartPlug
from kasa import Discover

devices = asyncio.run(Discover.discover())
for alias in devices.items():
    print(F"{alias}")