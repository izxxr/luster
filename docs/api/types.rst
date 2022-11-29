.. currentmodule:: luster.types

.. _api-types:

API Types
=========

When it comes to working with low level API, dealing with raw JSON payloads and handling API
payloads manually can be an overwhelming task.

To ease you in this case, Library provides easy to use type defintions for Revolt API that only
allow you to properly typehint your application but also get cutting edge autocompletion in
your code editor.

Enumerations
------------

This section documents various enumerations from the Revolt API. All these are type aliases of
:class:`typing.Literal`.

.. data:: EventTypeSend

    The types of websocket events that are sent by the client.

.. data:: EventTypeRecv

    The types of websocket events that are received by the client.

.. data:: EventType

    The types of websocket events. This is equivalent to :class:`typing.Union`
    of :data:`EventTypeSend` and :data:`EventTypeRecv`.

.. data:: ErrorId

    The error labels often sent in :class:`ErrorEvent` websocket event.

.. data:: WebsocketVersion

    The versions for Revolt websocket protocol.

.. data:: WebsocketFormat

    The formats used for packets transport in Revolt websocket protocol.

.. data:: FileType

    The types of file.

.. data:: FileTag

    The tags or buckets that a file can be uploaded to.

.. data:: PresenceType

    The presence states of a user.

.. data:: RelationshipStatus

    The status of a relationship.

.. data:: UserRemoveField

    The fields that can be removed from a user object by editing it.

.. data:: ChannelTypeServer

    The channel types related to a server.

.. data:: ChannelTypePrivate

    The channel types for private channels.

.. data:: ChannelType

    All channel types.

.. data:: ChannelRemoveField

    The fields that can be removed from channel object by editing it.

.. data:: ServerRemoveField

    The fields that can be removed from server object by editing it.

API Models
----------

This section documents type definitions for various API models. All these type definitions
are subclasses of :class:`typing.TypedDict`.

NodeInfo
~~~~~~~~

.. autoclass:: NodeInfo()
    :members:

NodeInfoFeatures
~~~~~~~~~~~~~~~~

.. autoclass:: NodeInfoFeatures()
    :members:

NodeInfoCaptchaFeature
~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: NodeInfoCaptchaFeature()
    :members:

NodeInfoAutumnFeature
~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: NodeInfoAutumnFeature()
    :members:

NodeInfoJanuaryFeature
~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: NodeInfoJanuaryFeature()
    :members:

NodeInfoVosoFeature
~~~~~~~~~~~~~~~~~~~

.. autoclass:: NodeInfoVosoFeature()
    :members:

User
~~~~

.. autoclass:: User()
    :members:

Status
~~~~~~~~~~

.. autoclass:: Status()
    :members:

Profile
~~~~~~~~~~~

.. autoclass:: Profile()
    :members:


PartialUserBot
~~~~~~~~~~~~~~

.. autoclass:: PartialUserBot()
    :members:


Relationship
~~~~~~~~~~~~

.. autoclass:: Relationship()
    :members:

Server
~~~~~~

.. autoclass:: Server()
    :members:


SystemMessages
~~~~~~~~~~~~~~

.. autoclass:: SystemMessages()
    :members:

Category
~~~~~~~~

.. autoclass:: Category()
    :members:

Role
~~~~

.. autoclass:: Role()
    :members:


Permissions
~~~~~~~~~~~

.. autoclass:: Permissions()
    :members:

SavedMessages
~~~~~~~~~~~~~

.. autoclass:: SavedMessages()
    :members:

DirectMessage
~~~~~~~~~~~~~

.. autoclass:: DirectMessage()
    :members:


Group
~~~~~

.. autoclass:: Group()
    :members:

TextChannel
~~~~~~~~~~~

.. autoclass:: TextChannel()
    :members:

VoiceChannel
~~~~~~~~~~~~

.. autoclass:: VoiceChannel()
    :members:

ServerChannel
~~~~~~~~~~~~~

.. data:: ServerChannel

    A type alias for :class:`typing.Union` of various Server channels.

    This currently includes:

    - :class:`TextChannel`
    - :class:`VoiceChannel`

PrivateChannel
~~~~~~~~~~~~~~

