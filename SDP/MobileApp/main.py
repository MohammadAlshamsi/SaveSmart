from kasa.discover import Discover
from kasa.smartplug import SmartPlug
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen,ScreenManager
from kivymd.uix.label import MDLabel
from kivymd.uix.picker import MDDatePicker,MDTimePicker
from kivymd.app import MDApp
from kivy.properties import ObjectProperty
from kivymd.uix.list import OneLineAvatarIconListItem, OneLineListItem, ThreeLineListItem, TwoLineListItem
from decimal import Decimal
from matplotlib.pyplot import text
from paramiko import sftp, sftp_client
from pyemvue import PyEmVue, device
import datetime
import asyncio
import sys
import os
import paramiko
from enum import Enum
from kivymd.uix.card import MDCard
from kivy.core.text import Label, LabelBase
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar
import threading
import csv



KIVY_FONTS = [
    {
        "name": "RobotoCondensed",
        "fn_regular": "fonts/RobotoCondensed-Light.ttf",
        "fn_bold": "fonts/RobotoCondensed-Regular.ttf",
        "fn_italic": "fonts/RobotoCondensed-LightItalic.ttf",
        "fn_bolditalic": "fonts/RobotoCondensed-Italic.ttf"
    }
]
    
for font in KIVY_FONTS:
    LabelBase.register(**font)

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

global z
z = 0


def greedy_algo(mystuff, limit):

    # Copy the dictionary to work on duplicate
    copy_stuff = dict(mystuff)
    # Initialize an output list
    outlist = []

    def keywithmaxval(d):
     #a) create a list of the dict's keys and values; 
     #b) return the key with the max value  
        v=list(d.values())
        k=list(d.keys())
        return k[v.index(max(v))]


    def greedy_grab(mydict):
        result = []
        total = 0
        while total <= limit and len(mydict) > 0:
            maxkey=keywithmaxval(mydict)
            result.append(maxkey)
            total += mydict[maxkey]
            del mydict[maxkey]
        return result

    def update_dict(mydict, mylist):
        for i in mylist:
            del mydict[i]
        return mydict     

    while len(copy_stuff) > 0:
        outlist.append(greedy_grab(copy_stuff))


    return outlist


