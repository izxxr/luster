# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023
# Credits: Rapptz/discord.py for idea of Object

from __future__ import annotations

__all__ = (
    "Object",
)


class Object:
    """Represents a generic object.

    This class implements the minimal functionality required to be
    compatible with :class:`BaseModel`. This class can be initialized
    manually and can be useful in certain cases.

    An example application of this class is when you want to perform
    an HTTP operation on a Revolt entity and you just have the ID of
    that entity. Instead of fetching that entity first, you can pass
    the instance of this class to HTTP method. Most (not all) HTTP
    methods allow you to pass this class.

    In many cases, This class may also be returned in API responses.
    These are the cases when library could not resolve the complete
    entity from cache so it falls back to this class.

    Parameters
    ----------
    id: :class:`str`
        The ID for this object.
    """

    __slots__ = (
        "id",
    )

    def __init__(self, id: str) -> None:
        self.id = id
