'''
Created on May 1, 2013

@author: christofer
'''

import kivy
kivy.require('1.6.0')

from kivy.app import App
from kivy.graphics import Color, Ellipse, Line
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class RootWidget(BoxLayout):

    points = ListProperty()

    def on_touch_down(self, touch):
        if len(self.points) < 4:
            with self.canvas.after:
                Color(1, 1, 0)
                d = 15.
                Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
                line = Line(points=touch.pos)
                if len(self.points):
                    line.points += self.points[-1]
                self.points.append(touch.pos)
        else:
            self.canvas_clear()
        return True

    def canvas_clear(self):
        self.points = []
        self.canvas.after.clear()


class WindButton(Button):
    pass


class MyApp(App):
    def build(self):
        return RootWidget()


if __name__ == '__main__':
    MyApp().run()
