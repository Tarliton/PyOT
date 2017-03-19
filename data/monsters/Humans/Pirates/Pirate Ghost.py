pirate_ghost = genMonster("Pirate Ghost", 35, 5995)
pirate_ghost.health(275)
pirate_ghost.type("undead")
pirate_ghost.defense(armor=20, fire=1, earth=0, energy=1, ice=1, holy=1.25, death=0, physical=0, drown=1)
pirate_ghost.experience(250)
pirate_ghost.speed(230)
pirate_ghost.behavior(summonable=0, hostile=True, illusionable=True, convinceable=0, pushable=True, pushItems=True, pushCreatures=False, targetDistance=1, runOnHealth=0)
pirate_ghost.walkAround(energy=1, fire=1, poison=0)
pirate_ghost.immunity(paralyze=1, invisible=0, lifedrain=1, drunk=0)
pirate_ghost.voices("Yooh Ho Hooh Ho!", "Hell is waiting for You!", "It's alive!", "The curse! Aww the curse!", "You will not get my treasure!")
pirate_ghost.melee(95, condition=CountdownCondition(CONDITION_POISON, 2), conditionChance=100)
pirate_ghost.loot( ("stealth ring", 0.75), (2148, 100, 63), ("tattered piece of robe", 4.5), ("parchment", 0.5), ("spike sword", 0.0025), ("red robe", 0.25) )