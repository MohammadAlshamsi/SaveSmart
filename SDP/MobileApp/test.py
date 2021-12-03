from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager

Builder.load_string("""
<User>:
    username:username
    user_label:user_label
    but_1:but_1
    # cols: 1
    Label:
        id: user_label
        font_size: 30
        color: 0.6, 0.6, 0.6, 1
        text_size: self.width, None
        halign: 'center'
        text:'Enter username below'

    TextInput:
        id: username
        font_size: 30
        pos_hint:{"x":0.3,"y":0.25}
        size_hint: 0.4, 0.07
        color: 0.6, 0.6, 0.6, 1
        text_size: self.width, None
        halign: 'center'

    Button:
        id: but_1
        font_size: 20
        pos_hint:{"x":0.3,"y":0.15}
        size_hint: 0.4, 0.07
        text: 'Get username'
        on_press:
            root.save_username()
            root.set_username()
            root.manager.current = 'get_user'

<GetUser>:
    load_username:load_username
    user_label:user_label
    but_1:but_1
    # cols: 1
    Label:
        id: user_label
        font_size: 30
        color: 0.6, 0.6, 0.6, 1
        text_size: self.width, None
        halign: 'center'
        text:'Received username from previous page'

    TextInput:
        id: load_username
        font_size: 30
        pos_hint:{"x":0.3,"y":0.25}
        size_hint: 0.4, 0.07
        color: 0.6, 0.6, 0.6, 1
        text_size: self.width, None
        halign: 'center'
        disabled:True

    Button:
        id: but_1
        font_size: 20
        pos_hint:{"x":0.3,"y":0.15}
        size_hint: 0.4, 0.07
        text: 'Go back to username page'
        on_press:
            root.manager.current = 'user'
""")


class User(Screen):

    def save_username(self):
        print('saved: ', self.username.text)

    def set_username(self):  # <--- Asign the name here
        screens = App.get_running_app().root.screens
        other_screen = None
        text = ""
        for screen in screens:
            if screen.name == "user":
                text = screen.username.text
            elif screen.name == "get_user":
                other_screen = screen

        other_screen.load_username.text = text


class GetUser(Screen):
    pass


sm = ScreenManager()
sm.add_widget(User(name='user'))
sm.add_widget(GetUser(name='get_user'))


class UserName(App):

    def build(self):
        return sm


if __name__ == '__main__':
    UserName().run()