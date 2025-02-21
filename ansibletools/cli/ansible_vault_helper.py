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

import argparse
import configparser
import getpass
import inspect
import os
import os.path
import sys
import typing

import keyring


CFG_OPTION = "name"
CFG_SECTION = "vault"
KEYRING_SERVICE = "ansible-vault"


def main():
    args = parse_args()

    if args.update:
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
    args.add_argument(
        "-u",
        "--update",
        action="store_true",
        help="Stores/Updates a vault unlock password in the keyring, saving the association in ansible.cfg",
    )

    return args.parse_args()


def save():
    secret_name, err = get_secret_name()
    if err:
        name = input("Vault name: ")
        if not name:
            fatal("Vault name cannot be empty.")
    else:
        print(f"WARNING: Changing password for '{secret_name}'")
        name = secret_name

    password = getpass.getpass("Password: ")
    if not password:
        print("WARNING: Empty password, not updating keyring entry.")
        return

    set_secret(name, password)


def set_secret(name, secret):
    """Stores a secret into the keyring, creating or updating the relevant stanza
    in `ansible.cfg' in the process.

    """
    c = load_ansible_cfg()

    if not c.has_section("vault"):
        c.add_section("vault")

    existing_name = c.get(CFG_SECTION, CFG_OPTION, fallback="")
    if existing_name != name:
        c.set(CFG_SECTION, CFG_OPTION, name)
        with open(get_ansible_cfg_path(), "w") as fp:
            c.write(fp)

    keyring.set_password(KEYRING_SERVICE, name, secret)


def load_ansible_cfg():
    """Returns a ConfigParser instance with the contents of ansible.cfg. If the
    file does not exist, it returns an empty ConfigParser object instead.

    """
    c = configparser.ConfigParser()

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
        return (
            "",
            f"Unable to find option '{CFG_OPTION}' in section '{CFG_SECTION}' within ansible.cfg",
        )

    name = c.get(CFG_SECTION, CFG_OPTION)
    if not name:
        return ("", "Vault name cannot be empty.")

    return (name, "")


def fatal(*args: str) -> typing.NoReturn:
    print(*args, file=sys.stderr)
    sys.exit(1)


def get_secret(name) -> typing.Tuple[str, typing.Optional[str]]:
    """Obtains secret from the keyring."""
    p = keyring.get_password(KEYRING_SERVICE, name)

    if not p:
        return (
            "",
            inspect.cleandoc(
                f"""
                Unable to obtain password for vault "{name}" from the keyring.

                Call "ansible-vault-helper --update" to add or update the vault's password
                to the keyring.
                """
            )
            + "\n",
        )

    return (p, None)


if __name__ == "__main__":
    main()
