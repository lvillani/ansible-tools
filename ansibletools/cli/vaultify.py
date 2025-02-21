#!/usr/bin/env python3
#
# The MIT License (MIT)
#
# Copyright (c) 2025 Lorenzo Villani
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

import os
import os.path
import shutil
import subprocess
import sys
import typing


def main():
    helper_path = vault_helper_path()
    if helper_reports_error(helper_path):
        fatal("Unable to run ansible-vault-helper. Cannot continue.")

    # ansible-vault command expects the --vault-password-file argument to be after the action
    # argument
    if os.path.basename(sys.argv[1]).startswith("ansible-vault"):
        command = (
            [sys.argv[1], sys.argv[2]]
            + [f"--vault-password-file={helper_path}"]
            + sys.argv[3:]
        )
    else:
        command = (
            [sys.argv[1]] + [f"--vault-password-file={helper_path}"] + sys.argv[2:]
        )

    sys.exit(subprocess.call(command))


def vault_helper_path() -> str:
    p = shutil.which("ansible-vault-helper")
    if not p:
        fatal(
            "Cannot find ansible-vault-helper in your $PATH or it isn't executable. Aborting"
        )

    return p


def helper_reports_error(helper_path: str) -> bool:
    """Ansible doesn't check the return code of the helper script we give to the
    ``--vault-password-file`` command line switch and will happily use whatever we print to standard
    output when we exit with a non-zero status code, including an empty string.

    This method should be called before invoking ``ansible``, ``ansible-playbook`` or
    ``ansible-vault`` to make sure that the helper script exits cleanly (i.e.: without errors), so
    that we don't do stuff with a bogus passphrase.

    """
    try:
        # Use check_output, this way we don't print the unlock password when
        # there are no errors.
        subprocess.check_output(helper_path)

        return False
    except subprocess.CalledProcessError:
        return True


def fatal(*args: str) -> typing.NoReturn:
    print(*args, file=sys.stderr)
    sys.exit(1)
