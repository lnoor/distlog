#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Create a context for hierarchical logging.

Context for a log message is where it is produced in relation to what
other messages and functions.

Basically this module allows you to state what you want to achieve and
use the log messages to record the progress toward that goal.
A goal is usually defined in the terms of more primitive goals.
The whole set of goal and subgoals is considered the context of the log
message.
"""

__copyright__ = "Copyright (C) 2017 Leo Noordergraaf"
__licence__ = "GNU General Public Licence v3"

import logging
import uuid
import six


class LogRecord(logging.LogRecord):

    """
    :py:class:`~logging.LogRecord` replacement.

    This class replaces the standard :py:class:`~logging.LogRecord` class.
    It provides a single change: when an instance is created the instance is
    extended with a context attribute containing the current scope's context.
    """

    def __init__(
        self,
        name, level, pathname, lineno,
        msg, args, exc_info,
        func=None, sinfo=None, **kwargs
    ):
        super().__init__(
            name, level, pathname, lineno,
            msg, args, exc_info,
            func, sinfo, **kwargs
        )
        self.context = _context.top.context if _context.top else None


class Task(object):

    """
    Define the scope and context for other tasks and log messages.

    A :py:class:`~distlog.Task` defines the context for other tasks and log
    messages. It is a context manager that is ususally created by calling
    one of the functions :py:func:`~distlog.task` or :py:func:`~distlog.to`
    where :py:func:`~distlog.task` creates a new top-level context
    and :py:func:`~distlog.to` creates a subtask.

    The only real difference between the two is the way the id parameter is
    defined. A :py:func:`~distlog.task` creates a UUID as id and
    :py:func:`~distlog.to` creates a sequence number as id.
    :py:func:`~distlog.import_task` is an alternative for
    :py:func:`~distlog.to`, to be used when the subtask resides in another
    process.

    When the :py:func:`__enter__` method of the :py:class:`~distlog.Task` is
    called it will emit a log message at INFO level signalling the begin of the
    scope. Thereafter all log messages will belong to the same scope until a
    subtask is created with the :py:func:`~distlog.to` function or until the
    `with` section terminates.

    When the :py:func:`__exit__` method of the :py:class:`~distlog.Task` is
    called another log message at the INFO level signals the completion of the
    scope. The cause of leaving the `with` section, with an exception
    or normally, controls which log message is produced.

    :param string _id: Either absolute (task) or relative (to) task id.
    :param string msg: Task description, may contain % formatting.
    :param list args: Parameters for the msg parameter.
    :param dict kwargs: Context definition.
        You may provide as many named parameters as needed.
        They are stored as key/value pairs in the context
        and are added to the :py:class:`~distlog.LogRecord` when it is created.
    """

    def __init__(self, _id, msg, *args, **kwargs):
        self._id = _id
        self._parent = None
        self.msg = msg
        self.args = args
        self.data = kwargs
        self.smsg = None
        self.sargs = None
        self.counter = 0
        self.tasks = 0

    @property
    def id(self):
        """
        Property produces the context's unique id.

        :vartype string: scope (task/subtask) id.
        """
        if self.parent:
            return '{0}/{1}'.format(self.parent, self._id)
        else:
            return self._id

    @property
    def parent(self):
        """
        Parent id if available.

        Provides the value of the parents :py:attr:`~distlog.Task.id`
        property or `None` if there is no parent.

        :vartype: string Id of the parent component.
        """
        return self._parent.id if self._parent else None

    @property
    def context(self):
        """
        Assemble the context.

        The assembled context is added to the :py:class:`~distlog.LogRecord`
        instance as the `context` attribute.
        The assembly consists of the key identifying this log entry
        with the data provided when creating the context and any
        data added to it by the :py:func:`~distlog.Task.bind` function.

        :vartype: dict containing the context data.
        """
        data = {
            'key': '{0}@{1}'.format(self.counter, self.id)
        }
        self.counter += 1
        data.update(self.data)
        return data

    def get_next_task(self):
        """
        Identify the new subtask.

        Every subtask spawned from this scope is identified by the current
        scopes identifier suffixed by the subtask sequence number.
        This method increments that sequence number to create a new scope.

        :return int: subtask sequence number.
        """
        self.tasks += 1
        return self.tasks

    def get_foreign_task(self):
        """
        Determine task id for a foreign task.

        The returned ID can be passed over the network in an undefined
        manner and used on the other side as the first parameter for the
        function :py:func:`~distlog.import_task`.
        Doing so will link both tasks (although in separate processes)
        toghether in one related set of log messages.

        :return string: child task identification string.

        """
        _id = self.get_next_task()
        return '{0}/{1}'.format(self.parent, _id)

    def bind(self, **kwargs):
        """
        Add key/value pairs to the context.

        Add the key/value pairs in kwargs to the dataset that
        is eventually returned by the context property.

        :param dict kwargs: dict with key/value pairs
        """
        self.data.update(kwargs)

    def success(self, msg, *args):
        """
        Set success report message.

        When the context manager is terminated successfully and
        :py:func:`~distlog.Task.success` has been called on the context then the
        `msg` is used to report the status in a log message.

        :param string msg: The log message to display
        :param list args: optional format parameters for the msg
        """
        self.smsg = msg
        self.sargs = args

    def __enter__(self):
        """
        Add this task to the context.

        By entering this context manager the task is added to the
        context of log messages and its contents are automatically
        included in log messages.

        :rtype: Task
        """
        _context.push(self)
        logging.info(self.msg, *self.args)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Drop task from the context.

        When the context manager is terminated it removes itself
        from the log message context and the task becomes eligable
        for garbage collection.

        :param exc_type: see context manager
        :param exc_value: see context manager
        :param traceback: see context manager
        :rtype: bool False, do not interfere with exceptions
        """
        if exc_type:
            logging.exception('FAILED ' + self.msg, *self.args)
        elif self.smsg:
            logging.info(self.smsg, *self.sargs)
        _context.pop()
        return False


