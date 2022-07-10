# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, TypedDict
from typing_extensions import NotRequired
from luster.types.file import File

if TYPE_CHECKING:
    from luster.types.enums import PresenceType, RelationshipStatus

__all__ = (
    "UserStatus",
    "UserProfile",
    "PartialUserBot",
    "Relationship",
    "User",
)


class UserStatus(TypedDict):
    """Represents the status of a user."""

    text: NotRequired[Optional[str]]
    """The custom status text."""

    presense: PresenceType
    """The current presence state of the user."""


class UserProfile(TypedDict):
    """Represents the profile of a user."""

    content: NotRequired[Optional[str]]
    """The user's bio."""

    background: NotRequired[Optional[File]]
    """The custom banner background of user."""


class PartialUserBot(TypedDict):
    """Represents a "partial" bot attached to :attr:`User.bot`"""

    owner: str
    """The ID of bot's owner."""


class Relationship(TypedDict):
    """Represents a relationship of a user with another user."""

    _id: str
    """The ID of user that this relationship is with."""

    status: RelationshipStatus
    """The current relationship status."""


class User(TypedDict):
    """Represents a user's structure."""

    _id: str
    """The user's unique ID."""

    username: str
    """The user's username."""

    avatar: NotRequired[Optional[File]]
    """The user's avatar."""

    relations: NotRequired[Optional[List[Relationship]]]
    """The user's relationships with other users."""

    badges: NotRequired[Optional[int]]
    """The bitfield value for user profile badges."""

    status: NotRequired[Optional[UserStatus]]
    """The user's current activity status."""

    profile: NotRequired[Optional[UserProfile]]
    """The user's profile."""

    flags: NotRequired[Optional[int]]
    """The enum of user's flags."""

    privileged: bool
    """Whether this user is privileged."""

    bot: NotRequired[Optional[PartialUserBot]]
    """If the user is a bot, includes the partial bot information."""

    relationship: NotRequired[Optional[RelationshipStatus]]
    """The user's relationship with other users or themselves."""

    online: NotRequired[Optional[bool]]
    """Whether the user is currently online."""
