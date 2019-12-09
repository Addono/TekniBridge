from led import Led
from transitions import AbstractTransition



class FadeArray(AbstractTransition):

    def __init__(self, rate: float = 0.01) -> None:
        self.targets = [Led(0, 0, 0) for _ in range(2)]
        self.rate = rate

    def fix_dimension(self, previous):
        if len(previous) != len(self.targets):
            print("Dimension mismatch between previous (%s) and targets (%s) " % (len(previous), len(self.targets)))
            self.targets = [Led(*[0.0, 0, 0]) for _ in range(len(previous))]

    def step(self, previous):
        self.fix_dimension(previous)

        # if len(previous) != len(self.targets):
        #    print("Dimension mismatch between previous (%s) and targets (%s) " % (len(previous), len(self.targets)))
        #   self.targets = [Led(*[random(), random(), random()]) for _ in range(len(previous))]

        return self.computeFade(previous)

    def computeFade(self, previous):
        return [previous[i].blend(self.targets[i], self.rate) for i in range(len(previous))]

    def set_target(self, targets):
        # [Led([random(), random(), random()) for _ in range]
        self.targets = targets
