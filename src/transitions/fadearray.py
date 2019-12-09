from transitions import AbstractTransition


class FadeArray(AbstractTransition):

    def __init__(self, rate: float = 0.01) -> None:
        self.rate = rate
        self.targets = None

    def step(self, previous):
        # if len(previous) != len(self.targets):
        #    print("Dimension mismatch between previous (%s) and targets (%s) " % (len(previous), len(self.targets)))
        #   self.targets = [Led(*[random(), random(), random()]) for _ in range(len(previous))]

        return [led_previous.blend(led_target, self.rate) for led_previous, led_target in zip(previous, self.targets)]
