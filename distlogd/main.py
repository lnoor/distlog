#/usr/bin/python3

import json
import pickle
import time
import zmq
from zmq.utils.strtypes import cast_unicode

MEASURE_INTERVAL = 60
ENDPOINT= 'tcp://*:5010'

class Plugin(object):
    def match(self, data):
        raise NotImplementedError

    def handle(self, data):
        raise NotImplementedError

plugins = []
def add_plugin(plugin):
    if not isinstance(plugin, Plugin):
        raise Exception("{} is not a distlogd plugin".format(plugin.__name__))
    if plugin not in plugins:
        plugins.append(plugin)

def main():
    ctx = zmq.Context.instance()
    sock = ctx.socket(zmq.PULL)
    sock.bind(ENDPOINT)

    count = 0
    now = time.time()
    then = time.time()
    try:
        while then - now < MEASURE_INTERVAL:
            head, body = sock.recv_multipart()
            if head[2:3] == b'P':
                data = pickle.loads(body)
            else:
                data = json.loads(cast_unicode(body))

            for plugin in plugins:
                if plugin.match(data):
                    plugin.handle(data)

            count += 1
            then = time.time()

    finally:
        sock.close()
        ctx.term()

    print("{} requests took {} seconds".format(count, then - now))
    print("or {} seconds per request".format((then - now) / count))

if __name__ == '__main__':
    main()
