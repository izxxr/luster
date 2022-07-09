# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Union

if TYPE_CHECKING:
    from aiohttp import ClientResponse


__all__ = (
    "LusterException",
    "WebsocketError",
    "HTTPException",
    "HTTPNotFound",
    "HTTPForbidden",
    "HTTPServerError",
)


class LusterException(Exception):
    """Base class for all kinds of exception provided by the library."""


class WebsocketError(LusterException):
    """An exception indicating an error event from websocket.

    This is raised by :meth:`Client.connect` or :meth:`WebsocketHandler.connect`
    indicating that websocket sent an error.

    Attributes
    ----------
    error: :class:`types.ErrorId`
        The label of error that happened.
    """
    def __init__(self, error: str) -> None:
        self.error = error
        super().__init__("Websocket responded with an error: %r" % error)

class HTTPException(LusterException):
    """An exception raised when an HTTP request fails.

    For more convenient error handling, This exception class
    is narrowed down to further subclasses according to a specific
    status code:

    - :class:`HTTPNotFound`
    - :class:`HTTPForbidden`
    - :class:`HTTPServerError`

    Attributes
    ----------
    response: :class:`aiohttp.ClientResponse`
        The response for the request that failed.
    data: Union[:class:`dict`, :class:`str`]
        The data for the failed request. In most cases, This
        is a dictionary including information about the error
        however in some rare cases, This can be a :class:`str`.
    """
    def __init__(self, response: ClientResponse, data: Union[Dict[str, Any], str]) -> None:
        self.response = response
        self.data = data

        super().__init__("This request failed with status code: {0}".format(response.status))


class HTTPNotFound(HTTPException):
    """A :class:`HTTPException` raised when a ``404`` status code occurs."""


class HTTPForbidden(HTTPException):
    """A :class:`HTTPException` raised when a ``401`` or ``403`` status code occurs."""


class HTTPServerError(HTTPException):
    """A :class:`HTTPException` raised when a ``500`` or higher status code occurs."""
