# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Mapping, Optional, Type, Union
from luster.types.websocket import ChannelUpdateEventData
from luster.internal.mixins import StateAware
from luster.internal.update_handler import UpdateHandler, handle_update
from luster.internal.helpers import MISSING, get_attachment_id, upsert_remove_value
from luster.enums import ChannelType
from luster.file import File
from luster.users import User
from luster.protocols import BaseModel
from luster.permissions import Permissions, PermissionOverwrite

if TYPE_CHECKING:
    from io import BufferedReader
    from luster.server import Server
    from luster.state import State
    from luster import types

__all__ = (
    "ServerChannel",
    "TextChannel",
    "VoiceChannel",
    "PrivateChannel",
    "SavedMessages",
    "DirectMessage",
    "Group",
    "Category",
)


ChannelT = Union["ServerChannel", "PrivateChannel"]


def channel_factory(tp: Any) -> Type[ChannelT]:
    if tp == ChannelType.TEXT_CHANNEL:
        return TextChannel
    if tp == ChannelType.VOICE_CHANNEL:
        return VoiceChannel
    if tp == ChannelType.SAVED_MESSAGES:
        return SavedMessages
    if tp == ChannelType.DIRECT_MESSAGE:
        return DirectMessage
    if tp == ChannelType.GROUP:
        return Group

    # Fallback to PrivateChannel as it is the most
    # minimal channel type
    return PrivateChannel


class _EditChannelMixin(StateAware):
    id: str

    async def edit(
        self,
        *,
        name: str = MISSING,
        description: Optional[str] = MISSING,
        icon: Optional[Union[str, BufferedReader]] = MISSING,
        nsfw: bool = MISSING,
    ) -> None:
        """Edits the channel.

        This requires the :attr:`Permissions.manage_channel` permission
        in the group channel or the parent server when called in a server
        channel context.

        Parameters
        ----------
        name: Optional[:class:`str`]
            The name of this channel.
        description: Optional[:class:`str`]
            The description of this channel. Passing ``None`` will
            remove the description.
        icon: Optional[Union[:class:`str`, :class:`io.BufferedReader`]]
            The icon of this channel.
            |attachment-parameter-note|
        nsfw: :class:`bool`
            Whether this channel is marked as NSFW.
        """
        json = {}
        http = self._state.http_handler

        if name:
            json["name"] = name

        if description is not MISSING:
            if description is None:
                upsert_remove_value(json, "Description")
            else:
                json["description"] = description

        if icon is not MISSING:
            if icon is None:
                upsert_remove_value(json, "Icon")
            else:
                json["icon"] = await get_attachment_id(http, icon, "icons")

        if nsfw is not MISSING:
            json["nsfw"] = nsfw

        if json:
            # data is equivalent to types.EditChannelJSON now
            data = await http.edit_channel(self.id, json=json)  # type: ignore

            # self.__class__ will resolve to a valid channel type
            return self.__class__(data, self._state)  # type: ignore


