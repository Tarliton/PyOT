
spit_nettle = genMonster("Spit Nettle", 221, 6062)
spit_nettle.health(150, healthmax=150)
spit_nettle.type("slime")
spit_nettle.defense(armor=15, fire=1.1, earth=0, energy=0, ice=0.8, holy=1, death=1, physical=1, drown=1)
spit_nettle.experience(25)
spit_nettle.speed(0)
spit_nettle.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=False, pushCreatures=False, targetDistance=1, runOnHealth=0)
spit_nettle.walkAround(energy=0, fire=0, poison=0)
spit_nettle.immunity(paralyze=1, invisible=0, lifedrain=0, drunk=1)
spit_nettle.loot( ("sling herb", 6.0, 2), ("shadow herb", 9.5), (2148, 24.5, 5), ("grave flower", 0.75), ("seeds", 0.5), ("nettle blossom", 0.75), ("nettle spit", 7.5) )