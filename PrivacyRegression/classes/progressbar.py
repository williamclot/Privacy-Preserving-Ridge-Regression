from math import *
import sys
import time
from utils import termcol as tc

class ProgressBar:
    """
    This class allows you to make easily a progress bar.
    """

    def __init__(self, steps, maxbar=100, title='Chargement'):
        if steps <= 0 or maxbar <= 0 or maxbar > 200:
            raise ValueError

        self.steps = steps
        self.maxbar = maxbar
        self.title = title

        self.perc = 0
        self._completed_steps = 0

        self.update(False)

    def update(self, increase=True):
        if increase:
            self._completed_steps += 1

        self.perc = floor(self._completed_steps / self.steps * 100)

        if self._completed_steps > self.steps:
            self._completed_steps = self.steps

        steps_bar = floor(self.perc / 100 * self.maxbar)

        if steps_bar == 0:
            visual_bar = self.maxbar * ' '
        else:
            visual_bar = (steps_bar - 1) * '=' + '>' + (self.maxbar - steps_bar) * ' '

        sys.stdout.write(tc.HEADER+'\r' + self.title + ' [' + visual_bar + '] ' + str(self.perc) + '%'+' | '+ str(self._completed_steps)+tc.ENDC)
        sys.stdout.flush()


if __name__ == '__main__':
    bar = ProgressBar(50)

    i = 0
    while bar.perc != 100:
        bar.update()
        time.sleep(0.01)

        i += 1