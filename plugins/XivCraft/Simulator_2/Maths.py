from typing import Tuple

from . import Definitions
import math


def lv2clv(lv: int):
    if lv <= 50: return lv
    return Definitions.clvBase[(lv - 1) // 10 - 5] + Definitions.clvAdjust[(lv - 1) % 10]


def lv_dif(clv: int, rlv: int)-> Tuple[float,float]:
    """
    :return: ProgressFactor, QualityFactor
    """
    dif = clv - rlv
    if dif < Definitions.lv_dif_min:
        dif = Definitions.lv_dif_min
    elif dif > Definitions.lv_dif_max:
        dif = Definitions.lv_dif_max
    return Definitions.lv_dif[dif]


def base_progress(craft: int, clv: int, rlv: int):
    suggest=Definitions.recipe_lv_sheet.GetRow(rlv).SuggestedCraftsmanship
    return math.floor(lv_dif_progress(clv, rlv) * (0.21 * craft + 2) * (10000 + craft) / (10000 + Definitions.suggestProp[rlv][0]))


def base_quality(control: int, clv: int, rlv: int):
    return math.floor(lv_dif_quality(clv, rlv) * (0.35 * control + 35) * (10000 + control) / (10000 + Definitions.suggestProp[rlv][1]))


def total_push(efficiency, base, ball=1):
    temp = math.floor(efficiency * base * ball)
    return temp


def total_efficiency(skill, buffSum=0):
    return math.floor(skill * (1 + buffSum)) / 100
