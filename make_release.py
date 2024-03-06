#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Build a release and publish it to GitHub.

import argparse
import hashlib
import json
import re
import subprocess

from git import Repo
from github import Github

parser = argparse.ArgumentParser(description='Build a release and publish it to GitHub.')

parser.add_argument('--prerelease', action='store_true', help='Mark the release as a pre-release.')

parser.add_argument('version', help='The version number of the release.')

parser.add_argument('note', nargs='+', help='The release notes.')

args = parser.parse_args()

if not re.match(r'^\d+(\.\d+)+$', args.version):
    raise ValueError('Invalid version number.')

REPO_NAME = 'SOTN-AP-MapTracker'
OUTPUT_FILE = REPO_NAME + '.zip'

repo = Repo()

# Make ZIP file.
with open(OUTPUT_FILE, 'wb') as f:
    path = [
        'LICENSE',
        'README.md',
        'manifest.json',
        'images',
        'items',
        'layouts',
        'locations',
        'maps',
        'scripts',
    ]
    repo.archive(f, 'main', format='zip', path=path)

# Get SHA256 hash of ZIP file.
with open(OUTPUT_FILE, 'rb') as f:
    sha256 = hashlib.file_digest(f, 'sha256').hexdigest()

# Read current versions and create new entry from release notes.
with open('versions.json') as f:
    versions = json.load(f)

new_version = {
    'package_version': args.version,
    'download_url': '',  # Placeholder for field order.
    'sha256': sha256,
    'changelog': args.note
}

# Publish a new release to GitHub using OAuth token from command line.
# Use notes as bullet points in the release body.
tag = title = 'v' + args.version
body = '\n'.join('- ' + n for n in args.note)
process = subprocess.run(['gh', 'auth', 'token'], capture_output=True, text=True, check=True)
token = process.stdout.strip()

g = Github(token)
remote_repo = g.get_user().get_repo(REPO_NAME)
binsha = repo.commit('main').binsha
release = remote_repo.create_git_tag_and_release(tag, tag, title, body, binsha.hex(), 'commit',
                                                 prerelease=args.prerelease)
attachment = release.upload_asset(OUTPUT_FILE, label=OUTPUT_FILE)
new_version['download_url'] = attachment.browser_download_url

# Add download URL to new versions entry at the front and commit it to the repository.
versions['versions'].insert(0, new_version)
with open('versions.json', 'w') as f:
    json.dump(versions, f, indent=4)

repo.index.add(['versions.json'])
repo.index.commit(f'{tag} release')
repo.remotes.origin.push()