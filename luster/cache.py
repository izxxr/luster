# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Optional
from luster.internal.mixins import StateManagementMixin

if TYPE_CHECKING:
    from luster.users import User
    from luster.server import Server
    from luster.channels import ChannelT


class Cache(StateManagementMixin):
    """A class that handles caching of various entities from Revolt API.

    This acts as  a base class for custom cache handlers. You may inherit
    this class to implement custom caching using a separate service
    such as Redis.

    The possible ways of accessing the instance of this object is:

    - :attr:`State.cache`
    - :attr:`Client.cache`
    """

    def __init__(self) -> None:
        self.clear()

    def clear(self) -> None:
        self.__users: Dict[str, User] = {}
        self.__servers: Dict[str, Server] = {}
        self.__channels: Dict[str, ChannelT] = {}

    def users(self) -> List[User]:
        """The users that are currently cached.

        Returns
        -------
        List[:class:`User`]
        """
        return list(self.__users.values())

    def add_user(self, user: User) -> None:
        """Adds a new user to the cache.

        If a similar user already exists, It will be overwritten.

        Parameters
        ----------
        user: :class:`User`
            The user to add.
        """
        self.__users[user.id] = user

    def get_user(self, user_id: str) -> Optional[User]:
        """Gets a user from the cache.

        Parameters
        ----------
        user_id: :class:`str`
            The ID of user to get.

        Returns
        -------
        Optional[:class:`User`]
            The requested user; if exists. Otherwise ``None``.
        """
        return self.__users.get(user_id)

    def remove_user(self, user_id: str) -> Optional[User]:
        """Removes a user from the cache.

        Parameters
        ----------
        user_id: :class:`str`
            The ID of user to remove.

        Returns
        -------
        Optional[:class:`User`]
            The remoevd user; if exists. Otherwise ``None``.
        """
        return self.__users.pop(user_id, None)

    def servers(self) -> List[Server]:
        """The servers that are currently cached.

        Returns
        -------
        List[:class:`Server`]
        """
        return list(self.__servers.values())

    def add_server(self, server: Server) -> None:
        """Adds a new server to the cache.

        If a similar server already exists, It will be overwritten.

        Parameters
        ----------
        server: :class:`Server`
            The server to add.
        """
        self.__servers[server.id] = server

    def get_server(self, server_id: str) -> Optional[Server]:
        """Gets a server from the cache.

        Parameters
        ----------
        server_id: :class:`str`
            The ID of server to get.

        Returns
        -------
        Optional[:class:`Server`]
            The requested server; if exists. Otherwise ``None``.
        """
        return self.__servers.get(server_id)

    def remove_server(self, server_id: str) -> Optional[Server]:
        """Removes a server from the cache.

        Parameters
        ----------
        server_id: :class:`str`
            The ID of server to remove.

        Returns
        -------
        Optional[:class:`Server`]
            The remoevd server; if exists. Otherwise ``None``.
        """
        return self.__servers.pop(server_id, None)

    def channels(self) -> List[ChannelT]:
        """The channels that are currently cached.

        Returns
        -------
        List[Union[:class:`ServerChannel`, :class:`PrivateChannel`]]
        """
        return list(self.__channels.values())

    def add_channel(self, channel: ChannelT) -> None:
        """Adds a new channel to the cache.

        If a similar channel already exists, It will be overwritten.

        Parameters
        ----------
        channel: Union[:class:`ServerChannel`, :class:`PrivateChannel`]
            The channel to add.
        """
        self.__channels[channel.id] = channel

    def get_channel(self, channel_id: str) -> Optional[ChannelT]:
        """Gets a channel from the cache.

        Parameters
        ----------
        channel_id: :class:`str`
            The ID of channel to get.

        Returns
        -------
        Optional[Union[:class:`ServerChannel`, :class:`PrivateChannel`]]
            The requested channel; if exists. Otherwise ``None``.
        """
        return self.__channels.get(channel_id)

    def remove_channel(self, channel_id: str) -> Optional[ChannelT]:
        """Removes a channel from the cache.

        Parameters
        ----------
        channel_id: :class:`str`
            The ID of channel to remove.

        Returns
        -------
        Optional[Union[:class:`ServerChannel`, :class:`PrivateChannel`]]
            The remoevd channel; if exists. Otherwise ``None``.
        """
        return self.__channels.pop(channel_id, None)
