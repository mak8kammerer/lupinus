from kivy.tests.common import GraphicUnitTest


class GradientsTests(GraphicUnitTest):

    def test_color_stop(self):
        from bouquet.gradients import ColorStop
        
        c = ColorStop()
        self.assertEqual(c.position, 0.0)
        self.assertEqual(c.color, [1.0, 1.0, 1.0, 1.0])

        c.position = 1.5
        self.assertEqual(c.position, 1.0)
        
        c.position = -1.0
        self.assertEqual(c.position, 0.0)

        c = ColorStop(position=0.5, color='red')
        self.assertEqual(c.position, 0.5)
        self.assertEqual(c.color, [1.0, 0.0, 0.0, 1.0])

        with self.assertRaises(ValueError):
            c.color = None

        self.assertEqual(c._data, (0.5, 1.0, 0.0, 0.0, 1.0))
        
        repr_msg = '<ColorStop(position=0.5, color=[1.0, 0.0, 0.0, 1.0])>'
        self.assertEqual(repr(c), repr_msg)

    def test_gradient_base(self):
        from bouquet.gradients import ColorStop
        from bouquet.gradients.base import GradientBase
        
        render = self.render
        
        wid = GradientBase()
        render(wid)

        s = [
            ColorStop(position=0.0, color='black'),
            ColorStop(position=1.0, color='white')
        ]
        
        wid.color_stops = s
        texture = wid._1d_gradient_texture
        pixels = texture.pixels
        
        self.assertEqual(texture.height, 1)
        self.assertEqual(texture.width, 1024)

        self.assertEqual(len(pixels), 4 * 1024)
        # 0.0 -> right -> black
        self.assertEqual(pixels[:4], b'\x00\x00\x00\xff')
        # 0.5 -> middle -> gray
        self.assertEqual(pixels[4 * 512: 4 * 513], b'\x80\x80\x80\xff')
        # 1.0 -> left -> white
        self.assertEqual(pixels[-4:], b'\xff\xff\xff\xff')

        s = [
            ColorStop(position=0.75, color=[1.0, 0.0, 0.0, 0.0]),
            ColorStop(position=0.25, color=[0.0, 0.0, 1.0, 1.0])
        ]
        
        wid.color_stops = s
        texture = wid._1d_gradient_texture
        pixels = texture.pixels
        
        self.assertEqual(texture.height, 1)
        self.assertEqual(texture.width, 1024)

        self.assertEqual(len(pixels), 4 * 1024)
        # 0.0 -> opaque blue
        self.assertEqual(pixels[:4], b'\x00\x00\xff\xff')
        # 0.25 -> opaque blue
        self.assertEqual(pixels[4 * 256: 4 * 257], b'\x00\x00\xff\xff')
        # 0.75 -> transparent red == transparent black
        self.assertEqual(pixels[4 * 768: 4 * 769], b'\x00\x00\x00\x00')
        # 1.0 -> transparent red == transparent black
        self.assertEqual(pixels[-4:], b'\x00\x00\x00\x00')

        with self.assertRaises(ValueError):
            wid.color_stops = [ColorStop() for _ in range(1025)]

        with self.assertRaises(TypeError):
            wid.color_stops = [1]

    def test_linear_gradient(self):
        #TODO: test transparency
        pass

    def test_bilinear_gradient(self):
        from bouquet.gradients import BilinearGradient

        render = self.render

        wid = BilinearGradient()
        render(wid)

        wid.bottom_left_color = '#ff0000'
        render(wid)

        texture = BilinearGradient.render_texture()
        self.assertEqual(texture.size, (100, 100))

        tex_size = (500, 600)
        texture = BilinearGradient.render_texture(
            size=tex_size,
            bottom_left_color='#00000000'
        )
        self.assertEqual(texture.size, tex_size)

        pixels = texture.pixels
        self.assertEqual(len(pixels), tex_size[0] * tex_size[1] * 4)

        # bottom left corner -> transparent black
        self.assertEqual(pixels[:4], b'\x00\x00\x00\x00')
        # top right corner -> yellow
        self.assertEqual(pixels[-4:], b'\xff\xff\x00\xff')

    def test_radial_gradient(self):
        from kivy.graphics.fbo import Fbo
        from bouquet.gradients import RadialGradient

        render = self.render

        wid = RadialGradient()
        render(wid)

        wid.border_color = '#ff0000'
        render(wid)

        texture = RadialGradient.render_texture()
        self.assertEqual(texture.size, (100, 100))

        tex_size = (500, 500)
        texture = RadialGradient.render_texture(
            size=tex_size,
            border_color='#00000000'
        )
        self.assertEqual(texture.size, tex_size)

        pixels = texture.pixels
        self.assertEqual(len(pixels), tex_size[0] * tex_size[1] * 4)

        # bottom left corner -> transparent black
        self.assertEqual(pixels[:4], b'\x00\x00\x00\x00')
        # TODO: test center_color here
