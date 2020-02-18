import pyglet  # pyre-ignore

from rpi_ws281x_mock import PixelStrip


class VisualPixelStrip(PixelStrip):

    def begin(self):
        super().begin()

        self.window = pyglet.window.Window(1200, 20)

    def show(self):
        super().show()

        verts = []
        colors = []

        n = self._led_data.size
        w = self.window.width
        h = self.window.height

        for i, led in enumerate(self._led_data):
            x1 = int(round((i / n) * w))
            x2 = int(round(((i + 1) / n) * w))
            y1 = 0
            y2 = h

            white = (self._led_data[i] >> 24) & 0xff
            r = (self._led_data[i] >> 16) & 0xff
            g = (self._led_data[i] >> 8) & 0xff
            b = self._led_data[i] & 0xff

            color = list(int((c * white * self.brightness) / (255 * 255)) for c in (r, g, b))

            verts += [x1, y1, x2, y1, x2, y2, x1, y2]
            colors += color * 4

        pyglet.graphics.draw(n * 4, pyglet.gl.GL_QUADS, ('v2i', verts), ('c3B', bytes(colors)))

        self.window.switch_to()
        self.window.dispatch_events()
        self.window.dispatch_event('on_draw')
        self.window.flip()
