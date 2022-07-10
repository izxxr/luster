# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional
from luster.internal.helpers import handle_optional_field
from luster.internal.mixins import StateAware
from luster.file import File
from luster.enums import RelationshipStatus, PresenceType

if TYPE_CHECKING:
    from luster.state import State
    from luster.types.users import (
        User as UserData,
        Relationship as RelationshipData,
        UserProfile as UserProfileData,
        UserStatus as UserStatusData,
        PartialUserBot as PartialUserBotData,
    )
    from luster.types.enums import (
        RelationshipStatus as RawRelationshipStatus,
        PresenceType as RawPresenceType,
    )


__all__ = (
    "User",
    "Relationship",
    "Profile",
    "Status",
    "PartialUserBot",
)


class Relationship(StateAware):
    """Represents a relationship of a user with another user.

    Attributes
    ----------
    user: :class:`User`
        The user that the relationship belong to.
    id: :class:`str`
        The ID of user that the relationship is with.
    status: :data:`types.RelationshipStatus`
        The status of this relationship.

        .. seealso:: :class:`RelationshipStatus` enum
    """
    if TYPE_CHECKING:
        id: str
        status: RawRelationshipStatus

    __slots__ = (
        "_state",
        "user",
        "id",
        "status",
    )

    def __init__(self, data: RelationshipData, user: User) -> None:
        self.user = user
        self._state = user.state
        self._update_from_data(data)

    def _update_from_data(self, data: RelationshipData):
        self.id = data["_id"]
        self.status = data["status"]


class Profile(StateAware):
    """Represnts a user's profile.

    Attributes
    ----------
    user: :class:`User`
        The user that the profile belong to.
    content: Optional[:class:`str`]
        The user's bio, if any set.
    background: Optional[:class:`File`]
        The user's banner background, if any set.
    """
    if TYPE_CHECKING:
        content: Optional[str]
        background: Optional[File]

    __slots__ = (
        "_state",
        "user",
        "content",
        "background",
    )

    def __init__(self, data: UserProfileData, user: User) -> None:
        self.user = user
        self._state = user.state
        self._update_from_data(data)

    def _update_from_data(self, data: UserProfileData):
        self.content = data.get("content")

        background = data.get("background")
        self.background = File(background, state=self._state) if background else None


class Status(StateAware):
    """Represents the status of a user.

    Attributes
    ----------
    user: :class:`User`
        The user that the status belong to.
    text: Optional[:class:`str`]
        The user's custom status text, if any set.
    presence: :data:`types.PresenceType`
        The user's presence type.

        .. seealso:: :class:`PresenceType` enum
    """
    if TYPE_CHECKING:
        text: Optional[str]
        presence: RawPresenceType

    __slots__ = (
        "_state",
        "user",
        "text",
        "presence",
    )

    def __init__(self, data: UserStatusData, user: User) -> None:
        self.user = user
        self._state = user.state
        self._update_from_data(data)

    def _update_from_data(self, data: UserStatusData):
        self.text = data.get("text")
        self.presence = handle_optional_field(data, "presence", PresenceType.INVISIBLE, None)


class PartialUserBot(StateAware):
    """Represents a "partial" bot.

    This partial model only contains the subset of actual
    model. You can obtain this from :attr:`User.bot`.

    Attributes
    ----------
    user: :class:`User`
        The user that this model belong to.
    owner_id: :class:`str`
        The ID of owner of this bot.
    """
    if TYPE_CHECKING:
        owner_id: str

    __slots__ = (
        "_state",
        "user",
        "owner_id",
    )

    def __init__(self, data: PartialUserBotData, user: User) -> None:
        self.user = user
        self._state = user.state
        self._update_from_data(data)

    def _update_from_data(self, data: PartialUserBotData):
        self.owner_id = data["owner"]


class User(StateAware):
    """Represents a user entity.

    Attributes
    ----------
    id: :class:`str`
        The unique ID of this user.
    username: :class:`str`
        The username of this user.
    avatar: Optional[:class:`File`]
        The avatar of user, if they have one.
    badges: :class:`int`
        The bitfield value for user profile badges.
    flags: :class:`int`
        The bitfield value for user flags.
    privileged: :class:`bool`
        Whether the user is a privileged user.
    relationship: :data:`types.RelationshipStatus`
        The relationship of user with another user or themselves.
    online: :class:`bool`
        Whether the user is online right now.
    relationships: List[:class:`Relationship`]
        The relationships of this user with other users.
    profile: Optional[:class:`Profile`]
        The user's profile.
    status: Optional[:class:`Status`]
        The user's current status.
    """

    if TYPE_CHECKING:
        id: str
        username: str
        avatar: Optional[File]
        badges: int
        flags: int
        privileged: bool
        relationship: RawRelationshipStatus
        online: bool
        relationships: List[Relationship]
        profile: Optional[Profile]
        status: Optional[Status]

    __slots__ = (
        "_state",
        "id",
        "username",
        "avatar",
        "badges",
        "flags",
        "privileged",
        "relationship",
        "online",
        "relationships",
        "profile",
        "status",
        "bot",
    )

    def __init__(self, data: UserData, state: State) -> None:
        self._state = state
        self._update_from_data(data)

    def _update_from_data(self, data: UserData):
        self.id = data["_id"]
        self.username = data["username"]
        self.badges = handle_optional_field(data, "badges", 0, None)
        self.flags = handle_optional_field(data, "flags", 0, None)
        self.privileged = data.get("privileged", False)
        self.relationship = handle_optional_field(data, "relationship", RelationshipStatus.NONE, None)
        self.online = handle_optional_field(data, "online", False, None)

        avatar = data.get("avatar")
        relations = data.get("relations") or []
        profile = data.get("profile")
        status = data.get("status", None)
        bot = data.get("bot")

        self.avatar = File(avatar, state=self._state) if avatar else None
        self.relationships = [Relationship(r, self) for r in relations]
        self.profile = Profile(profile, self) if profile else None
        self.status = Status(status, self) if status else None
        self.bot = PartialUserBot(bot, self) if bot else None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, username={self.username})"