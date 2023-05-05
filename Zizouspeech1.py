from functools import partial
import os
from signal import pause
import time

#import playsound
from pygame import mixer
import speech_recognition as sr
from gtts import gTTS
from kivy.app import App
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, BooleanProperty, ListProperty
from kivy.uix.widget import Widget
from kivy.core.audio import SoundLoader
from kivy.config import Config
from kivy.base import EventLoop
from kivy.uix.spinner import Spinner
from language import lang, values
from kivy.uix.popup import Popup
from kivy.uix.behaviors import FocusBehavior
from kivy.lang import Builder
#config('input', 'mouse', 'mouse, disable_multitouch')


#Builder.load_file('zizoutalk.kv')
class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior,
                                  RecycleGridLayout):
    ''' Adds selection and focus behaviour to the view. '''
    pass

class SelectableButton(RecycleDataViewBehavior, Button):
    index =  None
    selected=BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        return super(SelectableButton, self).refresh_view_attrs(rv, index, data)
#class TouchInput(Widget):
    def on_touch_down(self, touch):
        return super().on_touch_down(touch)
        if touch.button == "right":
            print('right click ')
            pos = super(SelectableButton, self).to_local(*self._long_touch_pos, relative=True)
            self.show_cut_copy_paste(pos, EventLoop.window, mode='paste')
    def apply_selection(self, rv, index, is_selected):
        #return super().apply_selection(rv, index, is_selected)
        self.selected= is_selected
class SpeeZizou(BoxLayout):
    data = ListProperty([])
    entry = ObjectProperty()
    language = ObjectProperty()
    #txt=ObjectProperty()
    pause=False
    
    def __init__(self, **kwargs):
        super(SpeeZizou, self).__init__(**kwargs) 
        self.data = [{'text': str(x)} for x in lang]
        #self.data = [{'text': str(x), 'on_release': partial(self.butt, x)} for x in values]
        #self.choose_language(value)
    def speak(self):
        self.languages= self.language.text
        self.txt = self.entry.text
        #self.tts = gTTS(text=self.txt, lang=self.languages)
        if self.languages == "english":
            self.tts = gTTS(text=self.txt, lang="en")
        elif self.languages == "french":
            self.tts = gTTS(text=self.txt, lang="fr")
        elif self.languages == "german":
            self.tts = gTTS(text=self.txt, lang="de")
        elif self.languages == "spanish":
            self.tts = gTTS(text=self.txt, lang="es")
        elif self.languages == "russian":
            self.tts = gTTS(text=self.txt, lang="ru")
        elif self.languages == "Arabic":
            self.tts = gTTS(text=self.txt, lang="ar")
        self.filename= "txt.mp3"
        self.tts.save(self.filename)
        
        #playsound.playsound(filename)
        #sound = SoundLoader.load(filename)
        #if sound:
            #sound.play()
        mixer.init()
        mixer.music.load(self.filename)
        mixer.music.play()
    
    #def choose_language(self, value):
        #if value == "English":
            #self.tts.lang=("en")
    def pauses(self): 
            #self.ttxt=self.txt.text
            if mixer.music.get_busy():
                mixer.music.pause()
                self.ids.tx.source="images/play-button.png"
            else:
                mixer.music.unpause()
                self.ids.tx.source="images/pause.png"

    def stop(self):
        mixer.music.stop()
    def open_popup(self):
        the_popup = CustomPopup()
        the_popup.open()
    #def pipop(self):
        #self._popup =Popup(title='load file', content=RecycleView(data=root.data))
                            
        #self._popup.open()
    def butt(self,x):
        #self.languages= self.language.text
        
        
        print('clicked',x , "not")
        print("hello")
        
class CustomPopup(Popup):
    
    data = ListProperty([])    
    #entry_tx = diz.ids["entry_text"]
    language = ObjectProperty()
    #entr = ObjectProperty()
    
    def __init__(self, **kwargs):
        super(CustomPopup, self).__init__(**kwargs)
        SpeeZizou()
        self.data = [{'text': str(x), 'on_release': partial(self.butt, x)} for x in values]
        
    def butt(self,x):
        #self.languages= self.language.text
        
        
        print('clicked',x , "not")
        print("hello")
        #if self.languages == "english":
            #self.tts = gTTS(text=self.txt, lang="en")   
class ZizouTalk(App):
    def build(self):
        return SpeeZizou()

if __name__=="__main__":
    ZizouTalk().run()
