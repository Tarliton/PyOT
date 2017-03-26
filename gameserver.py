import signal
import sys
import time

import tornado.log
from tornado.tcpserver import IOLoop

from game import loading, scriptsystem
from game.service.gameserver import GameFactory
from game.service.loginserver import LoginFactory

try:
    import config
except ImportError:
    print("You got no config.py file. Please make a file from config.py.dist")
    sys.exit()

tornado.log.enable_pretty_logging()

if __name__ == '__main__':
    startTime = time.time()
    # Game Server
    gameServer = GameFactory()
    gameServer.bind(config.gamePort, config.gameInterface)
    gameServer.start()

    # Login Server
    loginServer = LoginFactory()
    loginServer.bind(config.loginPort, config.loginInterface)
    loginServer.start()

    # Load the core stuff!
    IOLoop.instance().add_callback(loading.loader, startTime)

    # Start reactor. This will call the above.
    signal.signal(signal.SIGINT, scriptsystem.shutdown)
    signal.signal(signal.SIGTERM, scriptsystem.shutdown)
    IOLoop.instance().start()
