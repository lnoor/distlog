Distlog
=======

A logging system with an attitude for distributed software systems.

Features
--------

Distlog (Python package)
++++++++++++++++++++++++

*   Fully compatible with the standard Python logging package.

*   Structured logging: Next to the ubiquitous log message, Distlog allows you
    to incorporate entire data sets in your log message.

*   Scoped logging messages: Log messages can be structured in a tree like
    fashion. A task consisting of multiple subtasks, all producing log
    messages can be displayed as a tree the branches (subtasks) of which
    containing the leaves (log messages) can be folded and unfolded to show
    relevant or hide irrelevant messages.

*   Scoped logging also works over process boundaries. A software system
    using a services architecture can create a coherent view of its execution
    where a service, possible executing on another host, is displayed as a
    subtask in the log message tree for a task.

*   Implements a handler that uses ØMQ to send and collect log messages from all
    components of the distributed application.

Distlogd (daemon)
+++++++++++++++++

*   Collects all log messages sent by Distlog over ØMQ.

*   Uses a plugin architecture where each plugin gets to process all incoming
    messages. Plugins can then decide if and how to process a message.

*   Contains predefined plugins to store the messages in a file, a MongoDB
    or Redis database or to publish them using ØMQ's PUB/SUB mechanism.

*   Distlogd and its plugins are configurable using a YAML configuration file.

Contents
--------

.. toctree::
    intro
    tutorial
    organization
    distlog
    distlogd
    plugins


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

