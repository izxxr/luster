# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

from typing import Any, ClassVar, Generator, Literal, Optional, Type, TypeVar, overload
from typing_extensions import Self

import aiohttp
import luster

__all__ = (
    "HTTPHandler",
    "create_http_handler",
)

HTTPHandlerT = TypeVar("HTTPHandlerT", bound="HTTPHandler")


@overload
def create_http_handler(
    *,
    cls: Literal[None] = None,
    token: str,
    session: Optional[aiohttp.ClientSession] = ...,
    bot: bool = ...,
) -> HTTPHandler:
    ...

@overload
def create_http_handler(
    *,
    cls: Optional[Type[HTTPHandlerT]] = ...,  # type: ignore
    token: str,
    session: Optional[aiohttp.ClientSession] = ...,
    bot: bool = ...,
) -> HTTPHandlerT:
    ...

def create_http_handler(
    *,
    cls: Optional[Type[HTTPHandlerT]] = None,
    token: str,
    session: Optional[aiohttp.ClientSession] = None,
    bot: bool = True,
) -> HTTPHandlerT:
    """A helper for creating a :class:`HTTPHandler`.

    This function can either be awaited or be used in an
    asynchronous context manager.

    Example::

        async with luster.create_http_handler(token="...") as http:
            await http.fetch_api_info()

        # is equivalent of

        http = await luster.create_http_handler()
        await http.fetch_api_info()

        # After usage, don't forget to close!
        await http.close()

    Parameters
    ----------
    cls: Optional[Type[:class:`HTTPHandler`]]
        The class type of :class:`HTTPHandler` to return. This can be used
        to return custom subclasses.
    token: :class:`str`
        The bot or session token used for authenticating requests.
        This cannot be modified once initialized.
    bot: :class:`bool`
        Whether the passed ``token`` is a bot token. Set this to
        ``False`` when a session token is passed. Defaults to ``True``.
    session: Optional[:class:`aiohttp.ClientSession`]
        The client session used for making HTTP requests.

        If not provided, A session is created internally and would
        be closed automatically after usage. Note that when a session
        is provided by the user, It must be closed by the user. Library
        will not take it's ownership.

    Returns
    -------
    :class:`HTTPHandler`
        The created HTTP handler.
    """
    if cls is None:
        cls = HTTPHandler  # type: ignore

    handler = cls(
        token=token,
        session=session,
        bot=bot,
    )  # type: ignore[reportOptionalCall]
    return handler


class HTTPHandler:
    """A class that handles HTTP requests to Revolt API.

    In most cases, you might not need to interact with this class.
    :class:`Client` provides a high level abstraction for this class.

    You should not initialize this class manually. Instead, use the
    :func:`create_http_handler` helper function. In a :class:`Client`,
    you can use :attr:`Client.http_handler` to get the instance of
    this class.

    Parameters
    ----------
    token: :class:`str`
        The bot or session token used for authenticating requests.
        This cannot be modified once initialized.
    bot: :class:`bool`
        Whether the passed ``token`` is a bot token. Set this to
        ``False`` when a session token is passed. Defaults to ``True``.
    session: Optional[:class:`aiohttp.ClientSession`]
        The client session used for making HTTP requests.

        If not provided, A session is created internally and would
        be closed automatically after usage. Note that when a session
        is provided by the user, It must be closed by the user. Library
        will not take it's ownership.
    """

    USER_AGENT: ClassVar[str] = f"Luster ({luster.__version__}, {luster.__url__})"
    """The user agent for attaching to requests.

    This by default includes library name but could be modified
    to be different.

    .. danger::

        Sending user agent that are invalid or are in invalid format
        can result in failing HTTP requests. **It is recommended to
        not change this attribute!**
    """

    BASE_URL: ClassVar[str] = "https://api.revolt.chat"
    """The base URL used for routes."""

    def __init__(
        self,
        *,
        token: str,
        session: Optional[aiohttp.ClientSession] = None,
        bot: bool = True,
    ) -> None:

        self.__token: str = token
        self.__session: Optional[aiohttp.ClientSession] = session
        self._session_owner: bool = session is None
        self._bot: bool = bot

    async def __aenter__(self) -> Self:
        await self._async_init()
        return self

    async def __aexit__(self, *_) -> None:
        await self.close()

    async def __await__(self) -> Generator[Any, None, Self]:
        return self._async_init().__await__()

    @property
    def token(self) -> Optional[str]:
        """The token used for authenticating requests.

        Returns
        -------
        Optional[:class:`str`]
        """
        return self.__token

    @property
    def bot(self) -> bool:
        """Indicates whether :attr:`.token` is a bot token.

        Returns
        -------
        :class:`bool`
        """
        return self._bot

    @property
    def session(self) -> Optional[aiohttp.ClientSession]:
        """The client session used for making HTTP requests.

        Returns
        -------
        Optional[:class:`aiohttp.ClientSession`]
        """
        return self.__session

    @property
    def session_owner(self) -> bool:
        """Indicates whether library owns the HTTP session.

        Returns
        -------
        :class:`bool`
        """
        return self._session_owner

    @property
    def closed(self) -> bool:
        """Indicates whether the underlying session is closed.

        Returns
        -------
        :class:`bool`
        """
        session = self.__session
        if session is None:
            return True

        return session.closed

    async def _async_init(self) -> Self:
        if self.closed:
            self.__session = aiohttp.ClientSession()
            self._session_owner = True

        return self

    async def close(self) -> bool:
        """Closes the underlying client session, if possible.

        Returns
        -------
        :class:`bool`
            Indicates whether the session was closed.
        """
        if self.__session and self._session_owner:
            await self.__session.close()
            return True

        return False
