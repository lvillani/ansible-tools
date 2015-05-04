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
    wrap(['ansible'], sys.argv[1:])


def ansible_local():
    # See http://stackoverflow.com/a/18255256 for the weird "inline inventory" syntax.
    wrap(['ansible-playbook', '-c', 'local', '-i', '127.0.0.1,'], sys.argv[1:])


def ansible_playbook():
    wrap(['ansible-playbook'], sys.argv[1:])


def ansible_vault():
    if len(sys.argv) < 2:
        subprocess.call(['ansible-vault', '--help'])

        return

    wrap(['ansible-vault', sys.argv[1]], sys.argv[2:])


#
# Support functions
#

def wrap(first, rest):
    if helper_reports_error():
        fatal("Cannot continue.")

    subprocess.call(first + ['--vault-password-file=%s' % VAULT_HELPER_PATH] + rest)


def helper_reports_error():
    """Ansible doesn't check the return code of the helper script we give to the
    ``--vault-password-file`` command line switch and will happily use
    whatever we print to standard output when we exit with a non-zero status
    code, including an empty string.

    This method should be called before invoking ``ansible``,
    ``ansible-playbook`` or ``ansible-vault`` to make sure that the helper
    script exits cleanly (i.e.: without errors), so that we don't do stuff
    with a bogus passphrase.

    """
    try:
        # Use check_output, this way we don't print the unlock password when
        # there are no errors.
        subprocess.check_output(VAULT_HELPER_PATH)

        return False
    except:
        return True


def fatal(*args):
    print(" ".join(args), file=sys.stderr)
    sys.exit(1)
