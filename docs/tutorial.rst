Tutorial
========

This tutorial tries to give you a taste of what it will be like to use this
system. At the same time it also allows to collect and refine my ideas.
The contents of this section is far from stable.

Loading and initializing distlog:

.. code-block:: python
    :linenos:
    :emphasize-lines: 5-6

    import logging
    import distlog

    logger = logging.getLogger()
    handler = distlog.ZmqHandler('tcp://localhost:5010')
    handler.setFormatter(distlog.JSONFormatter())
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

On line 5 the ØMQ handler is created and intialized. It will bind to the
Distlogd daemon listening on port 5010 on the local host.

Line 6 sets the formatter to the JSON encoder. You may also choose to use the
faster pickle encoder.

Using distlog:

.. code-block:: python
    :linenos:
    :lineno-start: 10
    :emphasize-lines: 2,5, 8

    def main():
        with distlog.task('toplevel', user='leo') as job:
            print('into task')
            logger.info('into task')
            with distlog.to('subtask', arg=42) as job:
                print('into subtask')
                logger.info('into task')
                job.success('subtask done')
        print('all done')
        logger.info('all done')

    if __name__ == '__main__':
        main()

.. sidebar:: Attitude

    I said Distlog has something of an attitude.
    And here it is.
    It assumes that you structure your program by stating its purpose, its task,
    and then proceed by implementing this task using smaller subtasks::

        with task('BEING IMPORTANT'):
            with to('appear important'):
                with to('dress up'):
                    pass

    In other words each subtask of your program is encapsulated in a Distlog
    context. --I use context and scope interchangeably to mean the same thing.

On line 11 the task is defined. This is the outermost scope of the logging tree.
The string becomes part of the task initiation termination messages.
Any positional arguments are assumed to be format parameters for the message
just as with the regular Python logging system.
But all keyword arguments are stashed away and added to all log messages that
are generated in this scope. Here that is only happens on line 13.

On line 14 a new scope is created as a child of the toplevel scope of line
11. The set of keyword arguments replaces those of the outer scope.
You can always find them through the encompassing scope.

On line 17 the inner scope is given a new logging message to use if the subtask
completes without an exception.

Finally on line 19 a log message is produced which is outside the toplevel scope.

When this program is run the console will display::

    into task
    into subtask
    all done

Over the ØMQ socket the following messages are sent (pretty printed):

.. code-block:: json

    {
        "exc_info": null,
        "process": 13732,
        "processName": "MainProcess",
        "module": "context",
        "name": "root",
        "created": 1523718349.0820286,
        "levelname": "INFO",
        "args": null,
        "filename": "context.py",
        "context": {
            "user": "leo",
            "key": "0@81a5da22-7600-4085-a5dd-78ca1c1682b7"
        },
        "asctime": "2018-04-14 17:05:49,082",
        "funcName": "__enter__",
        "lineno": 188,
        "hostname": "obelix",
        "msg": "toplevel",
        "levelno": 20,
        "threadName": "MainThread",
        "pathname": "/home/leo/src/distlog/distlog/logger/context.py",
        "relativeCreated": 129673.73085021973,
        "exc_text": null,
        "stack_info": null,
        "message": "toplevel",
        "thread": 140384598415104,
        "msecs": 82.02862739562988
    }

This is basically Python's LogRecord structure. It has an extra field `context`
containing the additional keyword argument and a `key` field which is used to
correlate the messages.

The `key` field consists of three parts:

* message sequence number
* unique toplevel scope identification
* subscope sequence number

Sidenote:
    Clearly the fields `funcName`, `lineno`, `module`, `filename` and `pathname`
    need more work to display correct values.

The other JSON messages are:

