.. currentmodule:: luster

.. _releases:

Releases
========

This page documents all the previous releases of the library.

v0.1.0a3 (Unreleased)
---------------------

Additions
~~~~~~~~~

- Add :meth:`Client.close_hook` hook and :attr:`Client.closed` property to allow tracking client's closures.
- Add support for proper state handling.
    - Add :class:`State` class.
    - Handlers and :class:`Client` now has a :attr:`~Client.state` attribute.

- Add support for caching.
    - Add :class:`Cache` class.
    - Add :class:`Client.cache` attribute.

- Add support for files.
    - Add :func:`HTTPHandler.upload_file` to allow uploading files.
    - Add :func:`Client.upload_file` to allow uploading files.

- Add support for various API entities

Bug Fixes & Improvements
~~~~~~~~~~~~~~~~~~~~~~~~

- Fix bug with websocket updates handling logic that caused crashes.
- :class:`WebsocketHandler` and all other classes dependent on it no longer allow multiple simultaneous websocket connections.

Documentation Changes
~~~~~~~~~~~~~~~~~~~~~

- Documentation now uses Revolt default color scheme.
- Add a :ref:`faq` section to documentation.
- Add missing documentation for :func:`create_http_handler` function.
- Add missing documentation for events and listeners.


v0.1.0a2
--------

- Add `typing_extensions>=4.2.0` to library dependencies

v0.1.0a1
--------

Initial release