'''
Created on May 1, 2013

@author: Christofer Bertonha
'''


import kivy
kivy.require('1.6.0')

import random

from kivy.app import App
from kivy.graphics import Color, Ellipse, Line
from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image


class RootWidget(GridLayout):
    map = ObjectProperty(None)
    wind = ObjectProperty(None)
    wind_button = ObjectProperty(None)
    text_area = ObjectProperty(None)

    def random_wind(self):
        angle = random.randint(0, 359)
        self.wind.rotation = angle

    def change_wind(self, *args):
        if len(self.map.points) > 4:
            self.map.clear_points()
            self.random_wind()


class LocationPlace(Image):

    points = ListProperty()

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            with self.canvas.after:
                Color(1, 1, 0)
                d = 15.
                Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
                line = Line(points=touch.pos)
                if len(self.points):
                    line.points += self.points[-1]
                self.points.append(touch.pos)
            return True
        return super(LocationPlace, self).on_touch_down(touch)

    def clear_points(self):
        self.points = []
        self.canvas.after.clear()


class MyApp(App):
    def build(self):
        root = RootWidget()
        root.map.bind(points=root.change_wind)
        root.wind_button.bind(on_press=root.change_wind)
        root.random_wind()
        return root


if __name__ in ('__main__', '__android__'):
    MyApp().run()
