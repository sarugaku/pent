===================================================
Pent: Alternative Command Line Interface for Pipenv
===================================================


Pent is a thin wrapper around Pipenv_ that provides an alternative set or
commands for the user to work with it. It does not provide any features
(everything is backed by Pipenv), but only wrap them so it fits a different
kind of brains.

.. _Pipenv: https://pipenv.org


Why?
====

Pipenv brings order to the chaotic Python project management ecosystem, which
is wonderful. With the ecosystem being so chaotic, however, everyone comes to
Pipenv with their own set of management rules, and it is impossible to satisfy
everyone. It is good to be opinionated, but we can agree to acknowledge we have
different preferences, as long as the underlying tooling stay compatible. These
are my preferences.

As an official PyPA project, Pipenv also is required to be more conservative
when it comes to tradeoffs. It still uses virtualenv (as of May 2018), a proven
inferior tool to the new built-in venv, because it needs to support Python 2
projects, and lacks resources to support both virtualenv and venv. Pent gives
me an oppertunity to move faster and experiement new things without needing to
convince people. I can also deal with less consequence if I make any wrong
decisions.


How do I use this thing?
========================

Let’s walk through a project’s lifetime to illustrate how Pent’s workflow looks
like.

New project
-----------

Unlike Pipenv, Pent *does not* create a Pipfile automatically when you start a
new project. You need to call ``new`` explicitly. The ``new`` command will
always create a Pipfile in the current working directory, if it does not exist.

Environment creation
--------------------

Once you have a Pipfile (either from ``new`` or when you clone a repository
from somewhere), you need a virtual environment. This is done with ``init``.
This command however *requires* you to pass the Python interpreter (or at least
the version of it) you want to use. It does not guess.

Pent also tries to use the built-in venv to create the environment if possible.

Install dependencies
--------------------

This part is the same as Pipenv. Call ``sync`` to install dependencies from a
Pipfile, ``install``/``uninstall`` to add/remove packages.

Pent adds two aliases, ``add`` and ``remove``, because I think the naming makes
more sense. They work exactly the same as ``install`` and ``uninstall``.

Note that ``install`` without arguments does not work in Pent. Use ``sync``
instead.

Other commands
--------------

``lock``, ``run``, ``check``, ``graph``, and ``clean`` are identical to their
Pipenv counterparts (Pent simply calls them).

``shell`` works a little better than Pipenv’s because Pent try to detect your
current shell instead of depending on the ``SHELL`` variable, and does not
guess if it cannot make a decision.

``where`` works as a combination of ``pipenv --where`` and ``pipenv --venv``.

Removed commands
----------------

``update`` is removed. You can achieve the same effect by first running
``lock`` to update dependency versions in Pipfile.lock, and ``sync`` to apply
the new versions.


Words of warning
================

As such is the nature of this project, Pent relies extremely heavily on
Pipenv’s internals, and calls a bunch of its internal functions that can break
anytime. This should be okay as long as I am actively involved in Pipenv’s
development, but I don’t make promises. Use this at your own risk, and be ready
to roll up your own sleeves. Do not expect me to fix things for you.
