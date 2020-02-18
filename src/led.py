from collections import Sequence

class Led(Sequence):
    """
    Represents an individual RGB LED. 
    
    The implementation aims to be immutable, although fields are left public. This could
    change in future versions.
    """

    def __init__(self, red: float, green: float, blue: float, brightness: float = 1.0):
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
        return (
            self.red == other.red
            and self.blue == other.blue
            and self.green == other.green
            and self.brightness == other.brightness
        )

    def with_brightness(self, brightness: float) -> 'Led':
        """
        Creates a new LED instance with the same colors, but new brightness
        @param brightness: The brightness of the new LED object
        @return: a new LED instance with the same colors, but new brightness
        """
        return Led(self.red, self.green, self.blue, brightness)

    def similar(self, other: 'Led', disparity: float = 0.05, only_color: bool = False) -> bool:
        return (
            abs(self.red - other.red) < disparity
            and abs(self.green - other.green) < disparity
            and abs(self.blue - other.blue) < disparity
            and (only_color or abs(self.brightness - other.brightness) < disparity)
        )

    def __str__(self) -> str:
        return "|".join(map(lambda x: str(round(x * 100)), [self.red, self.green, self.blue, self.brightness]))

    def scale(self, alpha: float) -> 'Led':
        """
        Create a linearly scaled instance of this LED.
        """
        assert 0.0 <= alpha <= 1.0

        scaled_values = (alpha * v for v in self)
        return Led(*scaled_values)

    def blend(self, other: 'Led', alpha: float) -> 'Led':
        """
        Blends - linearly scales - between two Leds. Returns self when alpha is zero, returns the other LED if
        alpha is one.
        """
        assert 0.0 <= alpha <= 1.0

        mixed_values = ((1 - alpha) * v1 + alpha * v2 for v1, v2 in zip(self, other))
        return Led(*mixed_values)
