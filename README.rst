===================================================
Pent: Alternative Command Line Interface for Pipenv
===================================================


Pent is a thin wrapper around Pipenv_ that provides an alternative set of
commands for the user to work with. It does not provide any features
(everything is backed by Pipenv), but only wrap them so it fits a different
kind of brains.

.. _Pipenv: https://pipenv.org


Why?
====

Pipenv brings order to the chaotic Python project management ecosystem, which
is wonderful. With the ecosystem being so chaotic, however, everyone comes to
Pipenv with their own set of management rules, and it is impossible to satisfy
everyone. It is good to be opinionated, but we can agree to acknowledge we have
different preferences, as long as the underlying tooling stay compatible. I
want to demostrate how easy it is to put together an alternative solution.
Consider doing the same if you don’t like Pipenv’s preferences, instead of
trying to convince people to have the same preferences as you do.

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

Manage dependencies
-------------------

This part is the same as Pipenv. Call ``lock`` to resolve Pipfile’s
specifications into Pipfile.lock, ``sync`` to install dependencies from
Pipfile.lock, ``install``/``uninstall`` to add/remove packages.

Pent uses ``add`` and ``remove`` to manage package addition and removal,
inspired by Yarn. I think this naming makes more sense. They are also more
deterministic—they work exactly the same as editing Pipfile and running
``sync`` yourself.

Note that there is not ``update`` in Pent. Use ``lock`` and  ``sync`` instead.

Other commands
--------------

``run``, ``check``, ``graph``, and ``clean`` are identical to their Pipenv
counterparts (Pent simply calls them).

``shell`` works a little better than Pipenv’s because Pent detects your
currently-running shell, instead of depending on the ``SHELL`` environment
variable, and does not guess if it cannot make a decision. It also only uses
the “fancy” shell, no matter what platform you’re on, and whether you set the
environment variable ``PIPENV_SHELL_FANCY`` or not.

``where`` works as a combination of ``pipenv --where`` and ``pipenv --venv``.


Words of warning
================

As such is the nature of this project, Pent relies extremely heavily on
Pipenv’s internals, and calls a bunch of its internal functions that can break
anytime. This should be okay as long as I am actively involved in Pipenv’s
development, but I don’t make promises. Use this at your own risk, and be ready
to roll up your own sleeves. Do not expect me to fix things for you.