.. code-block:: json

    {
        "exc_info": null,
        "process": 13732,
        "processName": "MainProcess",
        "module": "example",
        "name": "root",
        "created": 1523718609.7217119,
        "levelname": "INFO",
        "args": null,
        "filename": "example.py",
        "context": {
            "user": "leo",
            "key": "1@81a5da22-7600-4085-a5dd-78ca1c1682b7"
        },
        "asctime": "2018-04-14 17:10:09,721",
        "funcName": "main",
        "lineno": 15,
        "hostname": "obelix",
        "msg": "into task",
        "levelno": 20,
        "threadName": "MainThread",
        "pathname": "/home/leo/src/distlog/example.py",
        "relativeCreated": 390313.4140968323,
        "exc_text": null,
        "stack_info": null,
        "message": "into task",
        "thread": 140384598415104,
        "msecs": 721.7118740081787
    }

.. code-block:: json

    {
        "exc_info": null,
        "process": 13732,
        "processName": "MainProcess",
        "module": "context",
        "name": "root",
        "created": 1523718709.0561981,
        "levelname": "INFO",
        "args": null,
        "filename": "context.py",
        "context": {
            "arg": 42,
            "key": "0@81a5da22-7600-4085-a5dd-78ca1c1682b7/1"
        },
        "asctime": "2018-04-14 17:11:49,056",
        "funcName": "__enter__",
        "lineno": 188,
        "hostname": "obelix",
        "msg": "subtask",
        "levelno": 20,
        "threadName": "MainThread",
        "pathname": "/home/leo/src/distlog/distlog/logger/context.py",
        "relativeCreated": 489647.9003429413,
        "exc_text": null,
        "stack_info": null,
        "message": "subtask",
        "thread": 140384598415104,
        "msecs": 56.1981201171875
    }

.. code-block:: json

    {
        "exc_info": null,
        "process": 13732,
        "processName": "MainProcess",
        "module": "example",
        "name": "root",
        "created": 1523718738.5430636,
        "levelname": "INFO",
        "args": null,
        "filename": "example.py",
        "context": {
            "arg": 42,
            "key": "1@81a5da22-7600-4085-a5dd-78ca1c1682b7/1"
        },
        "asctime": "2018-04-14 17:12:18,543",
        "funcName": "main",
        "lineno": 18,
        "hostname": "obelix",
        "msg": "into task",
        "levelno": 20,
        "threadName": "MainThread",
        "pathname": "/home/leo/src/distlog/example.py",
        "relativeCreated": 519134.7658634186,
        "exc_text": null,
        "stack_info": null,
        "message": "into task",
        "thread": 140384598415104,
        "msecs": 543.0636405944824
    }

.. code-block:: json

    {
        "exc_info": null,
        "process": 13732,
        "processName": "MainProcess",
        "module": "context",
        "name": "root",
        "created": 1523718879.3886158,
        "levelname": "INFO",
        "args": null,
        "filename": "context.py",
        "context": {
            "arg": 42,
            "key": "2@81a5da22-7600-4085-a5dd-78ca1c1682b7/1"
        },
        "asctime": "2018-04-14 17:14:39,388",
        "funcName": "__exit__",
        "lineno": 207,
        "hostname": "obelix",
        "msg": "subtask done",
        "levelno": 20,
        "threadName": "MainThread",
        "pathname": "/home/leo/src/distlog/distlog/logger/context.py",
        "relativeCreated": 659980.318069458,
        "exc_text": null,
        "stack_info": null,
        "message": "subtask done",
        "thread": 140384598415104,
        "msecs": 388.61584663391113
    }

.. code-block:: json

    {
        "exc_info": null,
        "process": 13732,
        "processName": "MainProcess",
        "module": "example",
        "name": "root",
        "created": 1523718913.026932,
        "levelname": "INFO",
        "args": null,
        "filename": "example.py",
        "context": null,
        "asctime": "2018-04-14 17:15:13,026",
        "funcName": "main",
        "lineno": 21,
        "hostname": "obelix",
        "msg": "all done",
        "levelno": 20,
        "threadName": "MainThread",
        "pathname": "/home/leo/src/distlog/example.py",
        "relativeCreated": 693618.634223938,
        "exc_text": null,
        "stack_info": null,
        "message": "all done",
        "thread": 140384598415104,
        "msecs": 26.9320011138916
    }
