.. currentmodule:: luster

.. _installation:

Installation
============

This library is hosted on `PyPi <https://pypi.org/project/luster>`_ and can be installed using
Python's traditional package manager `pip`::

    $ pip install luster


.. _installation-dependencies:

Dependencies
------------

This library only requires `aiohttp <https://docs.aiohttp.org>`_ as it's core dependency. `pip`
should handle the required dependencies for you automatically.

There are some optional dependencies that this library uses for various purposes mostly including
performance optimizations. These dependencies are not required for functioning of the library but
can be used for optimizing the performance of library.

Following are the optional dependencies for performance optimizations:

- `msgpack <https://pypi.org/project/msgpack>`_ — Faster websocket packets parsing.
- `ujson <https://pypi.org/project/ujson>`_ — Faster JSON parsing.
- `aiohttp[speed] <https://docs.aiohttp.org/en/stable/#installing-speedups-altogether>`_ — aiohttp speed-ups.

All these optional dependencies can be installed easily by providing the ``speed`` scope in the
pip command above::

    $ pip install luster[speed]
