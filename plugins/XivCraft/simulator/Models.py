import math

names = {
    'DesignChanges': '设计变动',
    'TrainedEye': '工匠的神速技巧',
    'IntensiveSynthesis': '集中制作',
    'DelicateSynthesis': '精密制作',
    'Groundwork': '坯料制作',
    'PreparatoryTouch': '坯料加工',
    'PatientTouch': '专心加工',
    'FocusedTouch': '注视加工',
    'MastersMend': '精修',
    'WasteNot': '俭约',
    'Veneration': '崇敬',
    'GreatStrides': '阔步',
    'MuscleMemory': '坚信',
    'StandardTouch': '中级加工',
    'RapidSynthesis': '高速制作',
    'FocusedSynthesis': '注视制作',
    'InnerQuiet': '内静',
    'Reflect': '闲静',
    'CarefulObservation': '最终确认',
    'HastyTouch': '仓促',
    'BasicTouch': '加工',
    'Innovation': '改革',
    'PrudentTouch': '俭约加工',
    'TricksOfTheTrade': '秘诀',
    'Observe': '观察',
    'Manipulation': '掌握',
    'BrandOfTheElements': '元素之印记',
    'CarefulSynthesis': '模范制作',
    'BasicSynthesis': '制作',
    'NameOfTheElements': '元素之美名',
    'ByregotsBlessing': '比尔格的祝福',
    'PreciseTouch': '集中加工',
    'WasteNotTwo': '长期俭约'
}


class SkillBase(object):
    HIDE = False
    KEEP_ROUND = False

    def __init__(self):
        if not hasattr(self, "name"):
            if type(self).__name__ in names:
                self.name = names[type(self).__name__]
            else:
                self.name = type(self).__name__

    progress = 0
    quality = 0
    cost = 0
    durability = 0

    def get_progress(self, status):
        return self.progress

    def get_quality(self, status):
        return self.quality

    def get_cost(self, status):
        return self.cost

    def get_durability(self, status):
        return self.durability

    def __str__(self):
        return self.name

    def after_use(self, status):
        pass

    def can_use(self, status):
        return True


class BuffBase(object):

    def __init__(self):
        if not hasattr(self, "name"):
            if type(self).__name__ in names:
                self.name = names[type(self).__name__]
            else:
                self.name = type(self).__name__

    def __str__(self):
        return self.name

    def get_progress_buff(self, action_use, container, status):
        return self.progress

    def get_quality_buff(self, action_use, container, status):
        return self.quality

    def get_cost_buff(self, action_use, container, status):
        return self.cost

    def get_durability_buff(self, action_use, container, status):
        return self.durability

    progress = 0
    quality = 0
    cost = 0
    durability = 0

    def go_next_round(self, action_use, container, status):
        container.param -= 1
        if container.param < 1:
            status.remove_effect(self)


class BallBase(object):
    progress = 1
    quality = 1
    durability = 1
    cost = 1

    def get_progress(self, status):
        return self.progress

    def get_quality(self, status):
        return self.quality

    def get_cost(self, status):
        return self.cost

    def get_durability(self, status):
        return self.durability

    def __init__(self):
        if not hasattr(self, "name"):
            if type(self).__name__ in names:
                self.name = names[type(self).__name__]
            else:
                self.name = type(self).__name__

    def __str__(self):
        return self.name

    def after_use(self, action_use, status):
        pass
