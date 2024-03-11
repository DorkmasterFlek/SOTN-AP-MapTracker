#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Build a release and publish it to GitHub.

import sys

sys.path.append('../poptrackerlib-py/src')

from poptrackerlib.release import run_make_release

run_make_release()
