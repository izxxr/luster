# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations


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
