ansible-tools
=============

![PyPI](https://img.shields.io/pypi/dm/ansible-tools.svg)
![MIT License](https://img.shields.io/badge/license-mit-blue.svg)

This is a set of wrappers around the `ansible`, `ansible-playbook` and
`ansible-vault` commands which integrate with the system keyring to retrieve
the vault password.

It should work on both Linux and OS X.


# Installation

If you are on OS X and have Homebrew's Python:

    pip install ansible-tools

Otherwise:

    pip install --user ansible-tools

Then make sure to add the local pip's `bin` directory to the `$PATH`. Since it
is different on each platform, please refer to its documentation.

Otherwise, if you're feeling a badass and want to `sudo` your way out, then
run:

    sudo pip install ansible-tools


# Usage

Go to the same directory that contains your playbooks and then run:

    avault-helper --save

You will be prompted for a vault name (which can be anything) and the unlock
password. The former is stored in `ansible.cfg` alongside your playbooks, the
latter is securely stored in your keyring.

At this point you can use the following commands in place of Ansible's to have
the vault be automatically unlocked with each run:

* `alocal`: in place of `ansible-playbook -c local`;
* `aplay`: in place of `ansible-playbook`;
* `arun`: in place of `ansible`;
* `avault`: in place of `ansible-vault`;
