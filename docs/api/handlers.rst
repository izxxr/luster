.. currentmodule:: luster

.. _api-handlers:

Handlers
========

Some users might want to go beyond the boundaries and might want to handle everything by themself.
Fortunately, library provides a set of classes that provide low level control over the API.
Conventionally, we tend to call these low level classes, "Handlers"

Following are the main handlers provided by the library:

- :class:`HTTPHandler`
- :class:`WebsocketHandler`


HTTPHandler
-----------

.. autoclass:: HTTPHandler
    :members:

.. autofunction:: create_http_handler

WebsocketHandler
----------------

.. autoclass:: WebsocketHandler
    :members:
