from kivy.lang import Builder
from kivymd.uix.list import OneLineListItem
from kivymd.app import MDApp
from kivy.core.audio import SoundLoader
from kivy.uix.screenmanager import Screen, ScreenManager
import os

helper_string = """
ScreenManager:
    MainScreen:
    PlayingScreen:

<MainScreen>:
    name: 'list'
    BoxLayout:
        orientation: "vertical"
        MDToolbar:
            title: "Demo music player"
        ScrollView:
            MDList:
                id: scroll
                on_touch_down: app.root.current ='controller'


<PlayingScreen>:
    name: 'controller'
    MDLabel:
        text : 'Hello world'
        halight: 'center'

"""

class MainScreen(Screen):
    pass


class PlayingScreen(Screen):
    pass


sm = ScreenManager()
sm.add_widget(MainScreen (name='list'))
sm.add_widget(PlayingScreen (name='controller'))

class MainApp(MDApp):
    def build(self):
        self.sound = None
        self.theme_cls.theme_style="Dark"
        screen = Builder.load_string(helper_string)
        return screen
        
    def on_start(self):
        for root, dirs, files in os.walk('assets'):
            for file in files:
                if file.endswith('.mp3'):
                    required_file = file
                    the_location = os.path.abspath(os.path.join(root, required_file))
                    self.root.ids.scroll.add_widget(OneLineListItem(text=the_location, 
                                                                    on_release=self.play_song))

    
    def play_song(self, onelinelistitem):
        the_song_path = onelinelistitem.text
        if self.sound:
            self.sound.stop()
        self.sound = SoundLoader.load(the_song_path)
        if self.sound:
            self.sound.play()
        print(the_song_path)

    

MainApp().run()