class LogContext(object):

    """
    Log message context.

    The log message context is a stack of :py:class:`~distlog.Task` entries.
    Tasks form the context for individual log messages.
    Tasks can be constructed from subtasks which is why a stack structure is
    required.

    The :py:class:`~distlog.LogContext` itself is a class with only a single
    instance which acts as a singleton and is defined as a module global
    in this file.
    """

    def __init__(self):
        self.context = list()

    def push(self, action):
        """
        Push element onto the stack.

        :param action: item to add to the stack.
        :type action: :py:class:`~distlog.Task`
        """
        action._parent = self.top
        self.context.append(action)

    def pop(self):
        """
        Remove top element of the stack.

        Pop and return the topmost element of the stack.

        :rtype: :py:class:`~distlog.Task` the removed element.
        """
        action = self.context.pop()
        action._parent = None
        return action

    @property
    def top(self):
        """
        Produce element on top of stack.

        :vartype: :py:class:`~distlog.Task` the element on top of the stack.
        """
        if len(self.context) > 0:
            return self.context[-1]
        return None


_context = LogContext()
if six.PY2:
    class Logger(logging.Logger):
        def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None):
            """
            A factory method which can be overridden in subclasses to create
            specialized LogRecords.
            """
            rv = LogRecord(name, level, fn, lno, msg, args, exc_info, func)
            if extra is not None:
                for key in extra:
                    if (key in ["message", "asctime"]) or (key in rv.__dict__):
                        raise KeyError("Attempt to overwrite %r in LogRecord" % key)
                    rv.__dict__[key] = extra[key]
            return rv
    _loggerClass = logging.getLoggerClass()
    logging.setLoggerClass(Logger)
else:
    _logRecordFactory = logging.getLogRecordFactory()
    logging.setLogRecordFactory(LogRecord)


def task(msg, *args, **kwargs):
    """Create a toplevel task.

    Creates a new toplevel context.
    You would use this when a new activity is started.
    A task is generally composed from smaller subtasks.

    .. code-block:: python

        from distlog import task
        with task('counting up to %d', 10, job='count up', until=10):
            for i in range(10):
                print(i)

    :param string msg: state the goal of this program
    :param list args: parameters for the goal
    :param dict kwargs: key/value context for the log messages
    :rtype: :py:class:`~distlog.Task`
    """
    return Task(uuid.uuid4(), msg, *args, **kwargs)


def to(msg, *args, **kwargs):
    """Create a subtask.

    Encapsulates a part of a larger program.
    You typically use this to delineate a program section that
    performs a specific job. Usually this means that it
    encapsulates a function.

    :todo: Create a decorator to easily encapsulate a function.

    .. code-block:: python

        from distlog import to
        val = 10

        with to('print int', arg=val):
            print(val)

    :param string msg: defines the goal of this subtask
    :param list args: parameters for the goal
    :param dict kwargs: context for log messages of this task
    :rtype: :py:class:`~distlog.Task`
    """
    _context.top.get_next_task()
    return Task(_context.top.tasks, msg, *args, **kwargs)


def import_task(_id, msg, *args, **kwargs):
    """Link task to external parent.

    Let this task be a subtask of a task in a different process.
    Allows you to see the sequence of calls and log messages over
    process boundaries.

    `_id` is obtained in the calling process through the
    :py:meth:`~distlog.Task.get_foreign_task`. How the value is transferred
    from the caller to the callee is application defined. That depends on the
    application and communication protocols.

    .. code-block:: python

        from distlog import import_task
        id = get_foreign_task_id()
        myhost = 'sample.example.com'

        with import_task(id, 'continued processing', host=myhost):
            # do something interesting

    :param string _id: task id calculated by the foreign parent task
    :param string msg: log message used with entering (and optionally
        when leaving the task
    :param list args: parameters for the log message
    :param dict kwargs: key/value pairs forming the log message context.
    :rtype: :py:class:`~distlog.Task`
    """
    return Task(id, msg, *args, **kwargs)
