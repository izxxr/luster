# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023
# Credits: Rapptz/discord.py for providing a nice design for bitfield flags.

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, TypeVar
from typing_extensions import Self

from luster.internal.mixins import StateAware
from luster.internal.update_handler import UpdateHandler, handle_update
from luster.flags import BaseFlags
from luster import types

if TYPE_CHECKING:
    from luster.state import State

__all__ = (
    "Permissions",
    "PermissionOverwrite",
    "Role",
)


T = TypeVar("T", bound=type)


class Permissions(BaseFlags):
    """A class that provides an interface for manipulating bitwise permissions value.

    This class provides a user friendly way of manipulating permissions value
    using simple booleans. The permissions can either be passed during initialization
    as keyword arguments or raw permission value can be passed as first parameter.

    Following special operations are supported between :class:`Permissions` instances:

    - Equality operations
    - Less than and greater than operations

    Note that this class is used in places where the permission can only take two values: enabled
    or disabled. In some cases, their may be a third option of "inheriting" permissions from a
    certain parent entity. In that case, :class:`PermissionOverwrite` is used instead. The
    example is channel role permissions.

    Attributes
    ----------
    value: :class:`int`
        The raw bitwise value of permissions.
    """

    manage_channels = 1 << 0
    """Allows managing server channels."""

    manage_channel = manage_channels
    """An alias for :attr:`.manage_channels`."""

    manage_server = 1 << 1
    """Allows managing the server settings."""

    manage_permissions = 1 << 2
    """Allows managing permissions on server and channels."""

    manage_roles = 1 << 3
    """Allows managing server roles."""

    manage_customization = 1 << 4
    """Allows managing server emojis."""

    kick_members = 1 << 6
    """Allows kicking server members."""

    ban_members = 1 << 7
    """Allows banning server members."""

    timeout_members = 1 << 8
    """Allows timing out other members."""

    assign_roles = 1 << 9
    """Allows assigning roles to members below oneselves ranking."""

    change_nickname = 1 << 10
    """Allows changing ownself nickname."""

    manage_nicknames = 1 << 11
    """Allows changing other members nickname."""

    change_avatar = 1 << 12
    """Allows changing ownself server avatar."""

    remove_avatars = 1 << 13
    """Allows removing avatars of other members."""

    view_channels = 1 << 20
    """Allows viewing the server channels."""

    read_message_history = 1 << 21
    """Allows viewing messages history of a text channel."""

    send_messages = 1 << 22
    """Allows sending messages in a text channel."""

    manage_messages = 1 << 23
    """Allows operation on messages such as deleting and pinning."""

    manage_webhooks = 1 << 24
    """Allows operation on server webhooks."""

    invite_others = 1 << 25
    """Allows creating invite for a server or channel."""

    send_embeds = 1 << 26
    """Allows attaching rich embeds on messages."""

    upload_files = 1 << 27
    """Allows uploading file in messages."""

    masquerade = 1 << 28
    """Allows changing avatar and nickname on every message."""

    react = 1 << 29
    """Allows reacting to messages."""

    connect = 1 << 30
    """Allows connecting to voice channels."""

    speak = 1 << 31
    """Allows speaking in voice channels."""

    video = 1 << 32
    """Allows streaming video in voice channels."""

    mute_members = 1 << 33
    """Allows muting other members in voice channels."""

    deafen_members = 1 << 34
    """Allows deafening other members in voice channels."""

    move_members = 1 << 35
    """Allows removing and moving members in voice channels."""


def _apply_default_permissions(cls: T) -> T:
    for flag in Permissions.__valid_flags__:
        # The flag default argument is needed so that accurate
        # value of flag is available in getter's and setter's
        # local scope.
        def getter(self: T, flag: str = flag) -> Optional[bool]:
            return self._overrides.get(flag)  # type: ignore

        def setter(self: T, value: Optional[bool], flag: str = flag):
            self._set(flag, value)  # type: ignore

        prop = property(getter, setter)
        setattr(cls, flag, prop)

    return cls


