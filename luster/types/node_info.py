# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

from typing import TypedDict


__all__ = (
    # Objects
    "NodeInfo",
    "NodeInfoFeatures",
    "NodeInfoCaptchaFeature",
    "NodeInfoAutumnFeature",
    "NodeInfoJanuaryFeature",
    "NodeInfoVosoFeature",

    # HTTP API
    "QueryNodeResponse",
)


class NodeInfo(TypedDict):
    """Represents the Revolt node info often returned by :meth:`.fetch_api_info` route."""

    revolt: str
    """Revolt API version."""

    features: NodeInfoFeatures
    """The features enabled on this Revolt node."""

    ws: str
    """The URL used for connecting to websocket."""

    app: str
    """The URL pointing to client serving this node."""

    vapid: str
    """The web push VAPID public key."""


class NodeInfoFeatures(TypedDict):
    """Represents the features of a Revold node retrieved from :class:`NodeInfo`"""

    captcha: NodeInfoCaptchaFeature
    """The human captcha (hCaptcha) configuration."""

    email: bool
    """Whether email verification is enabled."""

    invite_only: bool
    """Whether the server is invite only."""

    autumn: NodeInfoAutumnFeature
    """The file server configuration."""

    january: NodeInfoJanuaryFeature
    """The proxy service configuration."""

    voso: NodeInfoVosoFeature
    """The voice server configuration."""


class NodeInfoCaptchaFeature(TypedDict):
    """Represents the hCaptcha configuration found in :attr:`NodeInfoFeatures.captcha` field."""

    enabled: bool
    """Whether human captcha is enabled."""

    key: str
    """The client key used for solving the captcha."""


class _BaseService(TypedDict):
    enabled: bool
    """Whether the service is enabled."""

    url: str
    """The URL pointing to this service."""


class NodeInfoAutumnFeature(_BaseService):
    """Represents the configuration for Autumn file server found in :attr:`NodeInfoFeatures.autumn` field."""


class NodeInfoJanuaryFeature(_BaseService):
    """Represents the configuration for January proxy service configuration found in :attr:`NodeInfoFeatures.january` field."""


class NodeInfoVosoFeature(_BaseService):
    """Represents the configuration for Voso voice service configuration found in :attr:`NodeInfoFeatures.voso` field."""


class QueryNodeResponse(NodeInfo):
    """Represents the response of :meth:`HTTPHandler.query_node` or :meth:`HTTPHandler.fetch_node_info` route.

    This is equivalent to :class:`NodeInfo`.
    """
