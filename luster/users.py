# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union
from luster.internal.helpers import (
    MISSING,
    handle_optional_field,
    inner_upsert,
    upsert_remove_value,
    get_attachment_id,
)
from luster.internal.mixins import StateAware
from luster.file import File
from luster.http import HTTPHandler
from luster.enums import RelationshipStatus, PresenceType

if TYPE_CHECKING:
    from io import BufferedReader
    from luster.state import State
    from luster.types.users import (
        User as UserData,
        Relationship as RelationshipData,
        Profile as ProfileData,
        Status as StatusData,
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

    def __init__(self, data: ProfileData, user: User) -> None:
        self.user = user
        self._state = user.state
        self._update_from_data(data)

    def _update_from_data(self, data: ProfileData):
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

    def __init__(self, data: StatusData, user: User) -> None:
        self.user = user
        self._state = user.state
        self._update_from_data(data)

    def _update_from_data(self, data: StatusData):
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

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id!r}, username={self.username!r})"

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

    @property
    def default_avatar_url(self) -> str:
        """The URL pointing to user's default avatar.

        This is not user's actual avatar.

        Returns
        -------
        :class:`str`
        """
        return f"{HTTPHandler.BASE_URL}/users/{self.id}/default_avatar"

    @property
    def display_avatar_url(self) -> str:
        """The URL pointing to user's displayed avatar.

        This property is a shorthand that returns the user's
        actual avatar URL if they have one and falls back to
        default avatar URL if they don't have a custom avatar.

        Returns
        -------
        :class:`str`
        """
        avatar = self.avatar
        if avatar is None:
            return self.default_avatar_url
        return avatar.url

    def is_bot(self) -> bool:
        """Indicates if the user is a bot.

        Returns
        -------
        :class:`bool`
        """
        return self.bot is not None

    async def fetch_profile(self) -> Profile:
        """Fetches the profile of this user.

        Returns
        -------
        :class:`Profile`
            The user's profile

        Raises
        ------
        HTTPException
            The request failed.
        HTTPNotFound
            You are not allowed to fetch this user's profile.
        """
        data = await self._state.http_handler.fetch_profile(self.id)
        return Profile(data, self)

    async def edit(
        self,
        *,
        status_text: Optional[str] = MISSING,
        status_presence: Optional[RawPresenceType] = MISSING,
        profile_content: Optional[str] = MISSING,
        profile_background: Optional[Union[str, BufferedReader]] = MISSING,
        avatar: Optional[Union[str, BufferedReader]] = MISSING,
    ) -> User:
        """Edits the user.

        This method requires the user to be the current authenticated
        user. Otherwise, This method will fail.

        Passing ``None`` to the parameters hinted as :class:`typing.Optional`
        will remove that field.

        Parameters
        ----------
        status_text: Optional[:class:`str`]
            The user's custom status.
        status_presence: Optional[:class:`types.PresenceType`]
            The user's presence type.

            .. seealso:: The :class:`PresenceType` enum.
        profile_content: Optional[:class:`str`]
            The content of profile "aka" the bio section.
        profile_background: Optional[Union[:class:`str`, :class:`io.BufferedReader`]]
            The profile background of the user.
            |attachment-parameter-note|
        avatar: Optional[Union[:class:`str`, :class:`io.BufferedReader`]]
            The avatar of the user.
            |attachment-parameter-note|

        Returns
        -------
        :class:`User`
            The updated user.

        Raises
        ------
        HTTPException
            Failed to edit the user.
        """
        json = {}

        if status_text is not MISSING:
            if status_text is None:
                upsert_remove_value(json, "StatusText")
            else:
                inner_upsert(json, "status", "text", status_text)

        if status_presence is not MISSING:
            if status_presence is None:
                upsert_remove_value(json, "StatusPresence")
            else:
                inner_upsert(json, "status", "presence", status_presence)

        if profile_content is not MISSING:
            if profile_content is None:
                upsert_remove_value(json, "ProfileContent")
            else:
                inner_upsert(json, "profile", "content", profile_content)

        state = self._state
        http = state.http_handler

        if profile_background is not MISSING:
            if profile_background is None:
                upsert_remove_value(json, "ProfileBackground")
            else:
                attachment_id = await get_attachment_id(http=http, target=profile_background, tag="backgrounds")
                inner_upsert(json, "profile", "background", attachment_id)

        if avatar is not MISSING:
            if avatar is None:
                upsert_remove_value(json, "Avatar")
            else:
                json["avatar"] = await get_attachment_id(http=http, target=avatar, tag="avatars")


        # json is now equivalent to types.EditUser
        data = await http.edit_user(json)  # type: ignore
        return User(data, state)
