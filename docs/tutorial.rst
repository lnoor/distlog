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
        "context": {
            "key": "0@e252a11f-d33d-483d-ba08-bc8f642b2f10",
            "user": "leo"
        },
        "filename": "example.py",
        "funcName": "main",
        "stack_info": null,
        "args": null,
        "process": 6156,
        "hostname": "obelix",
        "msecs": 148.06699752807617,
        "message": "toplevel",
        "name": "root",
        "module": "example",
        "thread": 139753641113344,
        "msg": "toplevel",
        "lineno": 13,
        "threadName": "MainThread",
        "exc_text": null,
        "exc_info": null,
        "levelno": 20,
        "asctime": "2018-04-18 23:03:19,148",
        "relativeCreated": 379328.7272453308,
        "levelname": "INFO",
        "processName": "MainProcess",
        "created": 1524085399.148067,
        "pathname": "/home/leo/src/distlog/example.py"
    }

This is basically Python's LogRecord structure. It has an extra field `context`
containing the additional keyword argument and a `key` field which is used to
correlate the messages.

The `key` field consists of three parts:

* message sequence number
* unique toplevel scope identification
* optional subscope sequence number


The other JSON messages are:

.. code-block:: json

    {
        "context": {
            "key": "1@e252a11f-d33d-483d-ba08-bc8f642b2f10",
            "user": "leo"
        },
        "filename": "example.py",
        "funcName": "main",
        "stack_info": null,
        "args": null,
        "process": 6156,
        "hostname": "obelix",
        "msecs": 824.9077796936035,
        "message": "into task",
        "name": "root",
        "module": "example",
        "thread": 139753641113344,
        "msg": "into task",
        "lineno": 15,
        "threadName": "MainThread",
        "exc_text": null,
        "exc_info": null,
        "levelno": 20,
        "asctime": "2018-04-18 23:06:30,824",
        "relativeCreated": 571005.5680274963,
        "levelname": "INFO",
        "processName": "MainProcess",
        "created": 1524085590.8249078,
        "pathname": "/home/leo/src/distlog/example.py"
    }

.. code-block:: json

    {
        "context": {
            "key": "0@e252a11f-d33d-483d-ba08-bc8f642b2f10/1",
            "arg": 42
        },
        "filename": "example.py",
        "funcName": "main",
        "stack_info": null,
        "args": null,
        "process": 6156,
        "hostname": "obelix",
        "msecs": 113.48962783813477,
        "message": "subtask",
        "name": "root",
        "module": "example",
        "thread": 139753641113344,
        "msg": "subtask",
        "lineno": 16,
        "threadName": "MainThread",
        "exc_text": null,
        "exc_info": null,
        "levelno": 20,
        "asctime": "2018-04-18 23:07:18,113",
        "relativeCreated": 618294.1498756409,
        "levelname": "INFO",
        "processName": "MainProcess",
        "created": 1524085638.1134896,
        "pathname": "/home/leo/src/distlog/example.py"
    }

.. code-block:: json

    {
        "context": {
            "key": "1@e252a11f-d33d-483d-ba08-bc8f642b2f10/1",
            "arg": 42
        },
        "filename": "example.py",
        "funcName": "main",
        "stack_info": null,
        "args": null,
        "process": 6156,
        "hostname": "obelix",
        "msecs": 585.9096050262451,
        "message": "into task",
        "name": "root",
        "module": "example",
        "thread": 139753641113344,
        "msg": "into task",
        "lineno": 18,
        "threadName": "MainThread",
        "exc_text": null,
        "exc_info": null,
        "levelno": 20,
        "asctime": "2018-04-18 23:07:35,585",
        "relativeCreated": 635766.569852829,
        "levelname": "INFO",
        "processName": "MainProcess",
        "created": 1524085655.5859096,
        "pathname": "/home/leo/src/distlog/example.py"
    }

.. code-block:: json

    {
        "context": {
            "key": "2@e252a11f-d33d-483d-ba08-bc8f642b2f10/1",
            "arg": 42
        },
        "filename": "example.py",
        "funcName": "main",
        "stack_info": null,
        "args": null,
        "process": 6156,
        "hostname": "obelix",
        "msecs": 411.38386726379395,
        "message": "subtask done",
        "name": "root",
        "module": "example",
        "thread": 139753641113344,
        "msg": "subtask done",
        "lineno": 19,
        "threadName": "MainThread",
        "exc_text": null,
        "exc_info": null,
        "levelno": 20,
        "asctime": "2018-04-18 23:08:13,411",
        "relativeCreated": 673592.0441150665,
        "levelname": "INFO",
        "processName": "MainProcess",
        "created": 1524085693.4113839,
        "pathname": "/home/leo/src/distlog/example.py"
    }

Note that the message shows the contents of the success() parameters.

.. code-block:: json

    {
        "context": null,
        "filename": "example.py",
        "funcName": "main",
        "stack_info": null,
        "args": null,
        "process": 6156,
        "hostname": "obelix",
        "msecs": 740.2544021606445,
        "message": "all done",
        "name": "root",
        "module": "example",
        "thread": 139753641113344,
        "msg": "all done",
        "lineno": 21,
        "threadName": "MainThread",
        "exc_text": null,
        "exc_info": null,
        "levelno": 20,
        "asctime": "2018-04-18 23:08:52,740",
        "relativeCreated": 712920.9146499634,
        "levelname": "INFO",
        "processName": "MainProcess",
        "created": 1524085732.7402544,
        "pathname": "/home/leo/src/distlog/example.py"
    }

Outside of any context so the `context` field is null/None.
