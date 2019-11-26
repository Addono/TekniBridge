class Led:

    def __init__(self, red=0, green=0, blue=0, brightness=0):
        super().__init__()

        self.red = red
        self.green = green
        self.blue = blue
        self.brightness = brightness

    def __len__(self):
        return 4

    def __getitem__(self, item):
        return [self.red, self.green, self.blue, self.brightness][item]

    def scale(self, alpha):
        scaled_values = (alpha * v for v in self)
        return Led(*scaled_values)

    def blend(self, other, alpha):
        mixed_values = ((1 - alpha) * v1 + alpha * v2 for v1, v2 in zip(self, other))
        return Led(*mixed_values)
