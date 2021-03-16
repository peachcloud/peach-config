"""
this file is the main entrypoint to all the peach-config CLI subcommands
"""
import sys
import argparse

from peach_config.generate_manifest import generate_manifest
from peach_config.setup_peach import init_setup_parser, setup_peach
from peach_config.update import init_update_parser, update


def peach_config():

    # create parser
    parser = argparse.ArgumentParser(prog='peach-config')
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    # create parsers for subcommands
    setup_parser = subparsers.add_parser('setup', help="idempotent setup of PeachCloud")
    init_setup_parser(setup_parser)
    subparsers.add_parser('manifest', help='prints manifest of peach configurations')
    update_parser = subparsers.add_parser('update', help='updates all PeachCloud microservices')
    init_update_parser(update_parser)

    # parse arguments
    args = parser.parse_args()

    # switch based on subcommand
    if args.subcommand == 'setup':
        setup_peach(parser)
    elif args.subcommand == 'manifest':
        generate_manifest()
    elif args.subcommand == 'update':
        update(parser)


if __name__ == '__main__':
    sys.exit(peach_config())