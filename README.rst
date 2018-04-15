Distlog
=======

Is a Python library and a set of applications to facilitate logging in a
distributed application.

The reason to create yet another logging tool arose while developing an
application based on (micro) services. Even though each component produces a
liberal amount of logging data making sense of it is challenging at times.

This is because each log file only tells part of the story.
The challenge is to find those parts of the log entries that are relevant to a
particular problem request. I tried to solve this by using correlation IDs.
These IDs are assigned when a request first enters the system and is passed on
to each service that is invoked to satisfy that request. It sort of works but it
takes a lot of time piecing all the bits together.

Hence the desire to let the system sort it out itself.

Requirements
============

My preferred solution should:

Interoperate
------------

Interoperate with Python's native logging library.
    This will automatically include logging activity from incorporated libraries
    which nearly always use Python's native logging support.

Distributed
-----------

Allow multiple clients to produce log entries.
    It is after all meant as a solution for a distributed application.

Centralize all logs in a single location.
    This will make it possible to combine entries from different sources
    relating to the same request.

Allow multiple clients to process the log entries.
    Some will store the log entries on permanent storage (file, database).
    Others may filter the entries and display them as if tailing a logfile.

Structured
----------

Offer additional structure to the log entries.
    Normal logs are a sequential but otherwise unstructured list of hopefully
    significant facts. What I'd like to see is that the log entries tell me what
    is being achieved and wheter that succeeded or not. Each of these goals may
    itself consist of subgoals creating a tree of goals which together reach a
    conclusion.

    For many years now we modularize and structure our code, yet none of that is
    visible in the log entries that tell us how the program is progressing.

The structure in the log entries should transcent process bounderies.
    When one process invokes the services of another process the structure of
    the log entries should reflect this. A process switch should not break the
    tree structure described above.

Dataset oriented
----------------

Support record logging.
    Traditionally log entries are supposed to be a single text string. I want to
    see all of Python's LogRecord fields in the log entry. And probably quite a
    few more fields as well. We can assume the LogRecord fields as a stable
    basis set of properties that are expanded by custom properties depending on
    the application and function.

Oh and the whole thing should be modular off course.
    - Structured logging
    - Multi process logging
    - Record logging

    Should be separate functional modules that can be combined to provide all of
    the above.

There is just one little thing: it doesn't exist. Yet.

The distlog package
====================
The distlog package exports a couple classes and functions:

* :class:`ZmqHandler`
    This is a handler for the standard Python logging library that transports
    :class:`LogRecords`. For it to work it needs a serializer that prepares the
    :class:`LogRecord` instances for transportation. This serializer should be
    derived from the :class:`~distlog.formatters.Serializer` class. Choose one
    of the predefined serializers :class:`JSONFormatter` or
    :class:`PickleFormatter` and set it as the formatter using
    :method:`ZmqHandler.setFormatter`.

* :class:`JSONFormatter`
    This is one of the predefined serializers, it converts a :class:`LogRecord`
    instances to JSON strings that can be sent via 0MQ.

* :class:`PickleFormatter`
    This is the other predefined serializer. it converts a :class:`LogRecord` to
    the binary Python specific pickle format. Note that the serialization method
    is part of the message so that the receiver knows how to deserialize the
    message.

* :function:`task`
    This function returns a :class:`Task` object that implements as a context
    handler and acts as the top level logging context for Pythons normal logger
    functions.

* :function:`to`
    This function returns a :class:`Task` instance that is a child of another
    logging context thus constructing a hierarchy of logging contexts.

* :function:`import_task`
    Creates a top level logging context that is subordinate to the logging
    context in a different process. Using :method:`Task.get_foreign_task` to
    obtain a task/context id, transferring this id from one process to another
    and passing it as parameter to :function:`import_task` it is possible to
    relate the activities across processes as belonging to one and the same
    activity.

Logging infrastructure
======================
The process(es) forming the application that is being logged send out their log
messages using :class:`ZmqHandler`. This class sends the message out using a
0MQ PUSH socket that binds to the well-known address of the corresponding PULL
socket of the `distlogd` process.

The `distlogd` process receives all log messages and filters them using a
configurable rule set. Based on the rule(s) which triggered, the message is
forwarded to one or more processors.

The configuration file, probably a YAML file, may instruct `distlogd` to load
processors as plugins. A processor will apply one or more filters on a message
and uses the outcome to decide to handle a message or not.
