# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, TypedDict
from typing_extensions import NotRequired
from luster.types.file import File

if TYPE_CHECKING:
    from luster.types.enums import PresenceType, RelationshipStatus, UserRemoveField

__all__ = (
    # Objects
    "Status",
    "Profile",
    "PartialUserBot",
    "Relationship",
    "User",

    # HTTP API
    "FetchSelfResponse",
    "EditUserJSON",
    "EditUserResponse",
    "FetchUserResponse",
    "ChangeUsernameJSON",
    "ChangeUsernameResponse",
    "FetchProfileResponse",
)


class Status(TypedDict):
    """Represents the status of a user."""

    text: NotRequired[Optional[str]]
    """The custom status text."""

    presence: NotRequired[Optional[PresenceType]]
    """The current presence state of the user."""


class Profile(TypedDict):
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

    status: NotRequired[Optional[Status]]
    """The user's current activity status."""

    profile: NotRequired[Optional[Profile]]
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


class FetchSelfResponse(User):
    """Represents the response for :meth:`HTTPHandler.fetch_self` route.

    This is equivalent to :class:`User`.
    """


class EditUserJSON(TypedDict):
    """Represents the JSON body for :meth:`HTTPHandler.edit_user` route."""

    status: NotRequired[Status]
    """The payload to change the status."""

    profile: NotRequired[Profile]
    """The payload to change the user profile."""

    avatar: NotRequired[str]
    """The attachment ID for new avatar."""

    remove: NotRequired[List[UserRemoveField]]
    """The list of fields to remove from user."""


class EditUserResponse(User):
    """Represents the response for :meth:`HTTPHandler.edit_user` route.

    This is equivalent to :class:`User`.
    """


class FetchUserResponse(User):
    """Represents the response for :meth:`HTTPHandler.fetch_user` route.

    This is equivalent to :class:`User`.
    """


class ChangeUsernameJSON(TypedDict):
    """Represents the JSON body for :meth:`HTTPHandler.change_username` route."""

    username: str
    """The new username"""

    password: str
    """The current account password."""


class ChangeUsernameResponse(User):
    """Represents the response for :meth:`HTTPHandler.change_username` route.

    This is equivalent to :class:`User`.
    """


class FetchProfileResponse(Profile):
    """Represents the response for :meth:`HTTPHandler.fetch_profile` route.

    This is equivalent to :class:`Profile`.
    """