.. data:: PrivateChannel

    A type alias for :class:`typing.Union` of various private channel types.

    This currently includes:

    - :class:`SavedMessages`
    - :class:`DirectMessages`
    - :class:`Group`

Channel
~~~~~~~

.. data:: Channel

    A type alias for :class:`typing.Union` of all channel types mentioned above.


HTTP Routes
-----------

This section documents type definitions for various HTTP routes. All these type definitions
are subclasses of :class:`typing.TypedDict`.

QueryNodeResponse
~~~~~~~~~~~~~~~~~

.. autoclass:: QueryNodeResponse()
    :members:

FetchSelfResponse
~~~~~~~~~~~~~~~~~

.. autoclass:: FetchSelfResponse()
    :members:

EditUserJSON
~~~~~~~~~~~~

.. autoclass:: EditUserJSON()
    :members:

EditUserResponse
~~~~~~~~~~~~~~~~

.. autoclass:: EditUserResponse()
    :members:

FetchUserResponse
~~~~~~~~~~~~~~~~~

.. autoclass:: FetchUserResponse()
    :members:

ChangeUsernameJSON
~~~~~~~~~~~~~~~~~~

.. autoclass:: ChangeUsernameJSON()
    :members:

ChangeUsernameResponse
~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: ChangeUsernameResponse()
    :members:

FetchProfileResponse
~~~~~~~~~~~~~~~~~~~~

.. autoclass:: FetchProfileResponse()
    :members:

UploadFileResponse
~~~~~~~~~~~~~~~~~~

.. autoclass:: UploadFileResponse()
    :members:

CreateServerJSON
~~~~~~~~~~~~~~~~

.. autoclass:: CreateServerJSON()
    :members:

CreateServerResponse
~~~~~~~~~~~~~~~~~~~~

.. autoclass:: CreateServerResponse()
    :members:

FetchServerResponse
~~~~~~~~~~~~~~~~~~~

.. autoclass:: FetchServerResponse()
    :members:

EditServerJSON
~~~~~~~~~~~~~~

.. autoclass:: EditServerJSON()
    :members:

EditServerResponse
~~~~~~~~~~~~~~~~~~

.. autoclass:: EditServerResponse()
    :members:

DeleteServerResponse
~~~~~~~~~~~~~~~~~~~~

.. data:: DeleteServerResponse

    A type alias representing response of :meth:`luster.HTTPHandler.delete_server` route.

MarkServerAsReadResponse
~~~~~~~~~~~~~~~~~~~~~~~~

.. data:: MarkServerAsReadResponse

    A type alias representing response of :meth:`luster.HTTPHandler.mark_server_as_read` route.

CreateServerChannelJSON
~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: CreateServerChannelJSON()
    :members:

CreateServerChannelResponse
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. data:: CreateServerChannelResponse

    A type alias representing response of :meth:`luster.HTTPHandler.create_server_channel` route.


FetchDirectMessageChannelsResponse
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. data:: FetchDirectMessageChannelsResponse

    A type alias representing the response of :meth:`luster.HTTPHandler.fetch_direct_message_channels`
    route.

    This is equivalent to :class:`typing.List` of :class:`DirectMessage` and :class:`Group`.

OpenDirectMessageResponse
~~~~~~~~~~~~~~~~~~~~~~~~~

.. data:: OpenDirectMessageResponse

    A type alias representing the response of :meth:`luster.HTTPHandler.open_direct_message`
    route.

    This is equivalent to :class:`typing.Union` of :class:`DirectMessage` and :class:`SavedMessages`.

FetchChannelResponse
~~~~~~~~~~~~~~~~~~~~

.. data:: FetchChannelResponse

    A type alias representing the response of :meth:`luster.HTTPHandler.fetch_channel`
    route.

    This is equivalent to :data:`Channel`.


DeleteChannelResponse
~~~~~~~~~~~~~~~~~~~~~

.. data:: DeleteChannelResponse

    A type alias representing the response of :meth:`luster.HTTPHandler.close_channel`
    route.

    This is equivalent to Literal[``None``].


EditChannelJSON
~~~~~~~~~~~~~~~

.. autoclass:: EditChannelJSON()
    :members:

