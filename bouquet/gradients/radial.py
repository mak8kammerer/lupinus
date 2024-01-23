'''
Radial Gradient
===============

The `RadialGradient` is a Kivy widget for creating a radial gradient effect,
where color is linearly interpolated from the center to the edges of the
widget. Currently, it is possible to set only two colors: the color of the
center (`center_color`) and the color of the border (`border_color`).

'''

__all__ = ('RadialGradient', )

from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.widget import Widget
from kivy.graphics import RenderContext
from kivy.properties import ColorProperty

# Make sure that OpenGL context is created
import kivy.core.window


KV = '''
<RadialGradient>:
    canvas:
        Color:
            rgba: 1.0, 1.0, 1.0, 1.0
        Rectangle:
            pos: self.pos
            size: self.size
'''


FRAGMENT_SHADER = '''
$HEADER$

// Inspired by https://gist.github.com/tito/4250317#file-gpuradialgradient-py

uniform vec4 centerColor;
uniform vec4 borderColor;

void main() {
    float distance = distance(tex_coord0, vec2(0.5)) * 2.0;
    gl_FragColor = mix(centerColor, borderColor, distance);
}
'''


class RadialGradient(Widget):
    
    center_color = ColorProperty(defaultvalue='white')
    '''
    Color of the widget center.
    
    :attr:`center_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `white`.
    '''
    
    border_color = ColorProperty(defaultvalue='black')
    '''
    Color of the widget borders.
    
    :attr:`border_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `black`.
    '''

    def __init__(self, **kwargs):
        self.canvas = RenderContext(
            fs=FRAGMENT_SHADER,
            use_parent_projection=True,
            use_parent_modelview=True,
            use_parent_frag_modelview=True
        )
        self.canvas['centerColor'] = tuple(self.center_color)
        self.canvas['borderColor'] = tuple(self.border_color)

        super(RadialGradient, self).__init__(**kwargs)

    def on_center_color(self, widget, new_value):
        widget.canvas['centerColor'] = tuple(new_value)
 
    def on_border_color(self, widget, new_value):
        widget.canvas['borderColor'] = tuple(new_value)


Builder.load_string(KV)
Factory.register('RadialGradient', cls=RadialGradient)
