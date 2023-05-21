from pytube import YouTube
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.uix.label import Label
from kivymd.uix.textfield import MDTextField
from kivy.uix.textinput  import TextInput
from kivy.uix.image import Image
from kivy.uix.button import Button
from functools import partial
from kivy.uix.dropdown import DropDown
from kivy.core.window import Window
import re


Window.size=(600,700)

class MyApp(MDApp):
    
    def getLinkInfo(self,event,layout):
        self.link=self.linkinput.text
        self.checklink=re.match("^https://www.youtube.com/.*",self.link)
        print(self.checklink)
        
        if self.checklink:
            self.errorLabel.text=""
            self.errorLabel.pos_hint={'center_x':0.5,'center_y':20}
            try:
                self.yt=YouTube(self.link)
                self.titleLabel.text=str(self.yt.title) 
                self.titleLabel.pos_hint={'center_x':0.5,'center_y': 0.4}
                
                self.viewsLabel.text="Views : "+str(self.yt.views) 
                self.viewsLabel.pos_hint={'center_x':0.5,'center_y': 0.35}
                
                self.lengthLabel.text="Length : "+str(self.yt.length) 
                self.lengthLabel.pos_hint={'center_x':0.5,'center_y': 0.30}
                
                self.downloadButton.text="Download"
                self.downloadButton.pos_hint={'center_x':0.5,'center_y': 0.15}
                self.downloadButton.size_hint=(.3,.1)
                
                self.video=self.yt.streams.filter(file_extension='mp4').order_by('resolution').desc()
                print(self.video)
                
                self.dropDown=DropDown()
                
                for video in self.video:
                    btton=Button(text=video.resolution,size_hint=(None,None),height=30)
                    btton.bind(on_release=lambda btton:self.dropDown.select(btton.text))
                    self.dropDown.add_widget(btton)
                
                self.main_button=Button(text='144p',size_hint=(None, None),pos=(350,65),height=50)
                
                self.main_button.bind(on_release=self.dropDown.open)
                
                self.dropDown.bind(on_select=lambda instance,x:setattr(self.main_button,'text',x))
                
                layout.add_widget(self.main_button)     

                print('LENGTH  :  '+str(self.yt.length))
                print('PUBLISH_DATE  :  '+str(self.yt.publish_date))
                print('TITLE  :  '+str(self.yt.title))
                print('VIEWS  :  '+str(self.yt.views))
                print('thumbnail_url  :  '+str(self.yt.thumbnail_url))
                print(dir(self.yt))
            except:
                self.errorLabel.text="Network Error or Something went wrong!"
                self.errorLabel.pos_hint={'center_x':0.5,'center_y':0.4}

        else:
            self.errorLabel.text="Invalid or Empty Link"
            self.errorLabel.pos_hint={'center_x':0.5,'center_y':0.4}

    
    def download(self,event,layout):
        self.ys=self.yt.streams.filter(file_extension='mp4').filter(res=self.main_button.text).first()
        print("Downloading")
        self.ys.download()
        print("Download Complete")
    
        
    def build(self):
        layout=MDRelativeLayout(md_bg_color=[248/255,200/255,220/255])
        
        self.img=Image(source='youtube.png',size_hint=(0.5,0.5),pos_hint={'center_x': 0.5,'center_y': 0.90})
        
        self.youtubelink=Label(text="Enter YouTube link to Download",pos_hint={'center_x': 0.5,'center_y': 0.75},size_hint=(1,1),font_size=20,color=(1,0,0)) 
        
        self.linkinput=TextInput(text='',pos_hint={'center_x': 0.5,'center_y': 0.65},
                                 size_hint= (1,None),
                                 height=48,font_size=29,
                                 foreground_color=(0,0.5,0),
                                 font_name="Comic")
        self.linkbutton=Button(text="Get Link",
                               pos_hint={'center_x': 0.5,'center_y': 0.5},
                               size_hint=(.2,.1),
                               font_size=24,
                               font_name="Comic",
                               background_color=[0,1,0])
        
        self.linkbutton.bind(on_press=partial(self.getLinkInfo,layout))
        
        self.titleLabel=Label(text="",pos_hint={'center_x': 0.5,'center_y': 20},
                              size_hint=(1,1),font_size=20)
        
        self.viewsLabel=Label(text="",pos_hint={'center_x': 0.5,'center_y': 20},
                              size_hint=(1,1),font_size=20)
        
        self.lengthLabel=Label(text="",pos_hint={'center_x': 0.5,'center_y': 20},
                              size_hint=(1,1),font_size=20)
        
        
        self.downloadButton=Button(pos_hint={'center_x': 0.5,'center_y': 20},
                                   size_hint=(.2,.1),
                                #    font_name="Comic",
                                   bold=True,
                                   font_size=24,
                                   background_color=(0,1,0))
        
        self.downloadButton.bind(on_press=partial(self.download,layout))
        
        self.errorLabel=Label(text='',
                              pos_hint={'center_x': 0.5,'center_y': 20},
                              size_hint=(1, 1),
                              font_size=20,
                              color=(1,0,0)
                              )
        
        layout.add_widget(self.img)
        layout.add_widget(self.youtubelink)
        layout.add_widget(self.linkinput)
        layout.add_widget(self.linkbutton)
        layout.add_widget(self.titleLabel)
        layout.add_widget(self.viewsLabel)
        layout.add_widget(self.lengthLabel)
        layout.add_widget(self.downloadButton)
        layout.add_widget(self.errorLabel)
        
        return layout
    
    
if __name__ == '__main__':
    MyApp().run()