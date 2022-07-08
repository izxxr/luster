# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations


__all__ = (
    "Client",
)


class Client:
    """A client that interacts with Revolt API.

    This class provides a user friendly interface for interacting
    with Revolt Events and HTTP API. This class mainly focuses on
    automating user accounts or creating bots. If you intend to
    perform simple HTTP requests, Use :class:`HTTPHandler` instead.
    """