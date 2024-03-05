#!/bin/bash

git archive -o SOTN-AP-MapTracker.zip main README.md LICENSE *.json images items layouts locations maps scripts
sha256sum SOTN-AP-MapTracker.zip