class Page1(Screen):
    mdlistid = ObjectProperty()
    elempower = ObjectProperty()
    elemcount = ObjectProperty()
    def create_new_item(self,*args):
        x = 0
        i = 0
        global wt
        global val
        val = []
        wt = []
        plugs = asyncio.run(Discover.discover())
        devices = vue.get_devices()
        usage_over_time, start_time = vue.get_chart_usage(devices[1].channels[0], datetime.datetime.now(datetime.timezone.utc)-datetime.timedelta(minutes=5), datetime.datetime.now(datetime.timezone.utc), scale=Scale.MINUTE.value, unit=Unit.KWH.value)
        print(x)
        for addr, dev in plugs.items():
            asyncio.run(dev.update())
            x = x + dev.emeter_realtime["power"]
            item = ThreeLineListItem(text=dev.alias, secondary_text= "Current Reading: {:.2f}".format(dev.emeter_realtime['power'] / 100) + " kW",tertiary_text= addr)
            item.bind(on_release= self.mycallback)
            self.mdlistid.add_widget(item)
            val.append(str(dev.alias))
            wt.append(int(dev.emeter_realtime['power'])) 
            item = TwoLineListItem(text= devices[i].device_name, secondary_text= "Current Reading: " + str(usage_over_time[3]) + "kW")
            item.bind(on_release=self.mycallback)
            self.mdlistid.add_widget(item)
            self.ids['elempower'].subtext = "{:.2f}".format(dev.emeter_realtime['power'] / 100) + " kW"
            i = i + 1
            self.ids['elemcount'].subtext = str(i)
            global output
            output = {}
            for key in val:
                for val in wt:
                    output[key] = val
                    wt.remove(val)
                    break
            print(output)
    def change_page(self,*args):
        self.manager.current = 'page2'
    def mycallback(self, instance):
        z=instance.tertiary_text
        p = SmartPlug(str(z))
        asyncio.run(p.update())
        current_power = "{:.2f}".format(p.emeter_realtime["power"] / 100)
        today_average = "{:.2f}".format(p.emeter_today)
        month_average = "{:.2f}".format(p.emeter_this_month)
        plug_name = p.alias
        print(p)
        reference = self.manager.get_screen("page2")
        reference.ids.plug_name.text = plug_name
        reference.ids.test.text = "Go back"
        reference.ids.current_power.text = "Current Power"
        reference.ids.current_power.subtext = current_power + " kWh"
        reference.ids.today_power.text = "Today's average" 
        reference.ids.today_power.subtext = today_average + " kWh"
        reference.ids.monthly_power.text = "Monthy average"
        reference.ids.monthly_power.subtext = month_average + " kWh"
        reference.ids.status.text = "Status "
        if p.is_on == True:
            reference.ids.status.subtext = "On"
            #reference.ids.status.on_press = asyncio.run(p.turn_off())
        else:
            reference.ids.status.subtext = "Off"
            #reference.ids.status.on_press = asyncio.run(p.turn_on())
        self.change_page()


    def show_date_picker(self):
        today_date = datetime.datetime.now()
        date_dialog = MDDatePicker(year=today_date.year, month=today_date.month, day=today_date.day)
        date_dialog.bind(on_save = self.on_save)
        date_dialog.open()
    def on_save(self,instance,value,date_range):
        self.ids['date_button'].text = str(value)
        global chosen_date
        chosen_date = value
        print(chosen_date)
    def show_time_picker(self):
        today_date = datetime.datetime.now()
        time_dialog = MDTimePicker()
        time_dialog.set_time(today_date)
        time_dialog.bind(time=self.get_time)
        time_dialog.open()
    def get_time(self, instance, time):
        self.ids['time_button'].text = str(time)
        global chosen_time
        chosen_time = time
        print(chosen_time)
    



    def get_predictions(self, *args):
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect('127.0.0.1', username='mohad', password='Moh123123!')
            stdout = client.exec_command('python C:/Users/mohad/SDP/pipeline.py', get_pty= True)[1]
            print('Neural Network AI pipeline executed!')
            for line in stdout:
                print(line)
            sftp_client = client.open_sftp()
            remote_file = sftp_client.open('C:/Users/mohad/SDP/predictions.csv')
            try:
                reader = csv.reader(remote_file)
                data = list(reader)
                for date, value in data:
                    item = TwoLineListItem(text=value + ' kWh', secondary_text=date)
                    self.predictlistid.add_widget(item)
            finally:
                client.close()
            exit_status = stdout.channel.recv_exit_status()
            if exit_status == 0:
                print("Output Received!")
            else:
                print("Error", exit_status)
            client.close()

    def get_recommendations(self, *args):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect('127.0.0.1', username='mohad', password='Moh123123!')
        sftp_client=client.open_sftp()
        remote_file = sftp_client.open('C:/Users/mohad/SDP/predictions.csv', 'r')
        print("File Opened!")
        try:
            reader = csv.reader(remote_file)
            data = list(reader)
            chosen_timing = datetime.datetime.combine(chosen_date, chosen_time)
            for date, value in data:
                timing = chosen_timing - datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
                if timing <= datetime.timedelta(seconds=3600):
                    bigger_date = date
                    knapsack_size = value
                    break
            device_list = greedy_algo(output, int(knapsack_size))
            for device in device_list:
                for item in device:
                    item = OneLineListItem(text=str(device))
                    self.recommend_list.add_widget(item)

        finally:
            remote_file.close() 
class Page2(Screen):
    pass
class SM(ScreenManager):
    pass

class MainApp(MDApp):
    def build(self):
        self.title='SaveSmart'
        self.icon = "images/logo.png"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        menu_items = [{"text": f"Item {i}"} for i in range(5)]
        self.menu = MDDropdownMenu(
            items=menu_items,
            width_mult=4,
        )
        self.menu.bind(on_release=self.menu_callback)
        Builder.load_file('app.kv')
        return SM()
    
    def callback(self, button):
        self.menu.caller = button
        self.menu.open()
        
    def menu_callback(self, menu, item):
        self.menu.dismiss()
        Snackbar(text=item.text).open()

MainApp().run()