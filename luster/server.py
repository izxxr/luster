# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional
from luster.internal.helpers import handle_optional_field
from luster.internal.mixins import StateAware
from luster.file import File

if TYPE_CHECKING:
    from luster.channels import ServerChannel
    from luster.state import State
    from luster import types

__all__ = (
    "Server",
)


class Server(StateAware):
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
    )

    def __init__(self, data: types.Server, state: State) -> None:
        self._state = state
        self._update_from_data(data)

    def _update_from_data(self, data: types.Server):
        # TODO: categories, system_messages, roles, default_permissions
        self.id = data["_id"]
        self.owner_id = data["owner"]
        self.name = data["name"]
        self.description = data.get("description")
        self.channel_ids = data.get("channels", [])
        self.flags = handle_optional_field(data, "flags", 0, None)
        self.nsfw = data.get("nsfw", False)
        self.discoverable = data.get("discoverable", False)
        self.analytics = data.get("analytics", False)

        icon = data.get("icon")
        banner = data.get("banner")

        self.icon = File(icon, self._state) if icon else None
        self.banner = File(banner, self._state) if banner else None

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
