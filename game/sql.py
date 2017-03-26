import os
import sys
import time
from collections import deque

from tornado import gen, ioloop
from tornado.gen import Return

import config

connections = None

if config.sqlModule == "mysql":
    connections = deque(maxlen=10)
    
    @gen.coroutine
    def connect():
        # I hate doing this but I have no choice
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__name__)), 'game'))
        import asynctorndb
        # Try one connection first.
        conn = asynctorndb.Connect(host=config.sqlHost, user=config.sqlUsername, passwd=config.sqlPassword,
                                   database=config.sqlDatabase, no_delay = False, charset='utf8')
        spawn = config.sqlConnections
        future = conn.connect()
        try:
            yield future
        except:
            pass

        if future.exception():
            print("SQL Connection to localhost failed, trying 127.0.0.1")
            if config.sqlHost == "localhost":
                config.sqlHost = "127.0.0.1"
                print("SQL Connection with localhost failed, trying 127.0.0.1")
        else:
            spawn -= 1
            connections.append(conn)

        # Make connection pool.
        for x in range(spawn):
            conn = asynctorndb.Connect(host = config.sqlHost, user=config.sqlUsername, passwd=config.sqlPassword, database=config.sqlDatabase, no_delay = False, charset='utf8')

            future = conn.connect()
            try:
                yield future
            except:
                pass

            if future.exception():
                print("SQL Connection failed", future.exception(), "check SQL settings in config.py!")
                sys.exit()
            else:
                connections.append(conn)

    def runOperation(*argc):
        ioloop.IOLoop.instance().add_callback(_runOperation, *argc)

    @gen.coroutine
    def _runOperation(*argc):
        # Get a connection.
        conn = None
        while not conn:
            try:
                conn = connections.popleft()
            except:
                conn = None

            if not conn:
                yield gen.Task(ioloop.IOLoop.instance().add_timeout, time.time() + 0.05)

        future = conn.execute(*argc)
        try:
            yield future
        except:
            pass


        exc = future.exc_info()
        if exc:
            print(exc[0].__name__, exc[1], 'from query:', argc[0])

        # Put connection back
        connections.append(conn)

    @gen.coroutine
    def runQuery(*argc):
        # Get a connection.
        conn = None
        while not conn:
            try:
                conn = connections.popleft()
            except:
                conn = None

            if not conn:
                yield gen.Task(ioloop.IOLoop.instance().add_timeout, time.time() + 0.05)

        future = conn.query(*argc)
        try:
            res = yield future
        except:
            res = None

        exc = future.exc_info()
        if exc:
            print(exc[0].__class__.__name__, exc[1], 'from query:', argc[0])
        exc = future.exception()



        # Put connection back
        connections.append(conn)

        raise Return(res)

    @gen.coroutine
    def runQueryWithException(*argc):
        # Get a connection.
        conn = None
        while not conn:
            try:
                conn = connections.popleft()
            except:
                conn = None

            if not conn:
                yield gen.Task(ioloop.IOLoop.instance().add_timeout, time.time() + 0.05)

        future = conn.query(*argc)

        yield future
        # Put connection back
        connections.append(conn)

        raise Return(future)

    @gen.coroutine
    def runOperationLastId(*argc):
        # Get a connection.
        conn = None
        while not conn:
            try:
                conn = connections.popleft()
            except:
                conn = None

            if not conn:
                yield gen.Task(ioloop.IOLoop.instance().add_timeout, time.time() + 0.05)

        future = conn.execute_lastrowid(*argc)

        try:
            res = yield future
        except:
            res = None
        exc = future.exc_info()
        if exc:
            print(exc[0].__class__.__name__, exc[1], 'from query:', argc[0])
        # Put connection back
        connections.append(conn)

        raise Return(res)

elif config.sqlModule == "tornado-mysql":
    from tornado_mysql import pools, cursors
    # Fix windows.
    if config.sqlHost == "localhost":
        config.sqlHost = "127.0.0.1" 

    @gen.coroutine
    def connect():
        global connections
        connections = pools.Pool(dict(host=config.sqlHost, user=config.sqlUsername, passwd=config.sqlPassword, db=config.sqlDatabase, cursorclass=cursors.DictCursor, no_delay=True), max_idle_connections=config.sqlConnections)
        yield connections._get_conn()
        
    def runOperation(*argc):
        ioloop.IOLoop.instance().add_callback(_runOperation, *argc)

    @gen.coroutine
    def _runOperation(query, *argc):
        future = connections.execute(query, argc)
        try:
            yield future
        except:
            pass


        exc = future.exc_info()
        if exc:
            print(exc[0].__name__, exc[1], 'from query:', argc[0])

    @gen.coroutine
    def runQuery(query, *argc):
        future = connections.execute(query, argc)
        try:
            res = yield future
        except:
            res = None

        exc = future.exc_info()
        if exc:
            print(exc[0].__class__.__name__, exc[1], 'from query:', argc[0])
        exc = future.exception()


        raise Return(res.fetchall())

    @gen.coroutine
    def runQueryWithException(query, *argc):
        future = connections.execute(query, argc)

        yield future

        raise Return(future)

    @gen.coroutine
    def runOperationLastId(query, *argc):

        future = connections.execute(query, argc)

        try:
            res = yield future
        except:
            res = None
        exc = future.exc_info()
        if exc:
            print(exc[0].__class__.__name__, exc[1], 'from query:', argc[0])
        # Put connection back
        connections.append(conn)

        raise Return(res.lastrowid)
else:
    raise ImportError("Unsupported sqlModule!")
