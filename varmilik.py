#!/usr/bin/env python3
"""varmilik
Watch currencies for my asset

Usage:
  varmilik run [-f <file_path>]
  varmilik watch [-f <file_path>] -t SECONDS [-s|-m|-h|-d]

Options:
  -f, --file <file_path>   the data file for your asset [default: data.json].
  -t, --time SECONDS       cool-down period.
  -s, --second             cool-down period time unit [default: True]
  -m, --minute             cool-down period time unit.
  -h, --hour               cool-down period time unit.
  -d, --day                cool-down period time unit.
"""
import os
import time
from docopt import docopt
from asset_manager import AssetManager


class Arguments:
    TIME = {
        'day': 24 * 60 * 60,
        'hour': 60 * 60,
        'minute': 60,
        'second': 1
    }

    def __init__(self, args):
        self.args = args
        self.watch = args['watch']
        self.run = args['run']

        if args['--time']:
            self.time = int(args['--time'])
        self.file = args['--file'] if args['--file'] else 'data.json'
        t = [self.TIME[k.replace("--", '')] for k in ['--day', '--minute', '--hour', '--second'] if args[k]]
        self.cooldown_time = t[0] if len(t) == 1 else self.TIME['second']
    
    def __repr__(self):
        return self.args.__str__()


def navigate(args):
    if args.watch:
        while 1:
            try:
                os.system('clear')
                AssetManager(args).run()
                print(time.asctime(time.localtime(time.time())))
                time.sleep(args.time * args.cooldown_time)
            except Exception:
                continue
    elif args.run:
        AssetManager(args).run()


if __name__ == '__main__':
    arguments = docopt(__doc__)
    navigate(Arguments(arguments))
