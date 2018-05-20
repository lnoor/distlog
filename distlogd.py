#/usr/bin/python3

import argparse
import distlogd

config = None

def main():
    handle_arguments()
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
    distlogd.plugins.load_config(args.configfile)


if __name__ == '__main__':
    exit(main())
