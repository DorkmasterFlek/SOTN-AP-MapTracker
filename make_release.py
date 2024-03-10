#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Build a release and publish it to GitHub.

import argparse
import os
import sys

sys.path.append('../poptrackerlib-py/src')

from poptrackerlib.release import create_release

parser = argparse.ArgumentParser(description='Build a release and publish it to GitHub.')

parser.add_argument('--repo', default=os.getcwd(),
                    help='The directory of the repository.  If not provided, current directory is used.')

parser.add_argument('--prerelease', action='store_true', help='Mark the release as a pre-release.')

parser.add_argument('version', help='The version number of the release.')

parser.add_argument('note', nargs='+', help='The release notes.')

args = parser.parse_args()

note = '\n'.join('- ' + n for n in args.note)

try:
    create_release(args.version, note, args.prerelease, args.repo)
except ValueError as e:
    parser.error(str(e))
