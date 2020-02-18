from typing import List, Optional

from transitions import AbstractTransition
from led import Led


class FadeArray(AbstractTransition):

    def __init__(self, rate: float = 0.01) -> None:
        self.rate = rate
        self._targets: List[Led] = []

    @property
    def targets(self):
        return self._targets
    
    @targets.setter
    def targets(self, targets: List[Led]):
        assert len(targets) > 0

        self._targets = targets

    def step(self, previous: List[Led]) -> List[Led]:
        # Do not do anything when targets is not yet set
        if not self._targets:
            return previous
        
        return [led_previous.blend(led_target, self.rate).with_brightness(self.brightness) for led_previous, led_target in zip(previous, self._targets)]
