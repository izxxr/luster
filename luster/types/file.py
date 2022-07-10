# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

from typing import TYPE_CHECKING, Optional, TypedDict
from typing_extensions import NotRequired

if TYPE_CHECKING:
    from luster.types.enums import FileType, FileTag


__all__ = (
    "FileMetadata",
    "File",
    "UploadFileResponse",
)


class FileMetadata(TypedDict):
    """Represents meta data for a :class:`File`."""

    type: FileType
    """The type of file."""


class File(TypedDict):
    """Represents a file asset from Revolt file server."""

    _id: str
    """The unique ID of file."""

    tag: FileTag
    """The tag or bucket that the file was uploaded to."""

    filename: str
    """The name of file."""

    metadata: FileMetadata
    """The extra metadata associated to this file."""

    content_type: str
    """The content type of this file."""

    size: int
    """The size of file in bytes."""

    deleted: NotRequired[Optional[bool]]
    """Whether this file was deleted."""

    reported: NotRequired[Optional[bool]]
    """Whether this file was reported."""

    message_id: NotRequired[Optional[str]]
    """The ID of message that the file was uploaded to."""

    user_id: NotRequired[Optional[str]]
    """The ID of user that uploaded this file."""

    server_id: NotRequired[Optional[str]]
    """The ID of server that the file was uploaded to."""

    object_id: NotRequired[Optional[str]]
    """The ID of object associated to this file such as a user."""


class UploadFileResponse(TypedDict):
    """Represents the response of :meth:`HTTPHandler.upload_file`."""
    
    id: str
    """The ID of uploaded file."""
