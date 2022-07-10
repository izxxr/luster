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
    "PresenceType",
    "RelationshipStatus",
    "UserRemoveField",
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

# Users
PresenceType = Literal["Online", "Idle", "Busy", "Invisible"]
RelationshipStatus = Literal["None", "User", "Friend", "Outgoing", "Incoming", "Blocked", "BlockedOther"]
UserRemoveField = Literal["Avatar", "StatusText", "StatusPresence", "ProfileContent", "ProfileBackground"]