class ServerChannel(_EditChannelMixin, UpdateHandler[ChannelUpdateEventData]):
    """The common base class for channels in a server.

    For convenience, This type has been narrowed down to following
    subclasses:

    - :class:`TextChannel`
    - :class:`VoiceChannel`

    Attributes
    ----------
    id: :class:`str`
        The ID of this channel.
    type: :class:`types.ChannelTypeServer`
        The type of this channel.
    server_id: :class:`str`
        The ID of server that this channel belongs to.
    name: :class:`str`
        The name of this channel.
    description: Optional[:class:`str`]
        The description of this channel.
    nsfw: :class:`bool`
        Whether this channel is marked as NSFW.
    """
    if TYPE_CHECKING:
        id: str
        type: types.ChannelTypeServer
        server_id: str
        name: str
        description: Optional[str]
        nsfw: bool
        _default_permissions: types.Permissions
        _role_permissions: Dict[str, types.Permissions]

    __slots__ = (
        "_state",
        "id",
        "type",
        "server_id",
        "name",
        "description",
        "nsfw",
        "default_permissions",
        "role_permissions",
    )

    def __init__(self, data: types.ServerChannel, state: State) -> None:
        self._state = state
        self._update_from_data(data)

    def _update_from_data(self, data: types.ServerChannel) -> None:
        self.id = data["_id"]
        self.type = data["channel_type"]
        self.server_id = data["server"]
        self.name = data["name"]
        self.description = data.get("description")
        self.nsfw = data.get("nsfw", False)

        self._default_permissions = data.get("default_permissions", {"a": 0, "d": 0})
        self._role_permissions = data.get("role_permissions", {})

    def handle_field_removals(self, fields: List[types.ChannelRemoveField]) -> None:
        for field in fields:
            if field == "Icon":
                self.icon = None
            if field == "Description":
                self.description = None

    @handle_update("name")
    def _handle_update_name(self, new: str) -> None:
        self.name = new

    @handle_update("description")
    def _handle_update_description(self, new: str) -> None:
        self.description = new

    @handle_update("icon")
    def _handle_update_icon(self, new: types.File) -> None:
        self.icon = File(new, self._state)

    @handle_update("nsfw")
    def _handle_update_nsfw(self, new: bool) -> None:
        self.nsfw = new

    @handle_update("default_permissions")
    def _handle_update_default_permissions(self, new: types.Permissions) -> None:
        self._default_permissions = new

    @handle_update("role_permissions")
    def _handle_update_role_permissions(self, new: Dict[str, types.Permissions]) -> None:
        self._role_permissions = new

    @property
    def server(self) -> Optional[Server]:
        """The server for this channel.

        This property might rarely return None if the server
        relating to this channel is not cached.

        Returns
        -------
        Optional[:class:`Server`]
            The channel's server.
        """
        return self._state.cache.get_server(self.server_id)

    @property
    def default_permissions(self) -> PermissionOverwrite:
        """The default permission overwrite on this channel.

        Returns
        -------
        :class:`PermissionOverwrite`
        """
        allow = Permissions(self._default_permissions["a"])
        deny = Permissions(self._default_permissions["d"])
        return PermissionOverwrite.from_pair(allow, deny)

    @property
    def role_permissions(self) -> Mapping[str, PermissionOverwrite]:
        """The default permission overwrite on this channel.

        Returns
        -------
        :class:`PermissionOverwrite`
        """
        permissions: Mapping[str, PermissionOverwrite] = {}

        for role_id, overwrite in self._role_permissions.items():
            allow = Permissions(overwrite["a"])
            deny = Permissions(overwrite["d"])
            permissions[role_id] = PermissionOverwrite.from_pair(allow, deny)

        return permissions

    async def delete(self) -> None:
        """Deletes the channel.

        This operation requires the :attr:`Permissions.manage_channels`
        permission in the parent server.

        Raises
        ------
        HTTPException
            The deletion failed.
        HTTPForbidden
            You are not allowed to do this.
        """
        await self._state.http_handler.delete_channel(self.id)


class TextChannel(ServerChannel):
    """Represents a text channel in a server.

    This class inherits the :class:`ServerChannel` class.

    Attributes
    ----------
    last_message_id: Optional[:class:`str`]
        The ID of last message sent in this channel.
    """
    if TYPE_CHECKING:
        last_message_id: Optional[str]

    __slots__ = ("last_message_id",)

    def _update_from_data(self, data: types.ServerChannel) -> None:
        super()._update_from_data(data)
        self.last_message_id = data.get("last_message_id")


class VoiceChannel(ServerChannel):
    """Represents a voice channel in a server.

    This class inherits the :class:`ServerChannel` class.
    """


