# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

from typing import Protocol, runtime_checkable

__all__ = (
    "BaseModel",
)


@runtime_checkable
class BaseModel(Protocol):
    """A protocol that acts as a base for most data models.

    Almost all data model classes provided by the library are
    compatible with this class. The :class:`Object` class allows
    you to create custom models and provides the minimal functionality
    required to be compatible with this class.

    This protocol supports runtime checks such as :func:`isinstance`
    and :func:`issubclass`.

    Attributes
    ----------
    id: :class:`str`
        The ID of this model.
    """
    __slots__ = ()

    id: str
