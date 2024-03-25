#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Build a release and publish it to GitHub.

# Using my PopTracker Python library to make it easier.
# See: https://github.com/DorkmasterFlek/poptrackerlib-py

import sys

sys.path.append('../poptrackerlib-py/src')

from poptrackerlib.release import run_make_release

run_make_release()
