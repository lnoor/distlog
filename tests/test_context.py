#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

if __name__ == '__main__':
    import sys
    sys.path.append('..')
import distlog.logger.context as context

def test_globals():
    assert logging.getLogRecordFactory() == context.LogRecord
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

rec = None
def test_logrecord():
    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger(__name__)
    class vang(logging.Handler):
        def emit(self, record):
            global rec
            rec = record
    v = vang(logging.DEBUG)
    logging.lastResort = v
    log.addHandler(v)

    tsk = context.Task('a', 'msg %d', 4, aap='noot', mies='teun')
    assert tsk.parent == None
    assert tsk.msg == 'msg %d'
    assert 'aap' in tsk.data
    assert tsk.data['aap'] == 'noot'
    assert tsk.counter == 0

    context._context.push(tsk)
    log.debug('lala %s',  'dada')
    assert hasattr(rec, 'context')
    assert 'aap' in rec.context
    assert rec.context['aap'] == 'noot'

def test_task():
    tsk = context.Task('b', 'msg %d', 6,  wim='jet', zus='gijs')
    assert tsk.parent is None
    assert 'does' not in tsk.data
    tsk.bind(does='schapen')
    assert 'does' in tsk.data
    assert tsk.data['does'] == 'schapen'
    assert tsk.smsg is None
    tsk.success('%s: %s', 'zeg', 'joepie')
    assert tsk.smsg == '%s: %s'
    assert tsk.sargs[0] == 'zeg'
    assert tsk.sargs[1] == 'joepie'

def test_contextmanager():
    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger(__name__)
    class vang(logging.Handler):
        def emit(self, record):
            global rec
            rec = record
    v = vang(logging.DEBUG)
    logging.lastResort = v
    log.addHandler(v)

    tsk = context.Task('c', 'msg %d', 8)
    with tsk:
        raise ValueError('bok')

if __name__ == '__main__':
    test_globals()
    test_context()
    test_logrecord()
    test_task()
    test_contextmanager()
