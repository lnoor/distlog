#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import json
import pickle

import pytest

import distlog.logger.formatters as formatters

@pytest.fixture
def record(request):
    return logging.LogRecord('name', 20, '/here/and/nowhere/else.py',  50, 'hi there %s %d',  ('number', 1), None)

def test_returned_json_matches_record(record):
    jf = formatters.JSONFormatter()
    s = jf.format(record)
    data = json.loads(s)
    assert data['name'] == 'name'
    assert data['levelno'] == 20
    assert data['filename'] == 'else.py'
    assert data['module'] == 'else'
    assert data['lineno'] == 50
    assert data['message'] == 'hi there number 1'

def test_returned_pickle_matches_record(record):
    pf = formatters.PickleFormatter()
    s = pf.format(record)
    data = pickle.loads(s)
    assert data['name'] == 'name'
    assert data['levelno'] == 20
    assert data['filename'] == 'else.py'
    assert data['module'] == 'else'
    assert data['lineno'] == 50
    assert data['message'] == 'hi there number 1'
