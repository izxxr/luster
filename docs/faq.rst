.. currentmodule:: luster

.. _faq:

Frequently Asked Questions
==========================

These are frequently asked questions regarding this library.

General
-------

How can I perform extra clean up on Client closure?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:class:`Client` provides a :meth:`close_hook` that is called whenever the client
is completely closed. You can override this method to implement custom clean up
such as closing database connections etc.

Example::

    class Client(luster.Client):
        async def close_hook(self):
            # Perform clean up here
            ...

Caching
-------

Is caching HTTP fetched entities a good idea?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The simple answer is **No.**

Cache is meant for entities whose state is tracked by the websocket events. This means
that if an entity such as a user is cached, changes in that entity are properly
tracked over websocket and if for example, user changes their status on Revolt, their
user object will also be updated accordingly.

The problem with caching entites fetched over HTTP is that they are not tracked by
websocket and are "stale". You may fetch a user that you do not share a server with
and cache it but you will not receive the updates for that user so it will remain
stale regardless of changes happening in that user.

The ``add_*`` methods on :class:`Cache` mainly are exposed to allow custom implementation
of cache handlers and should not be called directly by users.

How can I set a limit on number of entities cached?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can subclass :class:`Cache` to implement custom limits and pass the cache handler
to your :class:`Client` or :class:`State`. For more information, see the :ref:`api-caching-custom-handler`
section in the documentation.


Events and Listeners
--------------------

Can I create custom events?
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Creating custom events is discouraged** as it can cause conflicts with the library events and
can lead to surprising results.

Nevertheless in order to create custom events, you can subclass :class:`BaseEvent` and override
the :meth:`~events.BaseEvent.get_event_name` method to return your custom event name::

    class MyEvent(luster.events.BaseEvent):
        def get_event_name(self) -> str:
            return "my_event"

Then you can register listeners for your event and call :meth:`Client.call_listeners` somewhere
to dispatch your event::

    @client.listen("my_event")
    async def handle_my_event(event: MyEvent):
        ...

    # Somewhere else...
    client.call_listeners(MyEvent())

You can propagate your event's data to listeners by setting attributes on :class:`BaseEvent`.

Handlers
--------

How can I handle websocket events manually?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can subclass :class:`WebsocketHandler` and implement the :meth:`on_websocket_event` hook
and handle events manually::

    class WebsocketHandler(luster.WebsocketHandler):
        async def on_websocket_event(self, event: types.EventTypeRecv, data: Any) -> None:
            # Event handling goes here.
            ...


.. tip::

    You can pass the custom subclass of :class:`WebsocketHandler` in a :class:`Client` by
    passing the ``websocket_handler_cls`` parameter.

Data Models
-----------

How can I initialize a data model manually?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In order to manually initialize a data model, you need a :class:`State` to propagate
important data to the relevant data model.

For example, initializing a :class:`User` manually::

    async with luster.create_http_handler(token="...") as http:
        state = State(
            http_handler=http,
            websocket_handler=luster.WebsocketHandler(http),
            cache=luster.Cache(),
        )
        data = await http.fetch_user("USER_ID")

        # Pass data and state in User
        user = User(data, state)
        print(f"Fetched user object for {user.username} (user.id)")


Can I set custom attributes on data models?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The simple answer is **No.**

For performance purposes, All data models have defined a ``__slots__`` attribute which
disallows setting custom attributes. So, it is not possible to set custom attributes.
