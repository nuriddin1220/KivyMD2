from pytube import YouTube
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.core.window import Window
from kivymd.uix.card import MDCard
from kivy.metrics import dp
from kivymd.uix.floatlayout import MDFloatLayout
import re
from kivy.uix.image import AsyncImage
from kivymd.uix.button import MDFlatButton,MDRaisedButton
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import StringProperty
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.filemanager import MDFileManager
import subprocess
import os

Window.size=(500,600)


def convert_duration(duration_sec):
    minutes, remaining_seconds = divmod(duration_sec, 60)
    hours, remaining_minutes = divmod(minutes, 60)
    duration = ""
    if hours > 0:
        duration += f"{hours} soat, "
    if remaining_minutes > 0:
        duration += f"{remaining_minutes} minut, "
    if remaining_seconds > 0:
        duration += f"{remaining_seconds} sekund"
    return duration.rstrip(", ")

class IconListItem(OneLineIconListItem):
    icon = StringProperty()

class MainApp(MDApp):
    title="Nuriddin's YouTube Downloader"
    selected_path=''
    def build(self):
        self.theme_cls.theme_style="Light"
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_file("youtube.kv")


    
    def filechooser(self):
        self.file_manager = MDFileManager(select_path=self.select_path)
        self.file_manager.show(os.path.expanduser("~"))
        
        
    def select_path(self,path):
        self.select_path=path
        print(path)
        self.file_manager.close()
    
    
    def search_function(self):
        link=self.root.ids.link_input.text
        checklink=re.match("^https://www.youtube.com/.*",link)
        if checklink:
            try:
                yt=YouTube(link)
                
                self.root.ids.thumb_img.source=yt.thumbnail_url
                self.root.ids.thumb_img.pos_hint={'center_x': 0.5,'top': 0.55}
                
                self.root.ids.titleLabel.text=yt.title
                self.root.ids.titleLabel.pos_hint={'center_x': 0.5,'top': 0.23}
                
                self.root.ids.lengthLabel.text=convert_duration(yt.length)
                self.root.ids.lengthLabel.pos_hint={'center_x': 0.5,'top': 0.18}
                
                streams=yt.streams.filter(file_extension='mp4')
                self.resolution_list=[item.resolution for item  in streams if item.resolution is not None]
                    
                
                self.root.ids.downloadButton.pos_hint={'right':0.5,'top': 0.1}
                
                self.root.ids.drop_item.pos_hint={'right':0.7,'top': 0.1}
                self.root.ids.drop_item.text=str(streams.get_highest_resolution().resolution)    
                
              
            except:
                print('yt something')
        else:
            print('something')
        
    def choose_resolution(self, instance):
        menu_items = [{
            "viewclass": "IconListItem",
            "icon": "video-box",
            "height": dp(56),
            "text": i,
            "on_release": lambda x=i:self.set_item(x)
            } for i in self.resolution_list]
        self.dropdown = MDDropdownMenu(
            caller=instance,
            items=menu_items,
            width_mult=4,
            top=instance.y + instance.height
        )
        self.dropdown.open() 
    def set_item(self,text_item):
        self.root.ids.drop_item.set_item(text_item)
        self.dropdown.dismiss()
        
if __name__ == '__main__':
    MainApp().run()