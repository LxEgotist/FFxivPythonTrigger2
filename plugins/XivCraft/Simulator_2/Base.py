from typing import Tuple
import math
from FFxivPythonTrigger.lumina import lumina
from Lumina.Excel.GeneratedSheets import CraftLevelDifference, RecipeLevelTable, Recipe

clvBase = [120, 260, 390]
clvAdjust = [0, 5, 10, 13, 16, 19, 22, 25, 28, 30]

lv_dif = dict()
lv_dif_min = 999
lv_dif_max = -999
craft_lv_dif_sheet = lumina.lumina.GetExcelSheet[CraftLevelDifference]()
for _row in craft_lv_dif_sheet:
    if _row.Difference > lv_dif_max:
        lv_dif_max = _row.Difference
    if _row.Difference < lv_dif_min:
        lv_dif_min = _row.Difference
    lv_dif[_row.Difference] = (_row.ProgressFactor / 100, _row.QualityFactor / 100)

recipe_lv_sheet = lumina.lumina.GetExcelSheet[RecipeLevelTable]()
recipe_sheet = lumina.lumina.GetExcelSheet[Recipe]()

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


def lv2clv(lv: int):
    if lv <= 50: return lv
    return clvBase[(lv - 1) // 10 - 5] + clvAdjust[(lv - 1) % 10]


def lv_dif(clv: int, rlv: int) -> Tuple[float, float]:
    """
    :return: ProgressFactor, QualityFactor
    """
    dif = clv - rlv
    if dif < lv_dif_min:
        dif = lv_dif_min
    elif dif > lv_dif_max:
        dif = lv_dif_max
    return lv_dif[dif]


class Recipe(object):
    name: str
    rlv: int
    suggest_craft: int
    suggest_control: int
    difficulty: int
    quality: int
    durability: int

    def __init__(self, recipe_id: int):
        row = recipe_sheet.GetRow(recipe_id)
        rlvTable = row.RecipeLevelTable.Value
        self.name = row.ItemResult.Value.Name
        self.rlv = rlvTable.RowId
        self.suggest_craft = rlvTable.SuggestedCraftsmanship
        self.suggest_control = rlvTable.SuggestedControl
        self.difficulty = math.floor(rlvTable.Difficulty * row.DifficultyFactor / 100)
        self.quality = math.floor(rlvTable.Quality * row.QualityFactor / 100)
        self.durability = math.floor(rlvTable.Durability * row.DurabilityFactor / 100)


def base_progress(craft: int, clv: int, rlv: int):
    suggest = Definitions.recipe_lv_sheet.GetRow(rlv).SuggestedCraftsmanship
    return math.floor(lv_dif_progress(clv, rlv) * (0.21 * craft + 2) * (10000 + craft) / (10000 + Definitions.suggestProp[rlv][0]))


def base_quality(control: int, clv: int, rlv: int):
    return math.floor(lv_dif_quality(clv, rlv) * (0.35 * control + 35) * (10000 + control) / (10000 + Definitions.suggestProp[rlv][1]))


def total_push(efficiency, base, ball=1):
    temp = math.floor(efficiency * base * ball)
    return temp


def total_efficiency(skill, buffSum=0):
    return math.floor(skill * (1 + buffSum)) / 100
