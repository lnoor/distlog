import logging
import sys
import importlib
import yaml

log = logging.getLogger(__name__)

_locations = []
_plugins = []

class Plugin(object):
    def match(self, data):
        raise NotImplementedError

    def handle(self, data):
        raise NotImplementedError

def add_location(location):
    global _locations
    if type(location) == list:
        _locations += location
    else:
        _locations.append(location)

def add_plugin(plugin):
    if not isinstance(plugin, Plugin):
        raise Exception("{} is not a distlogd plugin".format(plugin.__name__))
    if plugin not in _plugins:
        _plugins.append(plugin)

def load_plugins(plugins):
    for path in _locations:
        sys.path.append(path)
    for plugin in plugins:
        name = plugin['package']
        try:
            module = importlib.import_module(name)
            add_plugin(module.initialize(plugin['options']))
        except:
            log.exception('failed to load plugin "{}"'.format(name))
            raise

def load_config(filename):
    config = yaml.load(filename)
    add_location(config['locations'])
    load_plugins(config['plugins'])

def handle(data):
    for plugin in _plugins:
        if plugin.match(data):
            plugin.handle(data)
