from transitions import AbstractTransition


class FadeArray(AbstractTransition):

    def __init__(self, rate: float = 0.01) -> None:
        self.rate = rate
        self.targets = None

    def step(self, previous):
        return [led_previous.blend(led_target, self.rate) for led_previous, led_target in zip(previous, self.targets)]
