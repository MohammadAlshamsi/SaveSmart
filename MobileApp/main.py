from kasa.discover import Discover
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen,ScreenManager
from kivymd.app import MDApp
from kivy.properties import ObjectProperty
from kivymd.uix.list import OneLineAvatarIconListItem, ThreeLineListItem, TwoLineListItem
from decimal import Decimal
from pyemvue import PyEmVue, device
import datetime
import asyncio
import sys
import os
import paramiko
from enum import Enum
class Scale(Enum):
    SECOND = '1S'
    MINUTE = '1MIN'
    MINUTES_15 = '15MIN'
    HOUR = '1H'
    DAY = '1D'
    WEEK = '1W'
    MONTH = '1MON'
    YEAR = '1Y'

class Unit(Enum):
    KWH = 'KilowattHours'
    USD = 'Dollars'
    AMPHOURS = 'AmpHours'
    TREES = 'Trees'
    GAS = 'GallonsOfGas'
    DRIVEN = 'MilesDriven'
    CARBON = 'Carbon'

vue = PyEmVue()
vue.login(username='mymalshamsi@gmail.com', password='Moh123123!')

class Page1(Screen):
    mdlistid = ObjectProperty()
    def create_new_item(self,*args):
        plugs = asyncio.run(Discover.discover())
        devices = vue.get_devices()
        usage_over_time, start_time = vue.get_chart_usage(devices[1].channels[0], datetime.datetime.now(datetime.timezone.utc)-datetime.timedelta(minutes=5), datetime.datetime.now(datetime.timezone.utc), scale=Scale.MINUTE.value, unit=Unit.KWH.value)
        for addr, dev in plugs.items():
            asyncio.run(dev.update())
            item = ThreeLineListItem(text=dev.alias, secondary_text= "Current Reading: {:.2f}".format(dev.emeter_realtime['power'] / 100) + " kW",tertiary_text= "IP Address: " + addr)
            item.bind(on_release=self.change_page)
            self.mdlistid.add_widget(item) 
            item = TwoLineListItem(text= devices[0].device_name, secondary_text= "Current Reading: " + str(usage_over_time[3]) + "kWh")
            item.bind(on_release=self.change_page)
            self.mdlistid.add_widget(item)
    def change_page(self,*args):
        self.manager.current = 'page2'
    def get_predictions(self, *args):
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect('127.0.0.1', username='mohad', password='Moh123123!')
            stdout = client.exec_command('python C:/Users/mohad/SDP/hi.py')[1]
            for line in stdout:
                print (line)
class Page2(Screen):
    pass
class SM(ScreenManager):
    pass

class MainApp(MDApp):
    def build(self):
        Builder.load_file('app.kv')
        return SM()
MainApp().run()