@_apply_default_permissions
class PermissionOverwrite:
    """Represents a permission overwrite.

    Permission overwrites are used to configure overriden permissions on
    certain server channels.

    This class is similar to :class:`Permissions` and takes the same keyword
    arguments. The main difference between this class and :class:`Permissions`
    is that the default value for a permission is ``None`` rather than ``False``.

    When initializing, either a boolean or ``None`` (default) can be passed
    to a permission's value:

    - ``None`` (default) represents inherit permission meaning the permission inherits
      from the server's default permissions set.
    - ``False`` represents that the permission is explicitly denied in the channel.
    - ``True`` represents that the permission is explicitly allowed in the channel.

    Equality operations between permission overwrite instances are supported.
    """

    if TYPE_CHECKING:
        manage_channels: Optional[bool]
        manage_channel: Optional[bool]
        manage_server: Optional[bool]
        manage_permissions: Optional[bool]
        manage_roles: Optional[bool]
        manage_customization: Optional[bool]
        kick_members: Optional[bool]
        ban_members: Optional[bool]
        timeout_members: Optional[bool]
        assign_roles: Optional[bool]
        change_nickname: Optional[bool]
        manage_nicknames: Optional[bool]
        change_avatar: Optional[bool]
        remove_avatars: Optional[bool]
        view_channels: Optional[bool]
        read_message_history: Optional[bool]
        send_messages: Optional[bool]
        manage_messages: Optional[bool]
        manage_webhooks: Optional[bool]
        invite_others: Optional[bool]
        send_embeds: Optional[bool]
        upload_files: Optional[bool]
        masquerade: Optional[bool]
        react: Optional[bool]
        connect: Optional[bool]
        speak: Optional[bool]
        video: Optional[bool]
        mute_members: Optional[bool]
        deafen_members: Optional[bool]
        move_members: Optional[bool]

    __slots__ = (
        "_overrides",
    )

    def __init__(self, **permissions: Optional[bool]) -> None:
        self._overrides: Dict[str, Optional[bool]] = {}

        for permission, value in permissions.items():
            self._set(permission, value)

    def __repr__(self) -> str:
        overrides = ", ".join("%s=%r" % (perm, value) for perm, value in self._overrides.items())
        return f"<{self.__class__.__name__} {overrides}>"

    def __eq__(self, o: Any) -> bool:
        if not isinstance(o, self.__class__):
            return False
        return self._overrides == o._overrides

    def _set(self, permission: str, value: Optional[bool]) -> None:
        if permission not in Permissions.__valid_flags__:
            raise TypeError("Unknown permission passed %r", permission)
        if not value in (True, False, None):
            raise TypeError("value must be a bool or None")

        self._overrides[permission] = value

    def pair(self) -> Tuple[Permissions, Permissions]:
        """Returns the allow and deny tuple pair for this overwrite.

        The first element in the returned tuple is the :class:`Permissions`
        instance with all permissions enabled that are allowed in this overwrite
        while second element is the :class:`Permissions` with all permissions
        enabled that are denied in this overwrite.

        Returns
        -------
        Tuple[:class:`Permissions`, :class:`Permissions`]
            The allow deny pair.
        """
        allow = Permissions()
        deny = Permissions()

        for permission, value in self._overrides.items():
            # Implicit check won't work here since None's
            # truth value is also False
            if value is True:
                setattr(allow, permission, True)
            elif value is False:
                setattr(deny, permission, True)

        return allow, deny

    @classmethod
    def from_pair(cls, allow: Permissions, deny: Permissions) -> Self:
        """Creates a :class:`PermissionOverwrite` from provided allow-deny pair.

        Parameters
        ----------
        allow: :class:`Permissions`
            Permissions instance with all permissions enabled that are
            allowed in the overwrite.
        deny: :class:`Permissions`
            Permissions instance with all permissions enabled that are
            denied in the overwrite.

        Returns
        -------
        :class:`PermissionOverwrite`
            The permission overwrite.
        """
        overwrite = cls()

        for flag in Permissions.__valid_flags__:
            if allow.get(flag):
                setattr(overwrite, flag, True)
            elif deny.get(flag):
                setattr(overwrite, flag, False)

        return overwrite


class Role(StateAware, UpdateHandler[types.ServerRoleUpdateEventData]):
    """Represents a server role.

    Attributes
    ----------
    id: :class:`str`
        The ID of role.
    name: :class:`str`
        The name of role.
    colour: Optional[:class:`str`]
        The CSS representation of role's colour.
    hoist: :class:`bool`
        Whether this role is displayed separate from others.
    rank: :class:`int`
        The rank of role in hierarchy.
    """
    __slots__ = (
        "id",
        "name",
        "colour",
        "hoist",
        "rank",
        "_state",
        "_permissions",
    )

    if TYPE_CHECKING:
        id: str
        name: str
        colour: Optional[str]
        hoist: bool
        rank: int

    def __init__(self, role_id: str, data: types.Role, state: State) -> None:
        self.id = role_id
        self._state = state
        self._update_from_data(data)

    def _update_from_data(self, data: types.Role) -> None:
        self.name = data["name"]
        self.colour = data.get("colour")
        self.hoist = data.get("hoist", False)
        self.rank = data.get("rank", 0)
        self._permissions = data.get("permissions", {"a": 0, "d": 0})

    def handle_field_removals(self, fields: List[types.RoleRemoveField]) -> None:
        for field in fields:
            if field == "Colour":
                self.colour = None

    @property
    def permissions(self) -> PermissionOverwrite:
        """The permissions of this role.

        Returns
        -------
        :class:`PermissionOverwrite`
        """
        permissions = self._permissions
        return PermissionOverwrite.from_pair(
            Permissions(permissions["a"]),
            Permissions(permissions["d"]),
        )

    @handle_update("name")
    def _handle_update_name(self, new: str) -> None:
        self.name = new

    @handle_update("colour")
    def _handle_update_colour(self, new: str) -> None:
        self.colour = new

    @handle_update("hoist")
    def _handle_update_hoist(self, new: bool) -> None:
        self.hoist = new

    @handle_update("rank")
    def _handle_update_rank(self, new: int) -> None:
        self.rank = new

    @handle_update("permissions")
    def _handle_update_permissions(self, new: types.Permissions) -> None:
        self._permissions = new
