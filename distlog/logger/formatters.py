#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Encode log messages for network transport.

The log entry formatters in this module take a LogRecord obect
and encode it for network transportation.

"""

__copyright__ = "Copyright (C) 2017 Leo Noordergraaf"
__licence__ = "GNU General Public Licence v3"

import logging
import os
import pickle
try:
    import jsonext as json
except ImportError:
    import json


class Serializer(logging.Formatter):

    """Common base class for formatters."""

    def _extract_record(self, record):
        """Extract the data from a LogRecord.

        Logging data is collected in a LogRecord.
        This function readies it for transmission.
        The receiver may not be able to deal with LogRecords,
        exception info and timestamps therefore these are
        converted into text, escaping any newlines.

        Additionally, the name of the host generating this
        message is added as well as the process id.

        :param record: LogRecord instance
        :return: A dict with the massaged record contents.

        """
        record.message = record.getMessage().replace('\n', '\\n')
        record.asctime = self.formatTime(record, self.datefmt)
        record.hostname = os.uname().nodename
        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info).\
                    replace('\n', '\\n')
        record.exc_info = None
        record.args = None
        return record.__dict__

    @property
    def encoding(self):
        """Describe the encoding used."""
        raise NotImplementedError()


class JSONFormatter(Serializer):

    """Formatter to convert to JSON format."""

    def format(self, record):
        """Format to JSON.

        Use the logging Formatter to convert the
        LogRecord data to JSON for network transport.

        :param record: LogRecord instance
        :return: JSON encoded record contents.

        """
        return json.dumps(self._extract_record(record))

    @property
    def encoding(self):
        """Describe the encoding used.

        :return string: encoding indicator

        """
        return 'J'


class PickleFormatter(Serializer):

    """Formatter to convert to pickle format."""

    def format(self, record):
        """Format to pickle.

        Use the logging Formatter to convert the
        LogRecord data to pickle format or network transport.

        :param record: LogRecord instance
        :return: pickled record contents.

        """
        return pickle.dumps(self._extract_record(record), 3)

    @property
    def encoding(self):
        """Describe the encoding used.

        :return string: encoding indicator

        """
        return 'P'
