# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Generic,
    Optional,
    Type,
)
from typing_extensions import Self
from luster.http import create_http_handler, HTTPHandlerT

if TYPE_CHECKING:
    from aiohttp import ClientSession


__all__ = (
    "Client",
)


class Client(Generic[HTTPHandlerT]):
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
    http_handler_cls: Optional[Type[:class:`HTTPHandler`]]
        The class type of :class:`HTTPHandler`. This can be used
        to set custom subclasses on :attr:`.http_handler`.
    """

    def __init__(
        self,
        token: str,
        bot: bool = True,
        session: Optional[ClientSession] = None,
        http_handler_cls: Optional[Type[HTTPHandlerT]] = None,
    ) -> None:

        self.__http_handler = create_http_handler(token=token, bot=bot, cls=http_handler_cls,
                                                  session=session)
        self.__initialized: bool = False

    async def __aenter__(self) -> Self:
        await self._async_init()
        return self

    async def __aexit__(self, *_) -> None:
        await self._cleanup()

    @property
    def http_handler(self) -> HTTPHandlerT:
        """The HTTP handler associated to this client.

        Returns
        -------
        :class:`HTTPHandler`
        """
        return self.__http_handler

    async def _async_init(self) -> None:
        if self.__initialized:
            return

        await self.__http_handler._async_init()  # type: ignore[reportPrivateUsage]
        self.__initialized = True

    async def _cleanup(self) -> None:
        if not self.__initialized:
            return

        await self.__http_handler.close()
        self.__initialized = False
