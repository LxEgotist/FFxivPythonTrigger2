from FFxivPythonTrigger.lumina import lumina

from Lumina.Excel.GeneratedSheets import CraftLevelDifference, RecipeLevelTable, Recipe

rlv = 0
durability = 1
progress = 2
quality = 3
lv = 0
craft = 1
control = 2
cp = 3

clvBase = [120, 260, 390]
clvAdjust = [0, 5, 10, 13, 16, 19, 22, 25, 28, 30]

lv_dif = dict()
lv_dif_min = 999
lv_dif_max = -999
craft_lv_dif_sheet = lumina.lumina.GetExcelSheet[CraftLevelDifference]()
for row in craft_lv_dif_sheet:
    if row.Difference > lv_dif_max:
        lv_dif_max = row.Difference
    if row.Difference < lv_dif_min:
        lv_dif_min = row.Difference
    lv_dif[row.Difference] = (row.ProgressFactor / 100, row.QualityFactor / 100)

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
