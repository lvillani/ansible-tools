# ansible-tools

[![PyPI Version](https://img.shields.io/pypi/v/ansible-tools.svg)](https://pypi.python.org/pypi/ansible-tools)
[![PyPI Downloads](https://img.shields.io/pypi/dm/ansible-tools.svg)](https://pypi.python.org/pypi/ansible-tools)
[![MIT License](https://img.shields.io/badge/license-mit-blue.svg)](https://choosealicense.com/licenses/mit/)

This is a set of wrappers around the `ansible`, `ansible-playbook` and `ansible-vault` commands
which integrate with the system keyring to retrieve the vault password.

It should work on both Linux and macOS.

# Installation

* On macOS, with Homebrew: `brew install lvillani/tap/ansible-tools`;
* With Pip: `pip install --user ansible-tools`;

It is best, however, to install `ansible-tools` in a Virtualenv, along with the version of Ansible
you are using.

# Overview

- `ansible-vault-helper`: Used by users to setup keyring integration, called by Ansible to obtain a
  Vault unlock password.
- `vaultify`: Wraps Ansible commands such as `ansible`, `ansible-playbook` and `ansible-playbook` so
  that the Vault is automatically unlocked with the password stored in the system's keyring.
- `ansible-local`: Wrapper to run Ansible locally.
- `ansible-mkpasswd`: Generates an encrypted password that can be used with the user module (see also
  [here](https://docs.ansible.com/ansible/latest/reference_appendices/faq.html#how-do-i-generate-encrypted-passwords-for-the-user-module))

# Usage

Go to the same directory that contains your playbooks and then run:

    ansible-vault-helper --update

You will be prompted for a vault name (which can be anything) and the unlock password. The former is
stored in `ansible.cfg` alongside your playbooks, the latter is securely stored in your keyring.

At this point you can run Ansible as usual but precede the command with `vaultify`. That is, to
start a playbook run:

    vaultify ansible-playbook site.yml

We also ship a tool to easily apply a playbook on the current system called `ansible-local` which is
composable with `vaultify`.

# Aliases

Here's a list of handy shell aliases to make your life easier. They were tested on fish but should
work also on Bash and Zsh:

    alias v="vault"
    alias ansible="vaultify ansible"
    alias ansible-playbook="vaultify ansible-playbook"
