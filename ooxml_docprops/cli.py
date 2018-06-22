"""Simple command-line interface for easy testing.
"""

from ooxml_docprops import read_properties
from ooxml_docprops import update_properties
import argparse
import config
import json


def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('document', help='Office Document to be updated')
    parser.add_argument('-d', '--debug',
                        help='Show debug output',
                        action='store_true')
    return parser


def update_props():
    parser = create_arg_parser()
    parser.add_argument('metadata_file', help='JSON file containing metadata')
    args = parser.parse_args()

    config.DEBUG = args.debug
    if config.DEBUG:
        print("Updating '{}' with metadata from '{}'...".format(
            args.document, args.metadata_file))

    metadata = json.load(open(args.metadata_file))
    update_properties(args.document, metadata)


def read_props():
    parser = create_arg_parser()
    args = parser.parse_args()

    config.DEBUG = args.debug
    if config.DEBUG:
        print("Reading properties from '{}'...".format(args.document))

    for key, value in read_properties(args.document):
        print("{} = {}".format(key, value))
