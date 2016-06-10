
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.garden.mapview import MapView, MapMarker, MapSource
from functools import partial

class Toolbar(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(Toolbar, self).__init__(**kwargs)

        self.size_hint_y = None
        self.height = '48dp'
        self.padding = '4dp'
        self.spacing = '4dp'

        with self.canvas:
            Color(.2, .2, .2, .6, mode='rgba')
            self.rect = Rectangle(pos=self.pos, size=self.size)

        def update_rect(*args):
            self.rect.pos=(self.x, self.y)
            self.rect.size=(self.width, self.height)

        self.bind(pos=update_rect)
        self.bind(size=update_rect)


class MapBrowser(RelativeLayout):
    def __init__(self, *args, **kwargs):
        super(MapBrowser, self).__init__(**kwargs)

        mapview = MapView(lat=50.6394,
                          lon=3.057,
                          zoom=8,
                          cache_dir="cache")
        
        self.add_widget(mapview)

        mapview.add_widget(MapMarker(lat=50.6394, lon=3.057))
        mapview.add_widget(MapMarker(lat=-33.867, lon=151.206))

        top_bar = Toolbar(pos_hint={'top': 1})

        def center_on(lat, lon, instance):
            mapview.center_on(lat, lon)
            label_lat.text = "Latitude: {}".format(mapview.lat)
            label_lon.text = "Longitude: {}".format(mapview.lon)

        btn_lille = Button(text="Move to Lille, France")
        btn_lille.bind(on_release=partial(center_on, 50.6394, 3.057))
        top_bar.add_widget(btn_lille)

        btn_sydney = Button(text="Move to Sydney, Autralia")
        btn_sydney.bind(on_release=partial(center_on, -33.867, 151.206))
        top_bar.add_widget(btn_sydney)

        spinner_src = Spinner(text="mapnik", values=MapSource.providers.keys())
        def set_source(instance, selected_text):
            mapview.map_source = selected_text
        spinner_src.bind(text=set_source)
        top_bar.add_widget(spinner_src)

        bottom_bar = Toolbar()
        label_lon = Label(text="Longitude: {}".format(mapview.lon))
        label_lat = Label(text="Latitude: {}".format(mapview.lat))
        bottom_bar.add_widget(label_lon)
        bottom_bar.add_widget(label_lat)

        self.add_widget(top_bar)
        self.add_widget(bottom_bar)

class MapBrowserApp(App):
    def build(self):
        self.title = 'Map Browser'
        return MapBrowser()

if __name__ == '__main__':
    MapBrowserApp().run()