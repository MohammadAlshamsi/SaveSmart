from kivy.lang import Builder
from kivymd.uix.screen import Screen
from kivymd.app import MDApp
from kivymd.uix.list import MDList, ThreeLineAvatarIconListItem, ThreeLineListItem, OneLineListItem
from kivy.properties import StringProperty
from kivy.uix.switch import Switch
from kasa import Discover
from decimal import Decimal
import asyncio
from pathlib import Path
#from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
#from kivymd.uix.button import MDFillRoundFlatButton

class Test(MDApp):
    def build(self):
        return Builder.load_file('test.kv')
    
    class ListWithRightSwitch(ThreeLineAvatarIconListItem):

        icon = StringProperty("android")

    def on_start(self):
        devices = asyncio.run(Discover.discover())
        for addr, dev in devices.items():
            asyncio.run(dev.update())
            self.root.ids.devices.add_widget(
            ThreeLineListItem(text=dev.alias,
             secondary_text="Current Power: %.2f" % Decimal(dev.emeter_realtime['power_mw'] / 10)  + " mW",
             tertiary_text="Current Runtime: " + dev.on_since.strftime("%H:%M:%S")
             ))            
Test().run()