#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Publish log messages via 0MQ.

The LogRecord contents are, once properly formatter,
sent out using 0MQ.

"""

__copyright__ = "Copyright (C) 2017 Leo Noordergraaf"
__licence__ = "GNU General Public Licence v3"

import logging

import zmq
from zmq.utils.strtypes import cast_bytes

from .formatters import Serializer

TOPIC_SEPARATOR = ''
TOPIC_SYSTEM = 'TSP'
TOPIC_ENCODING = 'JP'
TOPIC_LOGGING = 'L'
TOPIC_PERFORMANCE = 'P'
"""Message topics.

Message topics are used to describe the contents of the
next fragment. It consists of three parts SYSTEM, KIND
and ENCODING. The parts are separated by the TOPIC_SEPARATOR.

A client subscribes to these topics and only receives those
messages to which it subscribed.

The SYSTEM topic is one of the letters TSP which stand for:

(T)est
    The test environment.
    The systems used for unit and integration testing.

(S)taging
    The staging (acceptation) environment.
    The systems used for functional and acceptance testing.

(P)roduction
    The production environment.
    The place where the software becomes the cash cow.

The KIND defines the kind of message:

(L)og message
    An (extended) LogRecord.
    A regular python logging message.

(P)erformance message
    A special kind of message.
    These messages contain data on performance subjects suitable for
    display in some fancy dashboard application. Since these messages
    share most if not all the requirements of normal log messages it
    makes sense to let them share the infrastructure.

Finally the ENCODING defines how the message is transferred:

(J)SON
    The LogRecord structure is encoded using JSON.
    This allows non python programs to generate or process the messages.

(P)ickle
    Python's own serialization method.
    Python specific but smaller and faster than JSON.
"""


class ZmqHandler(logging.Handler):

    """0MQ transport implementation."""

    log_topic = None
    perf_topic = None
    socket = None
    context = None

    def __init__(self, endpoint, context=None, system='P'):
        """Create a ZmqHandler.

        This creates the 0MQ PUSH socket and connects its with an endpoint.
        :param string endpoint: A 0MQ endpoint like `tcp://localhost:11223`.
        :param socket endpoint: An endpoint can also be a connected socket.
        :param context: A ZMQ context.

        """
        super().__init__()

        assert system in TOPIC_SYSTEM
        self._system = system

        if isinstance(endpoint, zmq.Socket):
            self.socket = endpoint
            self.context = self.socket.context
        else:
            self.context = context or zmq.Context.instance()
            self.socket = self.context.socket(zmq.PUSH)
            self.socket.connect(endpoint)

    def set_topic(self, encoding):
        """Set message topic elements.

        Creates the topic strings for log and performance messages.
        :param system: the system topic
        :param encoding: the encoding topic

        """
        assert encoding in TOPIC_ENCODING

        self.log_topic = TOPIC_SEPARATOR.join(
            [self._system, TOPIC_LOGGING, encoding]
        )

    def emit(self, record):
        """Do whatever it takes to actually log the specified logging record.
        """
        try:
            bmsg = cast_bytes(self.format(record))
            btopic = cast_bytes(self.log_topic)
        except Exception:
            self.handleError(record)
            return
        self.socket.send_multipart([btopic, bmsg])

    def setFormatter(self, fmt):  # noqa
        """Set the formatter for this handler."""
        if not isinstance(fmt, Serializer):
            raise TypeError('setFormatter of ZmHandler expects a Serializer'
                            ' derived object')
        super(ZmqHandler, self).setFormatter(fmt)
        self.set_topic(fmt.encoding)

#    def send_perf_data(self, data):
#        bdata = cast_bytes(data)
#        btopic = cast_bytes(self.perf_topic)
#
#        self.socket.send_multipart([btopic, bdata])
