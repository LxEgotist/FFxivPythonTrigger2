from . import Stage1, Stage2, Stage3, Stage4
from .. import Solver

stages = [Stage1.Stage1, Stage2.Stage2, Stage3.Stage3, Stage4.Stage4]


class Skyrim23Solver(Solver):
    @staticmethod
    def suitable(recipe, player):
        return recipe.status_flag == 0b1110011

    def __init__(self, recipe, player, logger):
        super().__init__(recipe, player, logger)
        self.stage = 0
        self.process_stages = [s() for s in stages]

    def process(self, craft=None, used_skill=None) -> str:
        if self.stage < 0: return ''
        if craft is None: return '闲静'
        while self.process_stages[self.stage].is_finished(craft, used_skill):
            self.stage += 1
            if self.stage >= len(self.process_stages):
                self.stage = -1
                return ''
        ans = self.process_stages[self.stage].deal(craft, used_skill)
        return ans
