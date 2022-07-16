# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional
from typing_extensions import Self
from luster.internal.helpers import MISSING, handle_optional_field
from luster.internal.mixins import StateAware
from luster.object import Object
from luster.protocols import BaseModel
from luster.file import File

import copy

if TYPE_CHECKING:
    from luster.channels import ServerChannel
    from luster.state import State
    from luster import types

__all__ = (
    "Server",
    "SystemMessages",
)


class SystemMessages:
    """Represents system messages channels assignment for a server.

    This class can generally be obtained using :attr:`Server.system_messages`
    attribute. You may also initialize this class when editing system messages
    using :meth:`Server.edit` method.

    Parameters
    ----------
    user_joined: Optional[:class:`BaseModel`]
        The channel used for notifying user joins.
    user_left: Optional[:class:`BaseModel`]
        The channel used for notifying user leaves.
    user_kicked: Optional[:class:`BaseModel`]
        The channel used for notifying user kicks.
    user_banned: Optional[:class:`BaseModel`]
        The channel used for notifying user bans.
    """

    __valid_keys__ = ("user_joined", "user_left", "user_kicked", "user_banned")
    __slots__ = ("_user_joined", "_user_left", "_user_kicked", "_user_banned")

    def __init__(
        self,
        *,
        user_joined: Optional[BaseModel] = MISSING,
        user_left: Optional[BaseModel] = MISSING,
        user_kicked: Optional[BaseModel] = MISSING,
        user_banned: Optional[BaseModel] = MISSING,
    ) -> None:
        self._user_joined = user_joined
        self._user_left = user_left
        self._user_kicked = user_kicked
        self._user_banned = user_banned


    @property
    def user_joined(self) -> Optional[BaseModel]:
        """The channel assigned for notifications regarding users joining.

        Returns
        -------
        Optional[:class:`BaseModel`]
        """
        ret = self._user_joined
        if ret is MISSING:
            return None

        return ret

    @user_joined.setter
    def user_joined(self, value: Optional[BaseModel]) -> None:
        self._user_joined = value 

    @property
    def user_left(self) -> Optional[BaseModel]:
        """The channel assigned for notifications regarding users leaving.

        Returns
        -------
        Optional[:class:`BaseModel`]
        """
        ret = self._user_left
        if ret is MISSING:
            return None

        return ret

    @user_left.setter
    def user_left(self, value: Optional[BaseModel]) -> None:
        self._user_left = value 

    @property
    def user_kicked(self) -> Optional[BaseModel]:
        """The channel assigned for notifications regarding user kicks.

        Returns
        -------
        Optional[:class:`BaseModel`]
        """
        ret = self._user_kicked
        if ret is MISSING:
            return None

        return ret

    @user_kicked.setter
    def user_kicked(self, value: Optional[BaseModel]) -> None:
        self._user_kicked = value 

    @property
    def user_banned(self) -> Optional[BaseModel]:
        """The channel assigned for notifications regarding user bans.

        Returns
        -------
        Optional[:class:`BaseModel`]
        """
        ret = self._user_banned
        if ret is MISSING:
            return None

        return ret

    @user_banned.setter
    def user_banned(self, value: Optional[BaseModel]) -> None:
        self._user_banned = value

    def copy(self) -> SystemMessages:
        """Creates the shallow copy of this class.

        Returns
        -------
        :class:`SystemMessages`
            The created shallow copy.
        """
        return copy.copy(self)

    def to_dict(self) -> types.SystemMessages:
        """Returns a dictionary format of this class compatible with Revolt API schema.

        Returns
        -------
        :class:`types.SystemMessages`
        """
        ret = {}

        join = self._user_joined
        left = self._user_left
        kicked = self._user_kicked
        banned = self._user_banned

        if join is not MISSING:
            ret["user_joined"] = join.id if join is not None else None
        if left is not MISSING:
            ret["user_left"] = left.id if left is not None else None
        if kicked is not MISSING:
            ret["user_kicked"] = kicked.id if kicked is not None else None
        if banned is not MISSING:
            ret["user_banned"] = banned.id if banned is not None else None

        # This is equivalent to types.SystemMessages now
        return ret  # type: ignore

    @classmethod
    def from_dict(cls, data: types.SystemMessages, *, state: Optional[State] = None) -> Self:
        """Converts a dictionary to :class:`SystemMessages`.

        Parameters
        ----------
        data: :class:`types.SystemMessages`
            The dictionary to convert.
        state: Optional[:class:`State`]
            The state to use for resolving channels. If not given,
            all attributes fallback to use :class:`Object` class.

        Returns
        -------
        :class:`SystemMessages`
            The converted instance.
        """
        if state:
            cache = state.cache
        else:
            cache = None

        ret = cls()

        for field, channel_id in data.items():
            if not field in cls.__valid_keys__:
                continue

            if channel_id is None:
                channel = None
            elif cache is None:
                channel = Object(channel_id)  # type: ignore
            else:
                channel = cache.get_channel(channel_id)  # type: ignore
                if channel is None:
                    channel = Object(channel_id)  # type: ignore

            setattr(ret, field, channel)

        return ret


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
    system_messages: :class:`SystemMessages`
        The system messages channels assignments.
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

        icon = data.get("icon")
        banner = data.get("banner")
        system_messages = data.get("system_messages") or {}

        self.icon = File(icon, self._state) if icon else None
        self.banner = File(banner, self._state) if banner else None
        self.system_messages = SystemMessages.from_dict(system_messages, state=self._state)

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
