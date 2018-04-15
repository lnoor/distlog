#/usr/bin/python3
do_json = False
#do_json = True

import zmq
from zmq.utils.strtypes import cast_bytes
import json
import pickle
from random import randint

msg = {
    'foo': 'bar',
    'nest': {
        'foo': 'bar',
        'nest': {
            'list': ['item1', 'item2', 1, 2]
        },
        'rand': 0
    },
    'nest2': {
        'foo': 'bar2',
        'nest': {
            'list': [4, 5, 6, 7]
        }
    },
    'list': [
        {'aap': 'noot'},
        {'mies': 'teun'},
        {'jet': 'zus'},
        {'rand': 0}
    ]
}

endpoint = 'tcp://localhost:5010'

ctx = zmq.Context.instance()
sock = ctx.socket(zmq.PUSH)
sock.connect(endpoint)

try:
    while True:
        msg['nest']['rand'] = randint(0, 1000)
        msg['list'][3]['rand'] = randint(1000, 2000)
        if do_json:
            btopic = b'PLJ'
            sock.send_multipart([btopic, cast_bytes(json.dumps(msg))])
        else:
            btopic = b'PLP'
            sock.send_multipart([btopic, pickle.dumps(msg)])
#        print('.', end='', flush=True)
finally:
    sock.close()
    ctx.term()
