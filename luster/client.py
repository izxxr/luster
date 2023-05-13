# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Callable,
    List,
    Optional,
    Type,
    Union,
)
from typing_extensions import Self
from luster.internal.events_handler import BE, EventsHandler, ListenersMixin, Listener
from luster.http import create_http_handler, HTTPHandler
from luster.internal.helpers import MISSING
from luster.protocols import BaseModel
from luster.websocket import WebsocketHandler
from luster.cache import Cache
from luster.state import State
from luster.users import User
from luster.file import PartialUploadedFile
from luster.channels import ChannelT, channel_factory
from luster.server import Server

import asyncio

if TYPE_CHECKING:
    from aiohttp import ClientSession
    from luster.channels import DirectMessage, Group
    from luster import types
    from io import BufferedReader

__all__ = (
    "Client",
)


class Client(ListenersMixin):
    """A client that interacts with Revolt API.

    This class provides a user friendly interface for interacting
    with Revolt Events and HTTP API. This class mainly focuses on
    automating user accounts or creating bots. If you intend to
    perform simple HTTP requests, Use :class:`HTTPHandler` instead.

    Parameters
    ----------
    token: :class:`str`
        The bot or session token.
    bot: :class:`bool`
        Whether the passed ``token`` is a bot token. Set this to
        ``False`` when a session token is passed (i.e for a user).
        Defaults to ``True``.
    session: Optional[:class:`aiohttp.ClientSession`]
        The client session used for making HTTP requests.

        If not provided, A session is created internally and would
        be closed automatically after usage. Note that when a session
        is provided by the user, It must be closed by the user. Library
        will not take it's ownership.
    http_handler_cls: Type[:class:`HTTPHandler`]
        The class type of :class:`HTTPHandler`. This can be used
        to set custom subclasses on :attr:`.http_handler`.
    websocket_handler_cls: Type[:class:`WebsocketHandler`]
        The class type of :class:`WebsocketHandler`. This can be used
        to set custom subclasses on :attr:`.websocket_handler`.
    cache_cls: Type[:class:`Cache`]
        The class type of :class:`Cache`. This can be used
        to set custom subclasses on :attr:`.cache`.

    Attributes
    ----------
    user: Optional[:class:`User`]
        The user for the connected client. This is only set after connection
        with Revolt API has been made.
    """

    def __init__(
        self,
        token: str,
        bot: bool = True,
        session: Optional[ClientSession] = None,
        http_handler_cls: Type[HTTPHandler] = HTTPHandler,
        websocket_handler_cls: Type[WebsocketHandler] = WebsocketHandler,
        cache_cls: Type[Cache] = Cache,
    ) -> None:

        self.__http_handler = create_http_handler(token=token, bot=bot, cls=http_handler_cls, session=session)
        self.__websocket_handler = websocket_handler_cls(http_handler=self.__http_handler)
        self.__cache = cache_cls()
        self.__state = State(
            http_handler=self.__http_handler,
            websocket_handler=self.__websocket_handler,
            cache=self.__cache,
        )
        self.__events_handler = EventsHandler(state=self.__state)
        self.__initialized: bool = False
        self.__state.set_client(self)
        self.__websocket_handler.set_events_handler(self.__events_handler)

    async def __aenter__(self) -> Self:
        await self._async_init()
        return self

    async def __aexit__(self, *_) -> None:
        await self._cleanup()

    def _get_events_handler(self) -> EventsHandler:
        return self.__events_handler

    @property
    def closed(self) -> bool:
        """Whether the client's websocket connection is currently closed.

        Returns
        -------
        :class:`bool`
        """
        return self.__websocket_handler.closed

    @property
    def http_handler(self) -> HTTPHandler:
        """The HTTP handler associated to this client.

        Returns
        -------
        :class:`HTTPHandler`
        """
        return self.__http_handler

    @property
    def websocket_handler(self) -> WebsocketHandler:
        """The websocket handler associated to this client.

        Returns
        -------
        :class:`WebsocketHandler`
        """
        return self.__websocket_handler

    @property
    def state(self) -> State:
        """The state associated to this client.

        Returns
        -------
        :class:`State`
        """
        return self.__state

    @property
    def cache(self) -> Cache:
        """The cache handler associated to this client.

        Returns
        -------
        :class:`Cache`
        """
        return self.__cache

    @property
    def latency(self) -> float:
        """The websocket latency.

        A shorthand for :attr:`WebsocketHandler.latency`.

        Returns
        -------
        :class:`float`
        """
        return self.__websocket_handler.latency

    @property
    def user(self) -> Optional[User]:
        """The user for the connected client.

        This is only set after connection with Revolt API has been made.

        Returns
        -------
        Optional[:class:`User`]
        """
        return self.__state.user

    def listen(self, event: str) -> Callable[[Listener[BE]], Listener[BE]]:
        """A decorator for registering an event listener.

        Parameters
        ----------
        event: :class:`str`
            The event to listen to.
        """
        def __wrap(func: Listener[BE]) -> Listener[BE]:
            self.add_listener(event, func)
            return func
        return __wrap

    async def _async_init(self) -> None:
        if self.__initialized:
            return

        await self.__http_handler._async_init()  # type: ignore[reportPrivateUsage]
        self.__initialized = True

    async def _cleanup(self) -> None:
        if not self.__initialized:
            return

        await self.__http_handler.close()
        await self.__websocket_handler.close()

        self.__state.user = None
        self.__initialized = False
        await self.close_hook()

    async def close_hook(self) -> None:
        """A hook that gets called when client has fully closed.

        :attr:`.closed` property will always return ``True``
        in this hook.

        You can use this hook to perform extra clean up on client
        closure such as closing database connections etc.
        """
        pass

    async def connect(self) -> None:
        """Connects the client to Revolt websocket."""
        if not self.__initialized:
            raise RuntimeError(
                "Client is not yet properly initialized. Make sure you are calling connect() "
                "within an async context manager"
            )

        await self.__websocket_handler.connect()

    def launch(self) -> None:
        """Launches the bot.

        This is a high level of :meth:`.connect` that handles asyncio
        event loop cleanup and provides a synchronous way of starting
        the client.

        Consider using :meth:`.connect` if you intend to have more
        control over the event loop.
        """
        async def runner():
            async with self:
                await self.connect()

        try:
            asyncio.run(runner())
        except KeyboardInterrupt:
            pass

    async def upload_file(self, file: BufferedReader, tag: types.FileTag) -> PartialUploadedFile:
        """Uploads a file to Autumn file server.

        Parameters
        ----------
        file: :class:`io.BufferedReader`
            The file buffer to upload.
        tag: :class:`types.FileTag`
            The tag or bucket to upload this file to.

        Returns
        -------
        :class:`PartialUploadedFile`
            The uploaded file.
        """
        data = await self.__http_handler.upload_file(file, tag)
        return PartialUploadedFile(data, tag, self.__state)

    async def fetch_self(self) -> User:
        """Fetches the user for current client.

        Returns
        -------
        :class:`User`
            The user for current client.

        Raises
        ------
        HTTPException
            Fetching the user failed.
        """
        data = await self.__http_handler.fetch_self()
        return User(data, self.__state)

    async def fetch_user(self, user_id: str) -> User:
        """Fetches the user by their ID.

        Parameters
        ----------
        user_id: :class:`str`
            The ID of user.

        Returns
        -------
        :class:`User`
            The requested user.

        Raises
        ------
        HTTPNotFound
            User does not exist.
        HTTPException
            The request failed.
        """
        data = await self.__http_handler.fetch_user(user_id)
        return User(data, self.__state)

    async def change_username(self, username: str, password: str) -> User:
        """Changes the username of current user.

        .. note::

            This can only be used by non-bot accounts.

        Parameters
        ----------
        username: :class:`str`
            The new username.
        password: :class:`str`
            The current account password.

        Returns
        -------
        :class:`User`
            The updated user.

        Raises
        ------
        HTTPException
            The request failed.
        HTTPForbidden
            The credentials are incorrect.
        """
        json: types.ChangeUsernameJSON = {
            "username": username,
            "password": password,
        }
        data = await self.__http_handler.change_username(json)
        return User(data, self.__state)

    # Channels

    async def fetch_channel(self, channel_id: str) -> ChannelT:
        """Fetches a channel.

        Parameters
        ----------
        channel_id: :class:`str`
            The ID of channel to fetch.

        Returns
        -------
        Union[:class:`ServerChannel`, :class:`PrivateChannel`]
            The fetched channel.

        Raises
        ------
        HTTPException
            The fetching failed.
        HTTPNotFound
            Invalid channel ID.
        """
        data = await self.__http_handler.fetch_channel(channel_id)
        cls = channel_factory(data["channel_type"])
        return cls(data, self.__state)  # type: ignore

    async def fetch_dms(self) -> List[Union[DirectMessage, Group]]:
        """Fetches the direct messages and groups that are currently opened.

        Returns
        -------
        List[Union[:class:`DirectMessage`, :class:`Group`]]
            The current direct message channels.

        Raises
        ------
        HTTPException
            The fetching failed.
        """
        data = await self.__http_handler.fetch_direct_message_channels()
        ret: List[Union[DirectMessage, Group]] = []

        for item in data:
            cls = channel_factory(item["channel_type"])
            ret.append(cls(item, self.__state))  # type: ignore

        return ret

    # Servers

    async def fetch_server(self, server_id: str) -> Server:
        """Fetches a server via it's ID.

        Parameters
        ----------
        channel_id: :class:`str`
            The ID of channel to fetch.

        Returns
        -------
        :class:`Server`
            The requested server.

        Raises
        ------
        HTTPNotFound
            The server does not exist.
        HTTPException
            Fetching of server failed.
        """
        data = await self.__http_handler.fetch_server(server_id)
        return Server(data, self.__state)

    async def create_server(
        self,
        *,
        name: str,
        description: str = MISSING,
        nsfw: bool = MISSING,
    ) -> Server:
        """Creates a server.

        Parameters
        ----------
        name: :class:`str`
            The name of server.
        description: :class:`str`
            The description of server.
        nsfw: :class:`bool`
            Whether this server is NSFW.

        Returns
        -------
        :class:`Server`
            The created server.

        Raises
        ------
        HTTPException
            Creation of server failed.
        """
        json: types.CreateServerJSON = {
            "name": name,
        }

        if description is not MISSING:
            json["description"] = description
        if nsfw is not MISSING:
            json["nsfw"] = nsfw

        data = await self.__http_handler.create_server(json=json)

        server = Server(data["server"], self.__state)

        for channel in data.get("channels", []):
            cls = channel_factory(channel["channel_type"])
            self.__cache.add_channel(cls(channel, self.__state))  # type: ignore

        return server

    async def create_group(
        self,
        name: str,
        recipients: List[BaseModel] = MISSING,
        description: str = MISSING,
        nsfw: bool = MISSING,
    ) -> Group:
        """Creates a new group.

        Parameters
        ----------
        name: :class:`str`
            The name of group.
        recipients: List[:class:`BaseModel`]
            The recipients to add to group.
        description: :class:`str`
            The description of group.
        nsfw: :class:`bool`
            Whether this group is NSFW.

        Returns
        -------
        :class:`Group`
            The created group.

        Raises
        ------
        HTTPException
            Creation of group failed.
        """
        if recipients is MISSING:
            recipients = []

        json: types.CreateGroupJSON = {
            "name": name,
            "users": [r.id for r in recipients],
        }

        if description is not MISSING:
            json["description"] = description

        if nsfw is not MISSING:
            json["nsfw"] = nsfw

        data = await self.__http_handler.create_group(json=json)
        return Group(data, self.__state)
