# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

from typing import Union, Literal


__all__ = (
    "EventTypeSend",
    "EventTypeRecv",
    "EventType",
    "ErrorId",
    "WebsocketVersion",
    "WebsocketFormat",
    "FileType",
    "FileTag",
    "PresenceType",
    "RelationshipStatus",
    "UserRemoveField",
    "ChannelTypeServer",
    "ChannelTypePrivate",
    "ChannelType",
    "ChannelRemoveField",
    "ServerRemoveField",
    "RoleRemoveField",
)


# Websocket
EventTypeSend = Literal["Authenticate", "BeginTyping", "EndTyping", "Ping"]
EventTypeRecv = Literal["Error", "Authenticated", "Bulk", "Pong", "Ready",
                        "Message", "MessageUpdate", "MessageAppend", "MessageDelete",
                        "ChannelCreate", "ChannelUpdate", "ChannelDelete", "ChannelGroupJoin",
                        "ChannelGroupLeave", "ChannelStartTyping", "ChannelStopTyping", "ChannelAck",
                        "ServerCreate", "ServerUpdate", "ServerDelete", "ServerMemberJoin",
                        "ServerMemberUpdate", "ServerMemberLeave", "ServerRoleUpdate", "ServerRoleDelete",
                        "UserUpdate", "UserRelationship", "EmojiCreate", "EmojiDelete"]
EventType = Union[EventTypeSend, EventTypeRecv]
ErrorId = Literal["LabelMe", "InternalError", "InvalidSession", "OnboardingNotFinished", "AlreadyAuthenticated"]
WebsocketVersion = Literal[1]
WebsocketFormat = Literal["msgpack", "json"]

# File
FileType = Literal["File"]
FileTag = Literal["attachments", "avatars", "banners", "icons", "emojis", "backgrounds"]

# Users
PresenceType = Literal["Online", "Idle", "Busy", "Invisible"]
RelationshipStatus = Literal["None", "User", "Friend", "Outgoing", "Incoming", "Blocked", "BlockedOther"]
UserRemoveField = Literal["Avatar", "StatusText", "StatusPresence", "ProfileContent", "ProfileBackground"]

# Channels
ChannelTypeServer = Literal["TextChannel", "VoiceChannel"]
ChannelTypePrivate = Literal["SavedMessages", "DirectMessage", "Group"]
ChannelType = Union[ChannelTypeServer, ChannelTypePrivate]
ChannelRemoveField = Literal["Description", "Icon", "DefaultPermissions"]

# Servers
ServerRemoveField = Literal["Description", "Categories", "SystemMessages", "Icon", "Banner"]

# Roles
RoleRemoveField = Literal["Colour"]
