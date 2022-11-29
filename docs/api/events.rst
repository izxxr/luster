.. currentmodule:: luster.events

.. _api-events:

Events
======

Luster mainly revolves around the concept of events. Events are messages received over websocket
whenever something happens such as message sent, user updated, message updated etc.

Luster provides an easy to use API in :class:`luster.Client` to efficiently listen to events and
respond to them. This page of the documentation documents the classes that are passed to
event listeners and contain information about the invoked event.

An Intro to Listeners
---------------------

First things first, let's quickly discuss what an event listener is and how we can register one.

Event listener is a simple function that is called whenever a specific event happens.

We can use the :meth:`luster.Client.listen` decorator to register an event listener. The first parameter
in this decorator is the name of event to listen to. :class:`luster.WebsocketEvent` enum provides all
the possible values for this parameter.

Example::

    @client.listen(luster.WebsocketEvent.READY)
    async def on_ready(event: luster.events.Ready):
        print(f"Bot is ready!")

Notice that the function is taking a single parameter ``event``, All listeners take this parameter.
The object passed in this parameter contains the information about the event. Depending on the event,
this parameter will take different class all inheriting a common base class, :class:`BaseEvent`.

.. note::

    For users manually using the :class:`luster.WebsocketHandler`, There is no event
    listeners API available in this class. They can override :meth:`luster.WebsocketHandler.on_websocket_event`
    hook to receive events and handle them manually.


Event Objects
-------------

Following classes are passed to event listener callback in the first parameter. These classes
are available under ``luster.events`` module.

BaseEvent
~~~~~~~~~

.. autoclass:: BaseEvent
    :members:

Authenticated
~~~~~~~~~~~~~

.. autoclass:: Authenticated
    :members:

Pong
~~~~

.. autoclass:: Pong
    :members:

Ready
~~~~~

.. autoclass:: Ready
    :members:

UserUpdate
~~~~~~~~~~

.. autoclass:: UserUpdate
    :members:

UserRelationship
~~~~~~~~~~~~~~~~

.. autoclass:: UserRelationship
    :members:

UserRelationshipUpdate
~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: UserRelationshipUpdate
    :members:

ServerCreate
~~~~~~~~~~~~

.. autoclass:: ServerCreate
    :members:

ServerUpdate
~~~~~~~~~~~~

.. autoclass:: ServerUpdate
    :members:

ServerDelete
~~~~~~~~~~~~

.. autoclass:: ServerDelete
    :members:

ChannelCreate
~~~~~~~~~~~~~

.. autoclass:: ServerCreate
    :members:

ChannelUpdate
~~~~~~~~~~~~~

.. autoclass:: ServerUpdate
    :members:

ChannelDelete
~~~~~~~~~~~~~

.. autoclass:: ServerDelete
    :members:

ChannelGroupJoin
~~~~~~~~~~~~~~~~

.. autoclass:: ChannelGroupJoin
    :members:

ChannelGroupLeave
~~~~~~~~~~~~~~~~~

.. autoclass:: ChannelGroupLeave
    :members:

GroupJoin
~~~~~~~~~

.. autoclass:: GroupJoin
    :members:

GroupLeave
~~~~~~~~~~

.. autoclass:: GroupLeave
    :members:

ServerRoleCreate
~~~~~~~~~~~~~~~~

.. autoclass:: ServerRoleCreate
    :members:

ServerRoleUpdate
~~~~~~~~~~~~~~~~

.. autoclass:: ServerRoleUpdate
    :members:

ServerRoleDelete
~~~~~~~~~~~~~~~~

.. autoclass:: ServerRoleDelete
    :members:

RoleCreate
~~~~~~~~~~

.. autoclass:: RoleCreate
    :members:

RoleUpdate
~~~~~~~~~~

.. autoclass:: RoleUpdate
    :members:

RoleDelete
~~~~~~~~~~

.. autoclass:: RoleDelete
    :members:
