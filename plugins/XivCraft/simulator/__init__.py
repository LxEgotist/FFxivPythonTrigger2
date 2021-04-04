################
# 1. 使用技能
# 2. 计算buff提供的加成总和，计算加减数值并且执行（e.g.改革，节俭，不包括內静！）
# 3. 执行 skill.after_use 统计 “需要增加的 buff ” , 或是对 status 进行修改（e.g.秘诀回复 cp ，掌握获取 buff ，比尔格修改內静等级为 0 ）
# 4. 移除存在的 “需要增加的 buff ”
# 5. 执行 effects.go_next_round （e.g.掌握回复耐久，內静如果 action_used 具有 quality 属性则自身等级+=1）
# 6. 执行 ball.go_next_round （e.g.紫球将待增加 buff 回合翻倍）
# 7. 将 effects 中具有 rounds 属性的 effect.param -= 1，并且移除 effect.param < 1 的项目
# 8. merge “需要增加的 buff ” 到 effects
###############
