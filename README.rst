Distlog
=======

Is a Python library and a set of applications to facilitate logging in a distributed application.

The reason to create yet another logging tool arose while developing an application based on (micro) services.
Even though each component produces a liberal amount of logging data making sense of it is challenging at times.

This is because each log file only tells part of the story.
The challenge is to find those parts of the log entries that are relevant to a particular problem request.
I tried to solve this by using correlation IDs.
These IDs are assigned when a request first enters the system and is passed on to each service that is invoked
to satisfy that request.
It sort of works but it takes a lot of time piecing all the bits together.

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
    This will make it possible to combine entries from different sources relating to the same request.

Allow multiple clients to process the log entries.
    Some will store the log entries on permanent storage (file, database).
    Others may filter the entries and display them as if tailing a logfile.

Structured
----------

Offer additional structure to the log entries.
    Normal logs are a sequential but otherwise unstructured list of hopefully significant facts.
    What I'd like to see is that the log entries tell me what is being achieved and wheter that
    succeeded or not.
    Each of these goals may itself consist of subgoals creating a tree of goals which together
    reach a conclusion.

    For many years now we modularize and structure our code, yet none of that is visible in the
    log entries that tell us how the program is progressing.
    The logs as produced by FreeRadius come to mind as an example.

The structure in the log entries should transcent process bounderies.
    When one process invokes the services of another process the structure of the log entries
    should reflect this.
    A process switch should not break the tree structure described above.

Dataset oriented
----------------

Support record logging.
    Traditionally log entries are supposed to be a single text string.
    I want to see all of Python's LogRecord fields in the log entry.
    And probably quite a few more fields as well.
    We can assume the LogRecord fields as a stable basis set of properties that are expanded by
    custom properties depending on the application and function.

Oh and the whole thing should be modular off course.
    - Structured logging
    - Multi process logging
    - Record logging

    Should be separate functional modules that can be combined to provide all of the above.

There is just one little thing: it doesn't exist. Yet.