class PrivateChannel(StateAware, UpdateHandler[ChannelUpdateEventData]):
    """The common base class for private channels.

    For convenience, This type has been narrowed down to following
    subclasses:

    - :class:`SavedMessages`
    - :class:`DirectMessage`
    - :class:`Group`

    Attributes
    ----------
    id: :class:`str`
        The ID of this channel.
    type: :class:`types.ChannelTypePrivate`
        The type of this channel.
    """
    if TYPE_CHECKING:
        id: str
        type: types.ChannelTypePrivate

    __slots__ = (
        "_state",
        "id",
        "type",
    )

    def __init__(self, data: types.PrivateChannel, state: State) -> None:
        self._state = state
        self._update_from_data(data)

    def _update_from_data(self, data: Any) -> None:
        self.id = data["_id"]
        self.type = data["channel_type"]

    def handle_field_removals(self, fields: List[types.ChannelRemoveField]) -> None:
        pass

    async def delete(self) -> None:
        """Deletes the channel.

        In case of groups, This leaves the channel and in case of direct
        messages, This closes the channel.

        When called in a group context, :attr:`~Permissions.manage_channel`
        permission is required.

        Raises
        ------
        HTTPException
            The deletion failed.
        HTTPForbidden
            You are not allowed to do this.
        """
        await self._state.http_handler.delete_channel(self.id)


class SavedMessages(PrivateChannel):
    """Represents a saved messages channel.

    This is often referred to as "Saved Notes" channel in the Revolt
    UI and is limited to a single user.

    This class inherits :class:`PrivateChannel` class.

    Attributes
    ----------
    user_id: :class:`str`
        The ID of user that this channel belongs to.
    """
    if TYPE_CHECKING:
        user_id: str

    __slots__ = ("user_id",)

    def _update_from_data(self, data: types.SavedMessages) -> None:
        super()._update_from_data(data)
        self.user_id = data["user"]


class DirectMessage(PrivateChannel):
    """Represents a direct message (DM) between two users.

    This class inherits :class:`PrivateChannel` class.

    Attributes
    ----------
    recipient_ids: List[:class:`str`]
        The IDs of recipients that this channel is with.
    active: :class:`bool`
        Whether this channel is active on both sides.
    last_message_id: Optional[:class:`str`]
        The ID of last message sent in this channel.
    """
    if TYPE_CHECKING:
        recipient_ids: List[str]
        active: bool
        last_message_id: Optional[str]

    __slots__ = ("recipient_ids", "active", "last_message_id")

    def _update_from_data(self, data: types.DirectMessage) -> None:
        super()._update_from_data(data)

        self.recipient_ids = data.get("recipients", [])
        self.active = data.get("active", False)
        self.last_message_id = data.get("last_message_id")

    @handle_update("recipients")
    def _handle_update_recipients(self, new: List[str]) -> None:
        self.recipient_ids = new

    @handle_update("active")
    def _handle_update_active(self, new: bool) -> None:
        self.active = new