EditChannelResponse
~~~~~~~~~~~~~~~~~~~

.. data:: EditChannelResponse

    A type alias representing the response of :meth:`luster.HTTPHandler.edit_channel`
    route.

    This is equivalent to :data:`Channel`.

CreateGroupJSON
~~~~~~~~~~~~~~~

.. autoclass:: CreateGroupJSON()
    :members:

CreateGroupResponse
~~~~~~~~~~~~~~~~~~~

.. autoclass:: CreateGroupResponse()
    :members:

FetchGroupMembersResponse
~~~~~~~~~~~~~~~~~~~~~~~~~

.. data:: FetchGroupMembersResponse

    A type alias representing the response of :meth:`luster.HTTPHandler.fetch_group_members`
    route.

AddGroupMemberResponse
~~~~~~~~~~~~~~~~~~~~~~

.. data:: AddGroupMemberResponse

    A type alias representing the response of :meth:`luster.HTTPHandler.add_group_member`
    route.

RemoveGroupMemberResponse
~~~~~~~~~~~~~~~~~~~~~~~~~

.. data:: RemoveGroupMemberResponse

    A type alias representing the response of :meth:`luster.HTTPHandler.remove_group_member`
    route.

Websocket Events
----------------

This section documents type definitions for various websocket events. All these type definitions
are subclasses of :class:`typing.TypedDict`.

AuthenticateEvent
~~~~~~~~~~~~~~~~~

.. autoclass:: AuthenticateEvent()
    :members:

PingEvent
~~~~~~~~~

.. autoclass:: PingEvent()
    :members:


BeginTypingEvent
~~~~~~~~~~~~~~~~

.. autoclass:: AuthenticateEvent()
    :members:

EndTypingEvent
~~~~~~~~~~~~~~

.. autoclass:: EndTypingEvent()
    :members:

ErrorEvent
~~~~~~~~~~

.. autoclass:: ErrorEvent()
    :members:

AuthenticatedEvent
~~~~~~~~~~~~~~~~~~

.. autoclass:: AuthenticatedEvent()
    :members:

PongEvent
~~~~~~~~~

.. autoclass:: PongEvent()
    :members:

BulkEvent
~~~~~~~~~

.. autoclass:: BulkEvent()
    :members:

ReadyEvent
~~~~~~~~~~

.. autoclass:: ReadyEvent()
    :members:

UserUpdateEvent
~~~~~~~~~~~~~~~

.. autoclass:: UserUpdateEvent()
    :members:

UserUpdateEventData
~~~~~~~~~~~~~~~~~~~

.. autoclass:: UserUpdateEventData()
    :members:

UserRelationshipEvent
~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: UserRelationshipEvent()
    :members:

ServerCreateEvent
~~~~~~~~~~~~~~~~~

.. autoclass:: ServerCreateEvent()
    :members:

ServerUpdateEvent
~~~~~~~~~~~~~~~~~

.. autoclass:: ServerUpdateEvent()
    :members:

ServerUpdateEventData
~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: ServerUpdateEventData()
    :members:

ServerDeleteEvent
~~~~~~~~~~~~~~~~~

.. autoclass:: ServerDeleteEvent()
    :members:

ChannelCreateEvent
~~~~~~~~~~~~~~~~~~

.. autoclass:: ChannelCreateEvent()
    :members:

ChannelUpdateEvent
~~~~~~~~~~~~~~~~~~

.. autoclass:: ChannelUpdateEvent()
    :members:

ChannelUpdateEventData
~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: ChannelUpdateEventData()
    :members:

ChannelDeleteEvent
~~~~~~~~~~~~~~~~~~

.. autoclass:: ChannelDeleteEvent()
    :members:

ChannelGroupJoinEvent
~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: ChannelGroupJoinEvent()
    :members:

ChannelGroupLeaveEvent
~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: ChannelGroupLeaveEvent()
    :members:

ServerRoleUpdateEvent
~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: ServerRoleUpdateEvent()
    :members:

ServerRoleUpdateEventData
~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: ServerRoleUpdateEventData()
    :members:

ServerRoleDeleteEvent
~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: ServerRoleDeleteEvent()
    :members:
