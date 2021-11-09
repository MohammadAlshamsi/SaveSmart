from kivy.lang import Builder
from kivy.uix.screenmanager import Screen,ScreenManager
from kivymd.app import MDApp
from kivy.properties import ObjectProperty
from decimal import Decimal
import asyncio
from kasa import Discover
from kivymd.uix.list import OneLineAvatarIconListItem, ThreeLineListItem
from pyemvue import PyEmVue
vue = PyEmVue()
vue.login(username= 'mymalshamsi@gmail.com', token_storage_file='keys.json')
customer = vue.get_customer_details()
class Page1(Screen):
    mdlistid = ObjectProperty()
    def seek_devices(self,*args):
        devices = asyncio.run(Discover.discover())
        for addr, dev in devices.items():
            asyncio.run(dev.update())
            item =ThreeLineListItem(text=dev.alias,
            secondary_text="Current Power: %.2f" % Decimal(dev.emeter_realtime['power_mw'] / 10)  + " mW",
            tertiary_text="Current Runtime: " + dev.on_since.strftime("%H:%M:%S"))
            item.bind(on_release=self.change_page)
            self.mdlistid.add_widget(item)
    def change_page(self,*args):
        self.manager.current = 'page2'
class Page2(Screen):
    pass
class SM(ScreenManager):
    pass


class MainApp(MDApp):
    def build(self):
        Builder.load_file('test.kv')
        return SM()
MainApp().run()