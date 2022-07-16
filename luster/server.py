# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

from typing import TYPE_CHECKING, List, Literal, Optional, Union, overload
from luster.internal.helpers import (
    MISSING,
    get_attachment_id,
    handle_optional_field,
    upsert_remove_value,
)
from luster.internal.update_handler import UpdateHandler, handle_update
from luster.internal.mixins import StateAware
from luster.types.websocket import ServerUpdateEventData
from luster.channels import Category, channel_factory
from luster.file import File
from luster.system_messages import SystemMessages

if TYPE_CHECKING:
    from io import BufferedReader
    from luster.channels import ServerChannel, TextChannel, VoiceChannel
    from luster.state import State
    from luster import types

__all__ = (
    "Server",
)


class Server(StateAware, UpdateHandler[ServerUpdateEventData]):
    """Represents a Revolt server.

    Attributes
    ----------
    id: :class:`str`
        The ID of this server.
    owner_id: :class:`str`
        The ID of user that owns this server.
    name: :class:`str`
        The name of this server.
    icon: Optional[:class:`File`]
        The server's icon, if any set.
    banner: Optional[:class:`File`]
        The server's banner, if any set.
    description: Optional[:class:`str`]
        The description of this server, if any set.
    channel_ids: List[:class:`str`]
        The list of IDs of channels in this server.
    flags: :class:`int`
        The enum for server flags.
    nsfw: :class:`bool`
        Whether this server is marked as NSFW.
    discoverable: :class:`bool`
        Whether this server is available for discovery.
    analytics: :class:`bool`
        Whether this server has enabled analytics data.
    system_messages: :class:`SystemMessages`
        The system messages channels assignments.
    categories: List[:class:`Category`]
        The list of categories associated to this server.
    """

    if TYPE_CHECKING:
        id: str
        owner_id: str
        name: str
        description: Optional[str]
        channel_ids: List[str]
        flags: int
        nsfw: bool
        discoverable: bool
        analytics: bool
        icon: Optional[File]
        banner: Optional[File]
        system_messages: SystemMessages
        categories: List[Category]

    __slots__ = (
        "_state",
        "id",
        "owner_id",
        "name",
        "description",
        "channel_ids",
        "flags",
        "nsfw",
        "discoverable",
        "analytics",
        "icon",
        "banner",
        "system_messages",
        "categories",
    )

    def __init__(self, data: types.Server, state: State) -> None:
        self._state = state
        self._update_from_data(data)

    def _update_from_data(self, data: types.Server):
        # TODO: categories, roles, default_permissions
        self.id = data["_id"]
        self.owner_id = data["owner"]
        self.name = data["name"]
        self.description = data.get("description")
        self.channel_ids = data.get("channels", [])
        self.flags = handle_optional_field(data, "flags", 0, None)
        self.nsfw = data.get("nsfw", False)
        self.discoverable = data.get("discoverable", False)
        self.analytics = data.get("analytics", False)
        self.categories = [Category(c, self._state) for c in handle_optional_field(data, "categories", [], None)]

        icon = data.get("icon")
        banner = data.get("banner")
        system_messages = data.get("system_messages") or {}

        self.icon = File(icon, self._state) if icon else None
        self.banner = File(banner, self._state) if banner else None
        self.system_messages = SystemMessages.from_dict(system_messages, state=self._state)

    def handle_field_removals(self, fields: List[types.ServerRemoveField]) -> None:
        for field in fields:
            if field == "Icon":
                self.icon = None
            elif field == "Banner":
                self.banner = None
            elif field == "Description":
                self.description = None
            elif field == "SystemMessages":
                self.system_messages = SystemMessages()
            elif field == "Categories":
                self.categories = []

    @handle_update("name")
    def _handle_update_name(self, new: str) -> None:
        self.name = new

    @handle_update("description")
    def _handle_update_description(self, new: str) -> None:
        self.description = new

    @handle_update("categories")
    def _handle_update_categories(self, new: List[types.Category]) -> None:
        self.categories = [Category(c, self._state) for c in new]

    @handle_update("system_messages")
    def _handle_update_system_messages(self, new: types.SystemMessages) -> None:
        self.system_messages = SystemMessages.from_dict(new, state=self._state)

    @handle_update("icon")
    def _handle_update_icon(self, new: types.File) -> None:
        self.icon = File(new, self._state)

    @handle_update("banner")
    def _handle_update_banner(self, new: types.File) -> None:
        self.banner = File(new, self._state)

    @handle_update("analytics")
    def _handle_update_analytics(self, new: bool) -> None:
        self.analytics = new

    @handle_update("discoverable")
    def _handle_update_discoverable(self, new: bool) -> None:
        self.discoverable = new

    @handle_update("nsfw")
    def _handle_update_nsfw(self, new: bool) -> None:
        self.nsfw = new

    def channels(self) -> List[ServerChannel]:
        """The list of channels in this server.

        Returns
        -------
        List[:class:`ServerChannel`]
        """
        channels: List[ServerChannel] = []
        cache = self._state.cache

        for channel_id in self.channel_ids:
            channel = cache.get_channel(channel_id)
            if channel is not None:
                # narrowed type is always ServerChannel
                channels.append(channel)  # type: ignore

        return channels

    async def edit(
        self,
        *,
        name: str = MISSING,
        description: Optional[str] = MISSING,
        icon: Optional[Union[str, BufferedReader]] = MISSING,
        banner: Optional[Union[str, BufferedReader]] = MISSING,
        system_messages: SystemMessages = MISSING,
        analytics: bool = MISSING,
    ) -> Server:
        """Edits the server.

        This requires the :attr:`~Permissions.manage_server` permission
        in the server.

        Parameters
        ----------
        name: :class:`str`
            The name of server.
        description: Optional[:class:`str`]
            The description of server. Passing ``None`` removes the existing
            description of server.
        icon: Optional[Union[:class:`str`, :class:`io.BufferedReader`]]
            The icon of server. Passing ``None`` removes the icon.
            |attachment-parameter-note|
        banner: Optional[Union[:class:`str`, :class:`io.BufferedReader`]]
            The banner of server. Passing ``None`` removes the banner.
            |attachment-parameter-note|
        system_messages: Optional[:class:`SystemMessages`]
            The system messages channels of the server.
        analytics: :class:`bool`
            Whether to enable analytics data for this server.

        Returns
        -------
        :class:`Server`
            The updated server.

        Raises
        ------
        HTTPForbidden
            Missing permissions.
        HTTPException
            The editing failed.
        """
        json: types.EditServerJSON = {}
        http = self._state.http_handler

        if name is not MISSING:
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

        if banner is not MISSING:
            if banner is None:
                upsert_remove_value(json, "Banner")
            else:
                json["banner"] = await get_attachment_id(http, banner, "banners")

        if system_messages is not MISSING:
            json["system_messages"] = system_messages.to_dict()

        if analytics is not MISSING:
            json["analytics"] = analytics

        data = await http.edit_server(self.id, json)
        return Server(data, self._state)

    async def delete(self) -> None:
        """Deletes or leaves the server.

        If you own the server, this method deletes it otherwise
        leaves it.

        Raises
        ------
        HTTPException
            The request failed.
        """
        await self._state.http_handler.delete_server(self.id)

    async def mark_read(self) -> None:
        """Marks this server as read.

        Raises
        ------
        HTTPException
            The request failed.
        """
        await self._state.http_handler.mark_server_as_read(self.id)

    @overload
    async def create_channel(
        self,
        *,
        name: str,
        type: Literal["TextChannel"],
        description: str = ...,
        nsfw: bool = ...,
    ) -> TextChannel:
        ...

    @overload
    async def create_channel(
        self,
        *,
        name: str,
        type: Literal["VoiceChannel"],
        description: str = ...,
        nsfw: bool = ...,
    ) -> VoiceChannel:
        ...

    async def create_channel(
        self,
        *,
        name: str,
        type: types.ChannelTypeServer,
        description: str = MISSING,
        nsfw: bool = MISSING, 
    ) -> ServerChannel:
        """Creates a channel in this server.

        This operation requires :attr:`~Permissions.manage_channels`
        permission in the server.

        Parameters
        ----------
        name: :class:`str`
            The name of channel.
        type: :class:`types.ChannelTypeServer`
            The type of channel.
        description: :class:`str`
            The description of channel.
        nsfw: :class:`bool`
            Whether to mark the channel as NSFW.

        Returns
        -------
        :class:`ServerChannel`
            The created channel.

        Raises
        ------
        HTTPForbidden
            You are not allowed to do this.
        HTTPException
            The request failed.
        """
        json: types.CreateServerChannelJSON = {
            "name": name,
            "channel_type": type,
        }

        if description is not MISSING:
            json["description"] = description
        if nsfw is not MISSING:
            json["nsfw"] = nsfw

        data = await self._state.http_handler.create_server_channel(self.id, json)
        cls = channel_factory(data["channel_type"])
        # cls should always be Type[ServerChannel]
        return cls(data, self._state)  # type: ignore
