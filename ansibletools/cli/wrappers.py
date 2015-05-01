#!/usr/bin/env python2.7
#
# The MIT License (MIT)
#
# Copyright (c) 2015 Lorenzo Villani
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

"""Wrapper for both `ansible', `ansible-playbook' and `ansible-vault' which
integrates with avault-helper to fetch decryption secret from system keyring.

"""

from __future__ import print_function

import os
import os.path
import subprocess
import sys

HERE = os.path.abspath(os.path.dirname(__file__))
VAULT_HELPER_PATH = os.path.join(HERE, "helper.py")


#
# Entry points used by setup.py
#

def ansible():
    wrap('ansible')


def ansible_playbook():
    wrap('ansible-playbook')


def ansible_vault():
    if len(sys.argv) < 2:
        subprocess.call(['ansible-vault', '--help'])
        return

    if helper_reports_error():
        fatal("Cannot continue")

    subprocess.call(['ansible-vault', sys.argv[1], '--vault-password-file=%s' % VAULT_HELPER_PATH] + sys.argv[2:])


#
# Support functions
#

def wrap(cmd):
    if helper_reports_error():
        fatal("Cannot continue.")

    subprocess.call([cmd, '--vault-password-file=%s' % VAULT_HELPER_PATH] + sys.argv[1:])


def helper_reports_error():
    """Make sure we can successfully call avault-helper first since ansible-vault
    isn't smart enough to check its code and will use whatever we output as
    the encryption key, even in case of errors. We use 'check_output' so that
    we don't print the password to stdout.

    """
    try:
        subprocess.check_output(VAULT_HELPER_PATH)

        return False
    except:
        return True


def fatal(*args):
    print(" ".join(args), file=sys.stderr)
    sys.exit(1)