class Group(PrivateChannel, _EditChannelMixin, UpdateHandler[ChannelUpdateEventData]):
    """Represents a group channel between several users.

    This class inherits :class:`PrivateChannel` class.

    Attributes
    ----------
    name: :class:`str`
        The name of this channel.
    owner_id: :class:`str`
        The ID of user that this channel is with.
    recipient_ids: List[:class:`str`]
        The IDs of recipients that are in this channel.
    description: Optional[:class:`str`]
        The description of this channel.
    icon: Optional[:class:`File`]
        The icon of this channel.
    last_message_id: Optional[:class:`str`]
        The ID of last message sent in this channel.
    nsfw: :class:`bool`
        Whether this channel is marked as NSFW.
    permissions: :class:`Permissions`
        The default set of permissions applied to every member in the group.
    """
    if TYPE_CHECKING:
        name: str
        owner_id: str
        recipient_ids: List[str]
        description: Optional[str]
        icon: Optional[File]
        nsfw: bool
        last_message_id: Optional[str]
        default_permissions: Permissions

    __slots__ = (
        "name",
        "owner_id",
        "recipient_ids",
        "description",
        "icon",
        "nsfw",
        "last_message_id",
        "default_permissions",
    )

    def _update_from_data(self, data: types.Group) -> None:
        super()._update_from_data(data)

        self.name = data["name"]
        self.owner_id = data["owner"]
        self.recipient_ids = data.get("recipients", [])
        self.description = data.get("description")
        self.nsfw = data.get("nsfw", False)
        self.last_message_id = data.get("last_message_id")
        self.default_permissions = Permissions(data.get("permissions", 0))

        icon = data.get("icon")
        self.icon = File(icon, self._state) if icon else None

    def handle_field_removals(self, fields: List[types.ChannelRemoveField]) -> None:
        for field in fields:
            if field == "Icon":
                self.icon = None
            if field == "Description":
                self.description = None

    @handle_update("name")
    def _handle_update_name(self, new: str) -> None:
        self.name = new

    @handle_update("recipients")
    def _handle_update_recipients(self, new: List[str]) -> None:
        self.recipient_ids = new

    @handle_update("description")
    def _handle_update_description(self, new: str) -> None:
        self.description = new

    @handle_update("icon")
    def _handle_update_icon(self, new: types.File) -> None:
        self.icon = File(new, self._state)

    @handle_update("nsfw")
    def _handle_update_nsfw(self, new: bool) -> None:
        self.nsfw = new

    @handle_update("permissions")
    def _handle_update_permissions(self, new: int) -> None:
        self.default_permissions = Permissions(new)

    async def fetch_owner(self) -> User:
        """Fetches the user that owns this group.

        Returns
        -------
        :class:`User`
            The group owner.

        Raises
        ------
        HTTPException
            Failed to fetch the owner.
        """
        state = self._state
        data = await state.http_handler.fetch_user(self.owner_id)
        return User(data, state)

    async def fetch_recipients(self) -> List[User]:
        """Fetches the users that are part of this group.

        Returns
        -------
        List[:class:`User`]
            The recipients of this group.

        Raises
        ------
        HTTPException
            The fetching failed.
        """
        state = self._state
        data = await state.http_handler.fetch_group_members(channel_id=self.id)
        return [User(u, state) for u in data]

    async def add_recipient(self, user: BaseModel) -> None:
        """Adds a new member to this group.

        Parameters
        ----------
        user: :class:`BaseModel`
            The user to add.

        Raises
        ------
        HTTPForbidden
            You are not allowed to add members.
        HTTPException
            The addition failed.
        """
        await self._state.http_handler.add_group_member(self.id, user.id)

    async def remove_recipient(self, user: BaseModel) -> None:
        """Removes a member from this group.

        Parameters
        ----------
        user: :class:`BaseModel`
            The user to remove.

        Raises
        ------
        HTTPForbidden
            You are not allowed to remove members.
        HTTPException
            The removal failed.
        """
        await self._state.http_handler.remove_group_member(self.id, user.id)


class Category(StateAware):
    """Represents a category for other channels.

    Attributes
    ----------
    id: :class:`str`
        The ID of this category.
    title: :class:`str`
        The title of this category.
    channel_ids: List[:class:`str`]
        The list of channel IDs that are in this category.
    """

    if TYPE_CHECKING:
        id: str
        title: str
        channel_ids: List[str]

    def __init__(self, data: types.Category, state: State) -> None:
        self._state = state
        self._update_from_data(data)

    def _update_from_data(self, data: types.Category):
        self.id = data["id"]
        self.title = data["title"]
        self.channel_ids = data.get("channels", [])

    def channels(self) -> List[ServerChannel]:
        """The list of channels in this category.

        Returns
        -------
        List[:class:`ServerChannel`]
            The channels associated to this category.
        """
        ret: List[ServerChannel] = []
        cache = self._state.cache

        for channel_id in self.channel_ids:
            channel = cache.get_channel(channel_id)
            if channel:
                # Should always be a ServerChannel
                ret.append(channel)  # type: ignore

        return ret
