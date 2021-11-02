from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivymd.app import MDApp
from kivymd.uix.list import MDList, ThreeLineListItem
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
from kasa import Discover
from kasa import SmartPlug
import asyncio
from decimal import Decimal

sm = ScreenManager()


class DeviceList(MDApp):
    def build(self):
        screen = Screen()
        scroll = ScrollView()
        list = MDList()
        devices = asyncio.run(Discover.discover())
        for addr, dev in devices.items():
            asyncio.run(dev.update())
            l = ThreeLineListItem(text=dev.alias, secondary_text="Current Power: %.2f" % Decimal(dev.emeter_realtime['power_mw'] / 10)  + " mW", tertiary_text="Current Runtime: " + dev.on_since.strftime("%H:%M:%S"))
            list.add_widget(l)
        scroll.add_widget(list)
        screen.add_widget(scroll)
        return screen
            

DeviceList().run()