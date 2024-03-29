# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from luster.client import Client
    from luster.cache import Cache
    from luster.http import HTTPHandler
    from luster.websocket import WebsocketHandler
    from luster.users import User

__all__ = (
    "State",
)


class State:
    """A class that manages state of a Revolt bot.

    This class mainly serves the purpose of properly passing data
    and tracking state across different classes and specifically
    :ref:`data models <api-data-classes>`.

    You should not worry about this class when using :class:`Client`
    as it is automatically handled under the hood. However, when using
    various :ref:`handlers <api-handlers>` to interact with Revolt API,
    you might need to manually initialize models in which case you will
    need this class.

    Parameters
    ----------
    http_handler: :class:`HTTPHandler`
        The HTTP handler used for HTTP requests.
    websocket_handler: :class:`WebsocketHandler`
        The websocket handler used for websocket connections.
    cache: :class:`Cache`
        The cache handler used for caching entities.
    """
    def __init__(
        self,
        http_handler: HTTPHandler,
        websocket_handler: WebsocketHandler,
        cache: Cache,
    ) -> None:
        self.__http_handler = http_handler
        self.__websocket_handler = websocket_handler
        self.__cache = cache
        self.__client: Optional[Client] = None
        self.__user: Optional[User] = None

        http_handler.set_state(self)
        websocket_handler.set_state(self)
        cache.set_state(self)

    def set_client(self, client: Client) -> None:
        self.__client = client

    def get_client(self) -> Optional[Client]:
        return self.__client

    def remove_client(self) -> Optional[Client]:
        client = self.__client
        if client:
            self.__client = None
            return client

    @property
    def user(self) -> Optional[User]:
        return self.__user

    @user.setter
    def user(self, value: Optional[User]) -> Optional[User]:
        self.__user = value

    @property
    def http_handler(self) -> HTTPHandler:
        """The HTTP handler associated to this state.

        Returns
        -------
        :class:`HTTPHandler`
        """
        return self.__http_handler

    @property
    def websocket_handler(self) -> WebsocketHandler:
        """The websocket handler associated to this state.

        Returns
        -------
        :class:`WebsocketHandler`
        """
        return self.__websocket_handler

    @property
    def cache(self) -> Cache:
        """The cache handler associated to this state.

        Returns
        -------
        :class:`Cache`
        """
        return self.__cache
