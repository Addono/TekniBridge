class Led:

    def __init__(self, red: float, green: float, blue: float, brightness: float=1.0):
        super().__init__()

        self.red = red
        self.green = green
        self.blue = blue
        self.brightness = brightness

    def __len__(self):
        return 4

    def __getitem__(self, item):
        return [self.red, self.green, self.blue, self.brightness][item]

    def __eq__(self, other):
        """Overrides the default implementation"""
        return (self.red == other.red and self.blue == other.blue and self.green == other.green and self.brightness
        == other.brightness)

    def similar(self,other, disparity = 0.05):
        return (abs(self.red - other.red) < disparity and abs(self.green - other.green)< disparity and
                abs(self.blue - other.blue) < disparity and abs(self.brightness - other.brightness)< disparity)


    def scale(self, alpha: float):
        scaled_values = (alpha * v for v in self)
        return Led(*scaled_values)

    def blend(self, other: 'Led', alpha: float):
        mixed_values = ((1 - alpha) * v1 + alpha * v2 for v1, v2 in zip(self, other))
        return Led(*mixed_values)
