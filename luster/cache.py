# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Optional
from luster.internal.mixins import StateManagementMixin

if TYPE_CHECKING:
    from luster.users import User


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
        user_id: :class:`User`
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
        user_id: :class:`User`
            The ID of user to remove.

        Returns
        -------
        Optional[:class:`User`]
            The remoevd user; if exists. Otherwise ``None``.
        """
        return self.__users.pop(user_id, None)
