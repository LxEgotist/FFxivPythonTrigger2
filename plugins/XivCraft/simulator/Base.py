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


class Player(object):
    def __init__(self, lv: int, craft: int, control: int, maxCp: int):
        self.lv = lv
        self.craft = craft
        self.control = control
        self.maxCp = maxCp
        self.clv = lv2clv(lv)


class Status(object):
    def __init__(self, player: Player, recipe: Recipe, current_cp: int = None, current_progress: int = None, current_quality: int = None,
                 current_durability: int = None, effects: list = None, status_round=1, cal_craft: int = None, cal_controls: dict = None):
        self.player = player
        self.recipe = recipe
        self.current_cp = current_cp or player.maxCp
        self.current_progress = current_progress or recipe.difficulty
        self.current_quality = current_quality or recipe.quality
        self.current_durability = current_durability or recipe.durability
        self.effects = effects or []
        self.status_round = status_round
        progress_factor, quality_factor = lv_dif(player.clv, recipe.rlv)
        if cal_craft is None:
            self.cal_craft = progress_factor * (0.21 * player.craft + 2) * (10000 + player.craft) / (10000 + recipe.suggest_craft)
        else:
            self.cal_craft = cal_craft
        if cal_controls is None:
            self.cal_controls = dict()
            for i in range(1, 12):
                control = player.control * (0.8 + i * 0.2)
                self.cal_controls[i] = quality_factor * (0.35 * control + 35) * (10000 + control) / (10000 + recipe.suggest_control)
        else:
            self.cal_controls = cal_controls

    def copy(self):
        return
