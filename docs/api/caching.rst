.. currentmodule:: luster

.. _api-caching:

Caching
=======

When it comes to maintaining a bot with a lot of traffic, You need to maintain a cache in order
to prevent excessive API calls that may lead to ratelimits. Luster makes this process incredibly
simple. 

The library not only automatically maintains a cache for you but also allows you to
write custom cache handlers to implement caching using some service such as Redis.

Cache
-----

.. autoclass:: Cache
    :members:

.. _api-caching-custom-handler:

Custom Cache Handler
--------------------

You can subclass :class:`Cache` and override certain methods to implement custom caching. Here
is an example of implementing custom caching for users using a simple dictionary::

    class MyCache(luster.Cache):
        def __init__(self) -> None:
            self._users = {}

        def add_user(self, user):
            self._users[user.id] = user

        def get_user(self, user_id):
            return self._users.get(user_id)

        def remove_user(self, user_id):
            return self._users.pop(user_id, None)

        def users(self):
            return list(self._users.values())

Now that we have implemented custom caching for users, we can pass our ``MyCache`` class to
:class:`Client`::

    client = luster.Client(token="...", cache_cls=MyCache)
    # client.cache is now MyCache
