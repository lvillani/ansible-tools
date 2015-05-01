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

"""
ansible-vault password helper.
"""

from __future__ import print_function

import ConfigParser
import argparse
import getpass
import os
import os.path
import sys

import keyring


CFG_OPTION = "name"
CFG_SECTION = "vault"
KEYRING_SERVICE = "ansible-vault"


def main():
    args = parse_args()

    if args.save:
        save()
        return

    secret_name, err = get_secret_name()
    if err:
        fatal(err)

    secret, err = get_secret(secret_name)
    if err:
        fatal(err)

    print(secret)


def parse_args():
    args = argparse.ArgumentParser()
    args.add_argument("-s", "--save", action="store_true", help="Prompts for a password and stores it in the keyring")

    return args.parse_args()


def save():
    secret_name, err = get_secret_name()
    if err:
        name = raw_input("Vault name: ")
    else:
        name = secret_name

    print('WARNING: Changing password for %s' % name)
    password = getpass.getpass("Password: ")
    set_secret(name, password)


def set_secret(name, secret):
    """Stores a secret into the keyring, creating or updating the relevant stanza
    in `ansible.cfg' in the process.

    """
    c = load_ansible_cfg()

    if not c.has_section("vault"):
        c.add_section("vault")

    c.set(CFG_SECTION, CFG_OPTION, name)

    with open(get_ansible_cfg_path(), "w") as fp:
        c.write(fp)

    keyring.set_password(KEYRING_SERVICE, name, secret)


def load_ansible_cfg():
    """Returns a ConfigParser instance with the contents of ansible.cfg. If the
    file does not exist, it returns an empty ConfigParser object instead.

    """
    c = ConfigParser.ConfigParser()

    if is_ansible_cfg_there():
        c.read(get_ansible_cfg_path())

    return c


def is_ansible_cfg_there():
    return os.path.isfile(get_ansible_cfg_path())


def get_ansible_cfg_path():
    return os.path.join(os.getcwd(), "ansible.cfg")


def get_secret_name():
    """Gets the secret name from local ansible.cfg file.

    Returns a tuple (secret_name, error_string) with `secret_name' being the
    empty string in case of errors, in which case `error_string' is set to a
    human-readable, non-localized, error message.

    """
    if not is_ansible_cfg_there():
        return ("", "Unable to find ansible.cfg in the current directory.")

    c = load_ansible_cfg()

    if not c.has_section(CFG_SECTION):
        return ("", "Unable to find 'vault' section within ansible.cfg")

    if not c.has_option(CFG_SECTION, CFG_OPTION):
        return ("", "Unable to find option '%s' in section '%s' within ansible.cfg" % (CFG_OPTION, CFG_SECTION))

    return (c.get(CFG_SECTION, CFG_OPTION), "")


def fatal(*args):
    print(" ".join(args), file=sys.stderr)
    sys.exit(1)


def get_secret(name):
    """Obtains secret from the keyring."""
    p = keyring.get_password(KEYRING_SERVICE, name)

    if not p:
        howto = "Call %s --set to save a password inside the keyring." % name

        return ("", "Unable to find a password with name %s.\n\n%s" % (name, howto))

    return (p, "")


if __name__ == "__main__":
    main()
