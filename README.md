ansible-tools
=============

This is a set of wrappers around the `ansible`, `ansible-playbook` and
`ansible-vault` commands which integrate with the system keyring to retrieve
the vault password.

It should work on both Linux and OS X.


# Installation

With Homebrew:

    pip install ansible-tools

Otherwise:

    pip install --user ansible-tools

Then make sure to add the local bin directory to the `$PATH`. it is different
on each platform, please refer to `pip`'s documentation.

Otherwise, if you're feeling dirty:

    sudo pip install ansible-tools


# Usage

Go to the same directory that contains your playbooks and then run:

    avault-helper --save

You will be prompted for a vault name (which can be anything) and the unlock
password. This data is securely stored in your login keyring.

The vault name is stored in the `ansible.cfg` file, which will be created if
missing.

At this point you can use the following commands in place of Ansible's to have
the vault be automatically unlocked with each run:

* `aplay`: in place of `ansible-playbook`
* `arun`: in place of `ansible`
* `avault`: in place of `ansible-vault`
