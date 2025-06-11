from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.slider import Slider
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
import csv
import os
from datetime import datetime
from kivy.core.audio import SoundLoader

class DabTimer(BoxLayout):
    def __init__(self, **kwargs):
        super(DabTimer, self).__init__(orientation='vertical', spacing=dp(10), padding=dp(10), **kwargs)
        self.beep = SoundLoader.load('beep.wav')
        
        # Timer display
        self.timer_label = Label(text='Ready', font_size='24sp', size_hint=(1, None), height=dp(50))
        self.add_widget(self.timer_label)

        # Material spinner
        self.add_widget(Label(text='Select Material:', size_hint=(1, None), height=dp(30)))
        self.material_spinner = Spinner(text='Quartz', values=['Quartz','Titanium','Ceramic'], size_hint=(1,None), height=dp(40))
        self.add_widget(self.material_spinner)

        # Style spinner
        self.add_widget(Label(text='Select Style:', size_hint=(1, None), height=dp(30)))
        self.style_spinner = Spinner(text='Flat Top', values=['Flat Top','Slanted','Thermal','Terp Slurper'], size_hint=(1,None), height=dp(40))
        self.add_widget(self.style_spinner)

        # Wax spinner
        self.add_widget(Label(text='Select Wax:', size_hint=(1, None), height=dp(30)))
        self.wax_spinner = Spinner(text='Shatter', values=['Shatter','Budder','Crumble','Rosin','Live Resin','Sugar'], size_hint=(1,None), height=dp(40))
        self.add_widget(self.wax_spinner)

        # Flame intensity slider
        self.add_widget(Label(text='Flame Intensity (×):', size_hint=(1, None), height=dp(30)))
        self.intensity_slider = Slider(min=0.5, max=2.0, value=1.0, step=0.1)
        self.add_widget(self.intensity_slider)
        self.int_label = Label(text=f'{self.intensity_slider.value:.1f}', size_hint=(1, None), height=dp(30))
        self.add_widget(self.int_label)
        self.intensity_slider.bind(value=lambda _,v: setattr(self.int_label, 'text', f'{v:.1f}'))

        # Buttons
        self.start_button = Button(text='Start Heat Timer', size_hint=(1,None), height=dp(40))
        self.start_button.bind(on_press=self.toggle_timer)
        self.add_widget(self.start_button)

        self.view_log_button = Button(text='View Log', size_hint=(1,None), height=dp(40))
        self.view_log_button.bind(on_press=self.show_log)
        self.add_widget(self.view_log_button)

        self.close_button = Button(text='Close App', size_hint=(1,None), height=dp(40))
        self.close_button.bind(on_press=self.close_app)
        self.add_widget(self.close_button)

        # Internal state
        self.phase = None
        self.time_left = 0
        self.heat_time = 0
        self.cool_time = 0
        self.event = None

        # Config dicts
        self.material_times = {'Quartz':30,'Titanium':45,'Ceramic':40}
        self.style_modifiers = {'Flat Top':1.0,'Slanted':0.9,'Thermal':1.2,'Terp Slurper':1.1}
        self.wax_cool_times = {'Shatter':45,'Budder':50,'Crumble':47,'Rosin':43,'Live Resin':48,'Sugar':46}

    def toggle_timer(self, instance):
        if self.event:
            Clock.unschedule(self._update_timer)
            self.event = None
            self.timer_label.text = 'Stopped'
            self.start_button.text = 'Start Heat Timer'
            return

        # Calculate times
        mat = self.material_spinner.text
        sty = self.style_spinner.text
        wax = self.wax_spinner.text
        intensity = self.intensity_slider.value

        self.heat_time = max(1, int(self.material_times[mat] * self.style_modifiers[sty] / intensity))
        self.cool_time = int(self.wax_cool_times[wax] * self.style_modifiers[sty])

        # Start
        self.phase = 'heat'
        self.time_left = self.heat_time
        self.timer_label.text = f'Heating: {self.time_left}s'
        self.start_button.text = 'Stop Timer'
        self.event = Clock.schedule_interval(self._update_timer, 1)

    def _update_timer(self, dt):
        self.time_left -= 1
        if self.time_left > 0:
            self.timer_label.text = f'{self.phase.capitalize()}: {self.time_left}s'
            return
        Clock.unschedule(self._update_timer)
        if self.phase == 'heat':
            self.phase = 'cool'
            self.time_left = self.cool_time
            self.timer_label.text = f'Cooling: {self.time_left}s'
            self.event = Clock.schedule_interval(self._update_timer, 1)
        else:
            self.timer_label.text = 'Dab Now!'
            self.start_button.text = 'Start Heat Timer'
            self.phase = None
            self.log_session()

    def log_session(self):
        fname = os.path.join(os.getcwd(), 'dab_timer_log.csv')
        new = not os.path.exists(fname)
        with open(fname,'a',newline='') as f:
            fields = ['timestamp','material','style','wax','intensity','heat_s','cool_s','rating']
            w = csv.DictWriter(f, fieldnames=fields)
            if new: w.writeheader()
            w.writerow({
                'timestamp':datetime.now().isoformat(),
                'material':self.material_spinner.text,
                'style':self.style_spinner.text,
                'wax':self.wax_spinner.text,
                'intensity':f'{self.intensity_slider.value:.1f}',
                'heat_s':self.heat_time,
                'cool_s':self.cool_time,
                'rating':''
            })

    def show_log(self, instance):
        fname = os.path.join(os.getcwd(), 'dab_timer_log.csv')
        if not os.path.exists(fname):
            Popup(title='No Log', content=Label(text='No log file.'), size_hint=(.8,.5)).open()
            return
        with open(fname,'r',newline='') as f: rows=list(csv.DictReader(f))
        content=BoxLayout(orientation='vertical',spacing=dp(5),padding=dp(5))
        scroll=ScrollView(size_hint=(1,1),scroll_type=['bars','content'],bar_width=dp(5))
        lst=BoxLayout(orientation='vertical',size_hint_y=None)
        lst.bind(minimum_height=lst.setter('height'))
        popup=Popup(title='Session Log',size_hint=(.9,.9))

        for i,r in enumerate(rows):
            dt = datetime.fromisoformat(r['timestamp'])
            dstr = f"{dt.month}/{dt.day}/{dt.year}"
            detail = f"{r['material']}, {r['style']}, {r['wax']},\n Intensity: {r['intensity']}×, {r['heat_s']}s, {r['cool_s']}s"
            row = BoxLayout(size_hint_y=None,height=dp(50))
            txt = BoxLayout(orientation='vertical',size_hint_x=0.6)
            lbl1 = Label(text=f"[b]{dstr}[/b]",markup=True,size_hint_y=None,height=dp(20),halign='center',valign='top')
            lbl1.text_size=(self.width*0.6,None)
            lbl2 = Label(text=detail,size_hint_y=None,height=dp(30),halign='center',valign='top')
            lbl2.text_size=(self.width*0.6,None)
            # Rating spinner in log entry
            rating_spinner = Spinner(text=r.get('rating','3'), values=[str(x) for x in range(1,6)], size_hint_x=0.1)
            rating_spinner.bind(text=lambda spinner,val,idx=i: self.update_rating(fname, rows, idx, val))
            # Load button to apply settings
            load_btn = Button(text='Load', size_hint_x=0.15)
            load_btn.bind(on_press=lambda btn, entry=r: self.load_entry(entry, popup))
            # Delete button
            delete_btn = Button(text='Delete', size_hint_x=0.15)
            delete_btn.bind(on_press=lambda btn, idx=i: self.delete_entry(popup, fname, rows, idx))
            txt.add_widget(lbl1)
            txt.add_widget(lbl2)
            row.add_widget(txt)
            row.add_widget(rating_spinner)
            row.add_widget(load_btn)
            row.add_widget(delete_btn)
            lst.add_widget(row)

        scroll.add_widget(lst)
        content.add_widget(scroll)
        close_btn = Button(text='Close',size_hint=(1,None),height=dp(50))
        close_btn.bind(on_press=popup.dismiss)
        content.add_widget(close_btn)
        popup.content=content
        popup.open()

    def update_rating(self, fname, rows, idx, val):
        rows[idx]['rating'] = val
        with open(fname,'w',newline='') as f:
            fields=['timestamp','material','style','wax','intensity','heat_s','cool_s','rating']
            w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore')
            w.writeheader(); w.writerows(rows)

    def load_entry(self, entry, popup):
        # Apply settings from log entry
        self.material_spinner.text = entry.get('material', self.material_spinner.text)
        self.style_spinner.text = entry.get('style', self.style_spinner.text)
        self.wax_spinner.text = entry.get('wax', self.wax_spinner.text)
        try:
            val = float(entry.get('intensity', '1.0'))
            self.intensity_slider.value = val
        except:
            pass
        popup.dismiss()

    def delete_entry(self, popup, fname, rows, idx):
        rows.pop(idx)
        with open(fname,'w',newline='') as f:
            fields=['timestamp','material','style','wax','intensity','heat_s','cool_s','rating']
            w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore')
            w.writeheader(); w.writerows(rows)
        popup.dismiss(); self.show_log(None)

    def close_app(self, instance):
        App.get_running_app().stop()

class DabApp(App):
    def build(self):
        return DabTimer()

if __name__=='__main__':
    DabApp().run()
