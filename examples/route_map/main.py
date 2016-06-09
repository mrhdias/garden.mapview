
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.bubble import Bubble
from kivy.garden.mapview import MapView, MapMarker, MapMarkerPopup
from mapview.geojson import GeoJsonMapLayer
from kivy.storage.jsonstore import JsonStore
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

class ImageButton(ButtonBehavior, Image):
    pass

class MapIcons(GridLayout):
    def __init__(self, *args, **kwargs):
        super(MapIcons, self).__init__(**kwargs)

        self.rows = 3
        self.cols = 1
        self.padding = '8sp'
        self.spacing = '8sp'
        self.size_hint = (None, None)
        self.height = 3 * self.width

        self.btn_zoom_in = ImageButton(size_hint=(1, 1./3.),
                                       allow_stretch=True,
                                       keep_ratio=True,
                                       source="assets/icon_zoom_in.png")
        self.btn_zoom_out = ImageButton(size_hint=(1, 1./3.),
                                        allow_stretch=True,
                                        keep_ratio=True,
                                        source="assets/icon_zoom_out.png")
        self.btn_center_on = ImageButton(size_hint=(1, 1./3.),
                                         allow_stretch=True,
                                         keep_ratio=True,
                                         source="assets/icon_crosshair.png")

        self.add_widget(self.btn_zoom_in)
        self.add_widget(self.btn_zoom_out)
        self.add_widget(self.btn_center_on)



class ShowMap(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(ShowMap, self).__init__(**kwargs)

        points = JsonStore("points_of_interest.json")

        self.view = MapView(lat=points["center"]['lat'],
                            lon=points["center"]['lon'],
                            zoom=15,
                            cache_dir="cache")

        # Add Route
        layer = GeoJsonMapLayer(source="route.json")
        self.view.add_layer(layer)

        # Add User
        user_marker = MapMarker(lat=points["center"]['lat'],
                                lon=points["center"]['lon'],
                                source='assets/icon_user.png')
        self.view.add_widget(user_marker)

        # Add Icons
        self.icons = MapIcons(width='60sp')

        def zoom_in(instance):
            print('Zoom In:', self.view.zoom)
            if self.view.zoom == 19:
                return
            self.view.zoom += 1
        self.icons.btn_zoom_in.bind(on_press=zoom_in)

        def zoom_out(instance):
            print('Zoom Out:', self.view.zoom)
            if self.view.zoom == 1:
                return
            self.view.zoom -= 1
        self.icons.btn_zoom_out.bind(on_press=zoom_out)

        def center_on(instance):
            print('Center On:', user_marker.lat, user_marker.lon)
            self.view.center_on(user_marker.lat, user_marker.lon)
        self.icons.btn_center_on.bind(on_press=center_on)

        self.view.add_widget(self.icons)

        for point in points["list"]:
            bubble = Bubble(orientation='vertical', background_image=point['image'])
            map_marker = MapMarkerPopup(id="marker",
                                        lat=point['lat'],
                                        lon=point['lon'],
                                        source='assets/icon_marker.png')
            map_marker.add_widget(bubble)
            self.view.add_marker(map_marker)
        
        self.add_widget(self.view)

        ### Begin Close Bubble ###
        def close_bubbles(arg, touch):
            for c in self.view.children:
                for cc in c.children:
                    if cc.id == 'marker':
                        if len(cc.children) and cc.is_open:
                            cc.is_open = False
                            cc.refresh_open_status()
        self.view.children[-1].bind(on_touch_up=close_bubbles)
        ### End Close Bubble ###


    def on_size(self, *args):
        if self.view:
            self.icons.pos = (self.width - self.icons.width, (self.height - self.icons.height)/2.)


class MapsApp(App):
    def build(self):
        self.title = 'Route Map'
        return ShowMap()

if __name__ == '__main__':
    MapsApp().run()