#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import time
import json
from threading import Thread

import zmq
from zmq.utils.strtypes import cast_unicode


from distlog.logger.handler import ZmqHandler
from distlog.logger.formatters import JSONFormatter

CONNECTPOINT = "tcp://localhost:6001"
BINDPOINT = "tcp://*:6001"

def publisher_thread():
    handler = ZmqHandler(CONNECTPOINT,  zmq.Context())
    handler.setFormatter(JSONFormatter())

    time.sleep(1)

    for i in range(10):
        record = logging.LogRecord('name', 20, '/here/and/nowhere/else.py', 50, 'hi there %s %d', ('number', 1), None)
        handler.emit(record)
    handler = None

def subscriber_thread():
    ctx = zmq.Context()
    subscriber = ctx.socket(zmq.PULL)
    subscriber.bind(BINDPOINT)

    count = 0
    while True:
        if count == 10:
            break

        msg = subscriber.recv_multipart()
        assert msg[0] == b'PLJ'
        data = json.loads(cast_unicode(msg[1]))
        assert data['name'] == 'name'
        assert data['levelno'] == 20
        assert data['filename'] == 'else.py'
        assert data['module'] == 'else'
        assert data['lineno'] == 50
        assert data['message'] == 'hi there number 1'
        count += 1


def test_handler():
    p_thread = Thread(target=publisher_thread)
    p_thread.start()

    # Do NOT use a thread for the code containing the asserts,
    # the exceptions will not be passed to the main thread.
    subscriber_thread()
    p_thread.join()

if __name__ == '__main__':
    test_handler()
