.. currentmodule:: luster.types

.. _api-types:

API Types
=========

When it comes to working with low level API, dealing with raw JSON payloads and handling API
payloads manually can be an overwhelming task.

To ease you in this case, Library provides easy to use type defintions for Revolt API that only
allow you to properly typehint your application but also get cutting edge autocompletion in
your code editor.

Enumerations
------------

This section documents various enumerations from the Revolt API. All these are type aliases of
:class:`typing.Literal`.

.. data:: EventTypeSend

    The types of websocket events that are sent by the client.

.. data:: EventTypeRecv

    The types of websocket events that are received by the client.

.. data:: EventType

    The types of websocket events. This is equivalent to :class:`typing.Union`
    of :data:`EventTypeSend` and :data:`EventTypeRecv`.

.. data:: ErrorId

    The error labels often sent in :class:`ErrorEvent` websocket event.

.. data:: WebsocketVersion

    The versions for Revolt websocket protocol.

.. data:: WebsocketFormat

    The formats used for packets transport in Revolt websocket protocol.

.. data:: FileType

    The types of file.

.. data:: PresenceType

    The presence states of a user.

.. data:: RelationshipStatus

    The status of a relationship.


API Models
----------

This section documents type definitions for various API models. All these type definitions
are subclasses of :class:`typing.TypedDict`.

NodeInfo
~~~~~~~~

.. autoclass:: NodeInfo()
    :members:

NodeInfoFeatures
~~~~~~~~~~~~~~~~

.. autoclass:: NodeInfoFeatures()
    :members:

NodeInfoCaptchaFeature
~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: NodeInfoCaptchaFeature()
    :members:

NodeInfoAutumnFeature
~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: NodeInfoAutumnFeature()
    :members:

NodeInfoJanuaryFeature
~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: NodeInfoJanuaryFeature()
    :members:

NodeInfoVosoFeature
~~~~~~~~~~~~~~~~~~~

.. autoclass:: NodeInfoVosoFeature()
    :members:

User
~~~~

.. autoclass:: User()
    :members:

UserStatus
~~~~~~~~~~

.. autoclass:: UserStatus()
    :members:

UserProfile
~~~~~~~~~~~

.. autoclass:: UserProfile()
    :members:


PartialUserBot
~~~~~~~~~~~~~~

.. autoclass:: PartialUserBot()
    :members:


Relationship
~~~~~~~~~~~~

.. autoclass:: Relationship()
    :members:


HTTP Routes
-----------

This section documents type definitions for various HTTP routes. All these type definitions
are subclasses of :class:`typing.TypedDict`.

QueryNodeResponse
~~~~~~~~~~~~~~~~~

.. autoclass:: QueryNodeResponse()
    :members:


Websocket Events
----------------

This section documents type definitions for various websocket events. All these type definitions
are subclasses of :class:`typing.TypedDict`.

AuthenticateEvent
~~~~~~~~~~~~~~~~~

.. autoclass:: AuthenticateEvent()
    :members:

PingEvent
~~~~~~~~~

.. autoclass:: PingEvent()
    :members:


BeginTypingEvent
~~~~~~~~~~~~~~~~

.. autoclass:: AuthenticateEvent()
    :members:

EndTypingEvent
~~~~~~~~~~~~~~

.. autoclass:: EndTypingEvent()
    :members:

ErrorEvent
~~~~~~~~~~

.. autoclass:: ErrorEvent()
    :members:

AuthenticatedEvent
~~~~~~~~~~~~~~~~~~

.. autoclass:: AuthenticatedEvent()
    :members:

PongEvent
~~~~~~~~~

.. autoclass:: PongEvent()
    :members:

BulkEvent
~~~~~~~~~

.. autoclass:: BulkEvent()
    :members:
