'''
Created on May 1, 2013

@author: Christofer Bertonha
'''


import kivy
kivy.require('1.6.0')

import random

from kivy.app import App
from kivy.graphics import Color, Ellipse, Line
from kivy.properties import ListProperty, ObjectProperty, BooleanProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image


DIAMETER = 17.

MESSANGES = (
    'Choose Point A',
    'Choose Point B',
    'Choose Point C',
    'Choose Land Point',
)


def calc_pos(touch):
    return (touch.x - DIAMETER / 2, touch.y - DIAMETER / 2)


def line_points(touch, points):
    if len(points):
        return touch.pos + points[-1]
    return touch.pos


class RootWidget(GridLayout):
    map = ObjectProperty(None)
    wind = ObjectProperty(None)
    wind_button = ObjectProperty(None)
    reset_button = ObjectProperty(None)
    text_area = ObjectProperty(None)

    def __init__(self, **kw):
        super(RootWidget, self).__init__(**kw)
        self.map.bind(points=self.points_added)
        self.wind_button.bind(on_press=self.change_wind)
        self.reset_button.bind(on_press=self.clean_points)

    def random_wind(self):
        angle = random.randint(0, 359)
        self.wind.rotation = angle

    def clean_points(self, *args):
        self.map.clear_points()

    def change_wind(self, *args):
        self.clean_points(*args)
        self.random_wind()

    def points_added(self, *args):
        total_points = len(self.map.points)
        if total_points < 4:
            self.map.add_points = True
            self.text_area.text = MESSANGES[total_points]
        elif total_points == 4:
            self.map.add_points = False
            self.text_area.text = 'You are sure?'
        elif total_points > 4:
            self.change_wind()


class LocationPlace(Image):

    points = ListProperty()
    add_points = BooleanProperty(True)

    def on_touch_down(self, touch):
        if self.add_points and self.collide_point(*touch.pos):
            with self.canvas.after:
                Color(1, 1, 0)
                elipse = Ellipse(pos=calc_pos(touch),
                                 size=(DIAMETER, DIAMETER))
                line = Line(points=line_points(touch, self.points))
                touch.ud['elipse'] = elipse
                touch.ud['line'] = line
            return True
        return super(LocationPlace, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.add_points and self.collide_point(*touch.pos):
            with self.canvas.after:
                elipse = touch.ud['elipse']
                elipse.pos = calc_pos(touch)
                line = touch.ud['line']
                line.points = line_points(touch, self.points)
            return True
        return super(LocationPlace, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.add_points and self.collide_point(*touch.pos):
            self.points.append(touch.pos)
            return True
        return super(LocationPlace, self).on_touch_up(touch)

    def clear_points(self):
        self.points = []
        self.canvas.after.clear()


class MyApp(App):
    def build(self):
        root = RootWidget()
        root.random_wind()
        return root


if __name__ in ('__main__', '__android__'):
    MyApp().run()
