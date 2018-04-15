Introduction
============

Distlog grew out of the frustration of working with the log files of a
software system consisting of multiple cooperating processes, so-called
microservices.

In order to track a request from the moment a client issued it all through
its resolution and response consisted of searching through about half a
dozen log files in multiple hosts all handling multiple requests concurrently.

Earlier attempts
----------------

Searching the net quickly showed that I wasn't the only frustrated programmer.
Among others I found structlog_, Logbook_ and Eliot_.
From them I learned about structured logging.

To me the phrase 'structured logging' has a double meaning.
One the one hand it means that log messages can be enhanced, or even replaced by
a dataset.
On the other that the log messages themselves are structured, nested if you
will. I will refer to this structure as scoping.

Both ideas appealed hugely to me and they cooperate nicely as the data
structures are used to record the parent/child relationschip between log
messages.

Still not happy
---------------

Yet all the mentioned solutions where lacking.
Either it replaced the standard Python logging module used by nearly all
packages. That would limit the usefullness of the logging messages since all
messages from external packages are excluded and must be processed and
correlated by hand as before.
Or the solution will not work nicely over processes.

All solutions suffered that they focussed mostly on *generating* log messages
but most of the work is in *processing* the messages.
You want to filter and drill down on messages because you want to look only at
that part of the system where an error occurs.
Or log messages are used for other purposes such as collecting usage and
performance data and you want those to be kept for a longer period and displayed
in some dashboard whereas regular logging messages can be discarded after a few
days.

Requirements
------------

Thus grew the idea that a logging system for a distributed application is in
itself quite a system. It needs to:

#.  Generate (standard Python) log messages.
#.  Scope log messages.
#.  Extend log messages with additional data.
#.  Collect those log messages in a central location.
#.  Filter, store and/or redistribute those log messages.
#.  Display log messages in a GUI or on a console and allow selection of
    relevant messages.
#.  It should be able to influence message generation dynamically. So some parts
    of the system may produce DEBUG messages while others are less verbose.

The Distlog package implements the first three items, Distlogd the next two.
There is still some work to do.


.. _structlog: https://structlog.readthedocs.io/en/stable/index.html
.. _Logbook: http://logbook.readthedocs.io/en/stable/index.html
.. _Eliot: https://eliot.readthedocs.io/en/1.3.0/#
