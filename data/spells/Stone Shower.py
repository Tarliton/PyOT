conjure = spell.Spell("Stone Shower", "adori mas tera", icon=23, group=SUPPORT_GROUP)
conjure.require(mana=430, level=28, maglevel=0, soul=3, learned=0, vocations=(2, 6))
conjure.use(2260)
conjure.cooldowns(0, 3)
conjure.targetEffect(callback=spell.conjure(2288, 3))

rune = spell.Rune(2288, icon=116, count=3, target=TARGET_AREA, group=ATTACK_GROUP)
rune.cooldowns(0, 2)
rune.require(mana=0, level=28, maglevel=0)
rune.area(AREA_CIRCLE3)
rune.targetEffect(callback=spell.damage(1, 2.6, 6, 16, EARTH))
rune.effects(area=EFFECT_STONES, shoot=ANIMATION_EARTH)