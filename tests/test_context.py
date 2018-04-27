#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import six
import pytest

if __name__ == '__main__':
    import sys
    sys.path.append('..')
import distlog.logger.context as context

def test_globals():
    if six.PY3:
        assert logging.getLogRecordFactory() == context.LogRecord
    assert type(logging.root) == context.RootLogger
    assert logging._loggerClass == context.Logger
    assert type(context._context) == context.LogContext

def test_context():
    class obj:
        parent = None
    x = obj()
    y = obj()
    z = obj()

    assert len(context._context.context) == 0
    context._context.push(x)
    context._context.push(y)
    context._context.push(z)

    assert len(context._context.context) == 3
    assert id(context._context.context[0]) == id(x)
    assert id(context._context.context[1]) == id(y)
    assert id(context._context.context[2]) == id(z)
    assert id(context._context.top) == id(z)

    assert id(context._context.pop()) == id(z)
    assert len(context._context.context) == 2
    assert id(context._context.pop()) == id(y)
    assert len(context._context.context) == 1
    assert id(context._context.pop()) == id(x)
    assert len(context._context.context) == 0

def test_logrecord():
    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger()
    log.handlers = [] # make sure only our handler gets installed
    log.propagate = False
    assert type(log) == context.RootLogger
    rec = []
    class vang(logging.Handler):
        def emit(self, record):
            #print("EMITTING")
            assert type(record) == context.LogRecord
            rec.append(record)
    v = vang(logging.DEBUG)
    log.addHandler(v)

    tsk = context.Task('a', 'msg %d', 4, aap='noot', mies='teun')
    assert tsk.parent == None
    assert tsk.msg == 'msg %d'
    assert 'aap' in tsk.data
    assert tsk.data['aap'] == 'noot'
    assert tsk.counter == 0

    context._context.push(tsk)
    assert len(rec) == 0
    log.debug('lala %s',  'dada')
    assert len(rec) == 1
    assert type(rec[0]) == context.LogRecord
    assert hasattr(rec[0], 'context')
    assert 'aap' in rec[0].context
    assert rec[0].context['aap'] == 'noot'

def test_task():
    tsk = context.Task('b', 'msg %d', 6,  wim='jet', zus='gijs')
    assert tsk.parent is None
    assert 'does' not in tsk.data
    tsk.bind(does='schapen')
    assert 'does' in tsk.data
    assert tsk.data['does'] == 'schapen'
    assert tsk.smsg is tsk.msg
    tsk.success('%s: %s', 'zeg', 'joepie')
    assert tsk.smsg == '%s: %s'
    assert tsk.sargs[0] == 'zeg'
    assert tsk.sargs[1] == 'joepie'

def test_contextmanager():
    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger()
    log.handlers = [] # make sure only our handler gets installed
    log.propagate = False
    assert type(log) == context.RootLogger
    rec = []
    class vang(logging.Handler):
        def emit(self, record):
            #print("EMITTING")
            rec.append(record)
    v = vang(logging.DEBUG)
    log.addHandler(v)

    tsk = context.Task('c', 'msg %d', 8, sample='good')
    assert len(rec) == 0
    with pytest.raises(ValueError):
        with tsk:
            #pass
            raise ValueError('bok')
    assert len(rec) == 2
    for r in rec:
        assert type(r) == context.LogRecord
        assert hasattr(r, 'context')
        assert 'sample' in r.context
        assert r.context['sample'] == 'good'

if __name__ == '__main__':
    test_globals()
    test_context()
    test_logrecord()
    test_task()
    test_contextmanager()
