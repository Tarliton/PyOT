#largely unknown
gloombringer = genMonster("Gloombringer", 12, 5980)
gloombringer.health(10000)
gloombringer.type("blood")
gloombringer.defense(armor=1, fire=1, earth=1, energy=1, ice=1, holy=1, death=1, physical=1, drown=1)
gloombringer.experience(0)
gloombringer.speed(300)
gloombringer.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=0)
gloombringer.walkAround(energy=0, fire=0, poison=0)
gloombringer.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
gloombringer.melee(3000)