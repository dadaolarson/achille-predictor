from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import StringProperty
import datetime
import random

KV = '''
BoxLayout:
    orientation: 'vertical'
    padding: 20
    spacing: 15

    Label:
        id: next_time
        text: root.next_str
        font_size: '28sp'
        color: 0, 0.7, 0.9, 1

    Label:
        id: status
        text: "En attente..."
        font_size: '24sp'

    Button:
        text: "Démarrer surveillance"
        font_size: '22sp'
        size_hint_y: .4
        on_release: app.start_watch()
'''

class AviatorApp(App):
    next_str = StringProperty("Calcul...")

    def build(self):
        Clock.schedule_once(self.update_next, 0)
        return Builder.load_string(KV)

    def update_next(self, dt):
        now = datetime.datetime.now()
        # prochain décollage à 2m20 après chaque heure pile
        base = now.replace(minute=0, second=0, microsecond=0)
        target = base + datetime.timedelta(minutes=2, seconds=20)
        if target <= now:
            target += datetime.timedelta(hours=1)
        self.next_str = target.strftime("Prochain décollage\n%H:%M:%S")

    def start_watch(self):
        Clock.schedule_interval(self.check_time, 1)

    def check_time(self, dt):
        now = datetime.datetime.now()
        if now.second == 20 and 2 <= now.minute <= 3:
            self.root.ids.status.text = "🚀 DÉCOLLAGE PRÉVU"
            Clock.unschedule(self.check_time)
            return False
        return True

if __name__ == '__main__':
    AviatorApp().run()
