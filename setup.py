from __future__ import absolute_import, division, print_function, unicode_literals

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="ansible-tools",
    version="0.1.2",
    description="Keyring integration and local execution wrappers for Ansible",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lvillani/ansible-tools",
    author="Lorenzo Villani",
    author_email="lorenzo@villani.me",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: System :: Systems Administration",
    ],
    keywords="ansible local keyring tools wrapper",
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    install_requires=["keyring", "passlib", "six"],
    entry_points={
        "console_scripts": [
            "ansible-local=ansibletools.cli.ansible_local:main",
            "ansible-mkpasswd=ansibletools.cli.ansible_mkpasswd:main",
            "ansible-vault-helper=ansibletools.cli.ansible_vault_helper:main",
            "vaultify=ansibletools.cli.vaultify:main",
        ]
    },
)
