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
VAULT_HELPER_PATH = os.path.join(HERE, "cli", "ansible_vault_helper.py")


def wrap(cli):
    if helper_reports_error():
        fatal("Cannot continue.")

    subprocess.call([sys.argv[1]] + ['--vault-password-file=%s' % VAULT_HELPER_PATH] + sys.argv[2:])


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
