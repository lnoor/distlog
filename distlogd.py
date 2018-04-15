#/usr/bin/python3

import importlib
import sys
import argparse
import yaml
import distlogd

config = None

def main():
    handle_arguments()
    load_plugins()
    return distlogd.main()


def handle_arguments():
    global config
    parser = argparse.ArgumentParser(description='Receive and process distlog messages.')
    parser.add_argument(
        '-c',
        dest='configfile',
        default='./distlogd.yml',
        type=argparse.FileType('r'),
        help='distlogd configuration file, default: ./distlogd.yml'
    )
    args = parser.parse_args()
    config = yaml.load(args.configfile)

def load_plugins():
    for path in config['locations']:
        sys.path.append(path)
    for plugin in config['plugins']:
        name = plugin['package']
        try:
            module = importlib.import_module(name)
            distlogd.add_plugin(module.initialize(plugin['options']))
        except Exception as e:
            print(e)

if __name__ == '__main__':
    exit(main())
