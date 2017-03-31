import builtins
from tornado import gen, ioloop
from collections import deque
import time
import userconfig
import math
from . import sql
from . import otjson
import sys
import random
import glob
import re
import os
import config
from game import item
from . import inflect
import pickle
import game

builtins.SERVER_START = time.time() - config.tibiaTimeOffset
IS_ONLINE = False
IS_RUNNING = True


def _txtColor(text, color):
    if color == "blue":
        color = 34
    elif color == "red":
        color = 31
    elif color == "green":
        color = 32
    elif color == "yellow":
        color = 33
    RESET_SEQ = "\033[0m"
    COLOR_SEQ = "\033[1;%dm"

    return "%s%s%s" % (COLOR_SEQ % color, text, RESET_SEQ)


@gen.coroutine
def loader(timer):
    sys.stdout.write("\x1b]2;PyOT\x07")

    # Begin loading items
    item.loadItems()

    # Initialize SQL
    yield sql.connect()

    # Does this database have tables?
    # Check one, etc players.
    future = sql.runQueryWithException("SELECT 1 FROM `players`")
    try:
        yield future
    except:
        pass
    if future.exception():
        yield install_tables()

    # Reset online status
    print("> > Reseting players online status...", end=' ')
    sql.runOperation("UPDATE players SET online = 0")
    print("%40s\n" % _txtColor("\t[DONE]", "blue"))

    globalData = sql.runQuery("SELECT `key`, `data`, `type` FROM `globals` WHERE `world_id` = %s" % config.worldId)
    groupData = sql.runQuery("SELECT `group_id`, `group_name`, `group_flags` FROM `groups`")
    houseData = sql.runQuery("SELECT `id`,`owner`,`guild`,`paid`,`name`,`town`,`size`,`rent`,`data` FROM `houses` WHERE `world_id` = %s" % config.worldId)

    # Globalize certain things
    print("> > Globalize data...", end=' ')
    const = sys.modules["game.const"]
    builtins.const = const

    for i in dir(const):
        if not "__" in i:
            setattr(builtins, i, getattr(const, i))

    for i in dir(sys.modules["game.errors"]):
        if not "__" in i:
            setattr(builtins, i, getattr(sys.modules["game.errors"], i))

    for i in sys.modules["game.functions"].globalize:
        setattr(builtins, i, getattr(sys.modules["game.functions"], i))

    print("%55s\n" % _txtColor("\t[DONE]", "blue"))

    # Tornado features.
    builtins.ioloop_ins = ioloop.IOLoop.instance()

    builtins.call_later = builtins.ioloop_ins.call_later

    builtins.call_at = builtins.ioloop_ins.call_at
    builtins.remove_timeout = builtins.ioloop_ins.remove_timeout
    builtins.add_callback = builtins.ioloop_ins.add_callback
    builtins.add_future = builtins.ioloop_ins.add_future
    builtins.PeriodicCallback = ioloop.PeriodicCallback

    # Important builtins.
    builtins.sql = sql
    builtins.config = config
    builtins.userconfig = userconfig

    builtins.register = game.scriptsystem.register
    builtins.registerFirst = game.scriptsystem.registerFirst
    builtins.registerForAttr = game.scriptsystem.registerForAttr
    
    builtins.functions = game.functions
    builtins.sys = sys
    builtins.math = math
    builtins.deque = deque
    builtins.random = random
    builtins.time = time
    builtins.re = re
    builtins.spell = game.spell # Simplefy spell making
    builtins.Item = game.item.Item
    builtins.makeItem = game.item.makeItem
    builtins.itemAttribute = game.item.attribute
    builtins.cid = game.item.cid
    builtins.idByName = game.item.idByName
    builtins.getTile = game.map.getTile
    builtins.setTile = game.map.setTile
    builtins.getTileConst = game.map.getTileConst
    builtins.getTileConst2 = game.map.getTileConst2
    builtins.Boost = game.conditions.Boost
    builtins.MultiCondition = game.conditions.MultiCondition
    builtins.itemAttribute = game.item.attribute
    builtins.getHouseId = game.map.getHouseId
    builtins.Position = game.position.Position
    builtins.StackPosition = game.position.StackPosition
    builtins.getHouseById = game.house.getHouseById
    builtins.getGuildById = game.guild.getGuildById
    builtins.getGuildByName = game.guild.getGuildByName
    builtins.logger = sys.modules["game.logger"]

    # Resources
    builtins.genMonster = game.monster.genMonster
    builtins.genNPC = game.npc.genNPC
    builtins.genQuest = game.resource.genQuest
    builtins.genOutfit = game.resource.genOutfit
    builtins.genMount = game.resource.genMount
    builtins.regVocation = game.vocation.regVocation

    # Spells
    builtins.typeToEffect = game.spell.typeToEffect

    # Grab them
    builtins.getNPC = game.npc.getNPC
    builtins.getMonster = game.monster.getMonster

    # Used alot in monster and npcs
    builtins.chance = game.monster.chance

    # We use this in the import system
    builtins.scriptInitPaths = game.scriptsystem.scriptInitPaths

    # Access
    builtins.access = game.scriptsystem.access

    # Conditions
    builtins.Condition = game.conditions.Condition
    builtins.Boost = game.conditions.Boost
    builtins.CountdownCondition = game.conditions.CountdownCondition
    builtins.PercentCondition = game.conditions.PercentCondition
    builtins.MultiCondition = game.conditions.MultiCondition
    builtins.RepeatCondition = game.conditions.RepeatCondition

    # Pathfinder
    builtins.pathfinder = game.pathfinder

    # Deathlist
    builtins.deathlist = game.deathlist

    # Bans
    builtins.ipIsBanned = game.ban.ipIsBanned
    builtins.playerIsBanned = game.ban.playerIsBanned
    builtins.accountIsBanned = game.ban.accountIsBanned
    builtins.addBan = game.ban.addBan

    # Market
    builtins.getMarket = game.market.getMarket
    builtins.newMarket = game.market.newMarket

    # Creature and Player class. Mainly for test and savings.
    builtins.Creature = game.creature.Creature
    builtins.Player = game.player.Player
    builtins.Monster = game.monster.Monster

    # JSON
    builtins.json = otjson

  
    class Globalizer(object):
        __slots__ = ()
        monster = game.monster
        npc = game.npc
        creature = game.creature
        player = game.player
        map = game.map
        item = game.item
        scriptsystem = game.scriptsystem
        spell = game.spell
        resource = game.resource
        vocation = game.vocation
        const = game.const
        house = game.house
        guild = game.guild
        party = game.party
        errors = game.errors
        chat = game.chat
        deathlist = game.deathlist
        ban = game.ban
        market = game.market

    builtins.game = Globalizer()

    print("> > Loading global data...", end=' ')
    for x in ( yield globalData ):
        if x['type'] == 'json':
            game.functions.globalStorage[x['key']] = otjson.loads(x['data'].decode("utf-8")) # JSON must be utf-8
        elif x['type'] == 'pickle':
            game.functions.globalStorage[x['key']] = pickle.loads(x['data'])
        else:
            game.functions.globalStorage[x['key']] = x['data']
    print("%50s\n" % _txtColor("\t[DONE]", "blue"))

    print("> > Loading groups...", end=' ')
    for x in (yield groupData):
        game.functions.groups[x['group_id']] = (x['group_name'], otjson.loads(x['group_flags']))
    print("%60s\n" % _txtColor("\t[DONE]", "blue"))

    print("> > Loading guilds...", end=' ')
    game.guild.load()
    print("%60s\n" % _txtColor("\t[DONE]", "blue"))

    print("> > Loading bans...", end=' ')
    game.ban.refresh()
    print("%60s\n" % _txtColor("\t[DONE]", "blue"))

    print("> > Loading market...", end=' ')
    game.market.load() # Fails to load?
    print("%55s\n" % _txtColor("\t[DONE]", "blue"))
    print("> > Loading house data...", end=' ')
    for x in (yield houseData):
        game.house.houseData[int(x['id'])] = game.house.House(int(x['id']), int(x['owner']),x['guild'],x['paid'],x['name'],x['town'],x['size'],x['rent'],x['data'])
    print("%55s\n" % _txtColor("\t[DONE]", "blue"))

    # Load scripts
    print("> > Loading scripts...", end=' ')
    game.scriptsystem.importer()
    game.scriptsystem.get("startup").run()
    print("%55s\n" % _txtColor("\t[DONE]", "blue"))

    # Load map (if configurated to do so)
    if config.loadEntierMap:
        config.performSectorUnload = False 
        print("> > Loading the entier map...", end=' ')
        begin = time.time()
        files = glob.glob('%s/%s/*.sec' % (config.dataDirectory, config.mapDirectory))
        for fileSec in files:
            x, y, junk = fileSec.split(os.sep)[-1].split('.')
            x = int(x)
            y = int(y)
            iX = x // game.map.sectorX
            iY = y // game.map.sectorY
            sectorSum = (iX << 11) + iY
            game.map.load(x,y, 0, sectorSum, False)

        print("%50s\n" % _txtColor("\t[DONE, took: %f]" % (time.time() - begin), "blue"))

    # Charge rent?
    def _charge(house):
            call_later(config.chargeRentEvery, game.functions.looper, lambda: game.scriptsystem.get("chargeRent").run(house=house))

    for house in game.house.houseData.values():
        if not house.rent or not house.owner: continue

        if house.paid < (timer - config.chargeRentEvery):
            game.scriptsystem.get("chargeRent").run(house=house)
            _charge(house)
        else:
            call_later((timer - house.paid) % config.chargeRentEvery, _charge, house)

    # Load protocols
    print("> > Loading game protocols...", end=' ')
    for version in config.supportProtocols:
        game.protocol.loadProtocol(version)
    print("%50s\n" % _txtColor("\t[DONE]", "blue"))

    # Do we issue saves?
    if config.doSaveAll:
        print("> > Schedule global save...", end=' ')
        call_later(config.saveEvery, game.functions.looper, game.functions.saveAll, config.saveEvery)
        print("%50s\n" % _txtColor("\t[DONE]", "blue"))

    # Do we save on shutdowns?
    if config.saveOnShutdown:
        game.scriptsystem.get("shutdown").register(lambda **k: game.functions.saveAll(True), False)

    # Reset online status on shutdown
    game.scriptsystem.get("shutdown").register(lambda **k: sql.runOperation("UPDATE players SET online = 0"), False)
    # Light stuff
    print("> > Turn world time and light on...", end=' ')
    lightchecks = config.tibiaDayLength / float(config.tibiaFullDayLight - config.tibiaNightLight)

    call_later(lightchecks, game.functions.looper, game.functions.checkLightLevel, lightchecks)
    print("%45s" % _txtColor("\t[DONE]", "blue"))

    call_later(60, game.functions.looper, pathfinder.clear, 60)

    # Now we're online :)
    print(_txtColor("Message of the Day: %s" % config.motd, "red"))
    print("Loading complete in %fs, everything is ready to roll" % (time.time() - timer))
    global IS_ONLINE
    IS_ONLINE = True

    print("\n\t\t%s\n" % _txtColor("[SERVER IS NOW OPEN!]", "green"))


@gen.coroutine
def install_tables():
    print("\nRUNNING INSTALLER\n=================")
    print("Running installer queries...")
    queries = open("extra/sql/installer.sql", 'r').read().split(';')
    for query in queries:
         if query.strip():
             print(query)
             yield sql._runOperation(query.strip())

    queries = open("extra/sql/houses.sql", 'r').read().split(';')
    print("\n\nRunning house installer queries...")
    for query in queries:
         if query.strip():
             yield sql._runOperation(query.strip())

    # Install accounts:
    print("\nFirst account,")

    username = None
    while not username:
        username = config.first_account_name

    password = None
    while not password:
         password = config.first_account_password

    # Leave demo to en_EN for now.
    language = "en_EN"
    """language = input("Language [en_EN]? ")
    if not language:
         language = "en_EN"""

    # This is without salt, but is just a demo anyway.
    yield sql._runOperation("INSERT INTO `accounts` VALUES (1, %s, SHA1(%s), '', 65535, %s, 0, 1)", username, password, language)
