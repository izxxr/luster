# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    Coroutine,
    Dict,
    Generator,
    Literal,
    Optional,
    Type,
    TypeVar,
    overload,
)
from typing_extensions import Self
from luster.internal.mixins import StateManagementMixin
from luster.exceptions import (
    HTTPException,
    HTTPForbidden,
    HTTPNotFound,
    HTTPServerError,
)

import io
import aiohttp
import luster

if TYPE_CHECKING:
    from luster import types


__all__ = (
    "HTTPHandler",
    "create_http_handler",
)

HTTPHandlerT = TypeVar("HTTPHandlerT", bound="HTTPHandler")

STATUS_CODE_EXCEPTIONS: Dict[int, Type[HTTPException]] = {
    401: HTTPForbidden,
    403: HTTPForbidden,
    404: HTTPNotFound,
}


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


class HTTPHandler(StateManagementMixin):
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

    AUTUMN_BASE_URL: ClassVar[str] = "https://autumn.revolt.chat"
    """The base URL for Autumn file service."""

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

    def __await__(self) -> Generator[Any, None, Self]:
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

    def _get_response(self, response: aiohttp.ClientResponse) -> Coroutine[Any, Any, Any]:
        if response.content_type == "application/json":
            return response.json()
        return response.text()

    async def request(self, method: str, route: str, base_url: Optional[str] = None, **kwargs: Any) -> Any:
        """Requests a certain route and returns the response data.

        Parameters
        ----------
        method: :class:`str`
            The HTTP method to use.
        route: :class:`str`
            The route that will be appended to :attr:`.BASE_URL`.
        base_url: :class:`str`
            Override the base URL per request. Defaults to :attr:`.BASE_URL`.
        **kwargs:
            The keyword arguments that are passed to :meth:`aiohttp.ClientSession.request`.
            It is worth noting that provided headers will be updated to include the proper
            authentication headers and you don't have to add any authentication headers
            manually.

            Following headers will be overwritten:

            - ``X-Session-Token``
            - ``X-Bot-Token``
        """
        if self.closed:
            raise RuntimeError("HTTP handler is closed.")

        # Headers construction
        headers = kwargs.pop("headers", {})
        to_update = {
            "User-Agent": self.USER_AGENT,
            "X-Bot-Token" if self._bot else "X-Session-Token": self.__token,
        }
        headers.update(to_update)

        if base_url is None:
            base_url = self.BASE_URL

        url = f"{base_url}{route}"
        session = self.__session

        async with session.request(method, url, headers=headers, **kwargs) as response:  # type: ignore
            status = response.status
            if status == 204:
                return None

            data = await self._get_response(response)

            if status < 300 and status >= 200:
                return data

            if status in STATUS_CODE_EXCEPTIONS:
                exc = STATUS_CODE_EXCEPTIONS[status](response, data)
                raise exc

            if status >= 500:
                raise HTTPServerError(response, data)

            raise HTTPException(response, data)

    async def upload_file(self, file: io.BufferedReader, tag: types.FileTag) -> types.UploadFileResponse:
        """Uploads a file to Autumn file server.

        Parameters
        ----------
        file: :class:`io.BufferedReader`
            The file buffer to upload.
        tag: :class:`types.FileTag`
            The tag or bucket to upload this file to.

        Returns
        -------
        :class:`types.UploadFileResponse`
            The uploaded file.
        """
        if not file.readable():
            raise RuntimeError("Asset must be readable")

        data = aiohttp.FormData()
        data.add_field(
            name="file",
            value=file.read(),
            filename=file.name,
            content_type="application/octet-stream",
        )
        data = await self.request("POST", f"/{tag}", base_url=self.AUTUMN_BASE_URL, data=data)
        return data

    # Node Info

    async def query_node(self) -> types.NodeInfo:
        """Fetches the information about current Revolt instance.

        This route does not require authorization.

        Returns
        -------
        :class:`types.NodeInfo`
        """
        data = await self.request("GET", "/")
        return data

    fetch_node_info = query_node
    """An alias of :meth:`.query_node` method."""

    # Users

    async def fetch_self(self) -> types.FetchSelfResponse:
        """Fetches the user information for current authenticated user.

        Returns
        -------
        :class:`types.FetchSelfResponse`
        """
        data = await self.request("GET", "/users/@me")
        return data

    async def edit_user(self, json: types.EditUserJSON) -> types.EditUserResponse:
        """Edits the current user.

        Parameters
        ----------
        json: :class:`types.EditUserJSON`
            The JSON body for request.

        Returns
        -------
        :class:`types.EditUserResponse`
        """
        data = await self.request("PATCH", "/users/@me", json=json)
        return data

    async def fetch_user(self, user_id: str) -> types.FetchUserResponse:
        """Fetches the user of given ID.

        Parameters
        ----------
        user_id: :class:`str`
            The ID of user to fetch.

        Returns
        -------
        :class:`types.FetchUserResponse`
        """
        data = await self.request("GET", f"/users/{user_id}")
        return data

    async def change_username(self, json: types.ChangeUsernameJSON) -> types.ChangeUsernameResponse:
        """Changes the username of current user.

        Parameters
        ----------
        json: :class:`types.EditUserJSON`
            The JSON body for request.

        Returns
        -------
        :class:`types.ChangeUsernameResponse`
        """
        data = await self.request("PATCH", "/users/@me/username", json=json)
        return data

    async def fetch_profile(self, user_id: str) -> types.FetchProfileResponse:
        """Fetch a user's profile.

        Parameters
        ----------
        json: :class:`types.EditUserJSON`
            The JSON body for request.

        Returns
        -------
        :class:`types.FetchProfileResponse`
        """
        data = await self.request("GET", f"/users/{user_id}/profile")
        return data
