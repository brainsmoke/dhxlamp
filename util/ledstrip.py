
RGB = (0, 1, 2)
GRB = (1, 0, 2)
RBG = (0, 2, 1)
BRG = (2, 0, 1)
GBR = (1, 2, 0)
BGR = (2, 1, 0)

class LedStrip(object):

    def calc_gamma(self):
        max_gamma = 255.**self.gamma
        self.gamma_map = [ chr(int( (1 + 2 * (x*self.brightness)**self.gamma / (max_gamma/255.)) //2 )) for x in xrange(256) ]

    def __init__(self, led_order=RGB, gamma=2.2, brightness=1.):
        self.gamma = float(gamma)
        self.brightness = float(brightness)
        self.led_order = led_order
        self.calc_gamma()

    def set_brightness(self, brightness):
        self.brightness = float(brightness)
        self.calc_gamma()

    def set_gamma(self, gamma):
        self.gamma = float(gamma)
        self.calc_gamma()

    def get_binary_data(self, data):
        buf = bytearray(len(data*3))
        gamma_map = self.gamma_map
        r_i, g_i, b_i = self.led_order

        for i, (r, g, b) in enumerate(data):

            buf[i*3+r_i] = gamma_map[min(255, max(int(r), 0))]
            buf[i*3+g_i] = gamma_map[min(255, max(int(g), 0))]
            buf[i*3+b_i] = gamma_map[min(255, max(int(b), 0))]

        return bytes(buf)

