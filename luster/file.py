# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

from typing import TYPE_CHECKING, Optional
from luster.internal.helpers import handle_optional_field
from luster.internal.mixins import StateAware

if TYPE_CHECKING:
    from luster.state import State
    from luster.types.file import (
        File as FileData,
        FileType as FileTypeRaw,
    )

__all__ = (
    "File",
)


class File(StateAware):
    """Represents a file from Revolt CDN.

    Attributes
    ----------
    id: :class:`str`
        The unique ID of this file.
    tag: :class:`str`
        The tag or bucket that this file has been uploaded to.
    filename: :class:`str`
        The original filename of file.
    content_type: :class:`str`
        The `content type <https://en.wikipedia.org/wiki/Media_type>`_ of this file.
    size: :class:`int`
        The size of this file, in bytes.
    type: :class:`types.FileType`
        The type of this file.

        .. seealso:: :class:`FileType` enum
    deleted: :class:`bool`
        Whether this file has been deleted.
    reported: :class:`bool`
        Whether this file has been reported.
    message_id: Optional[:class:`str`]
        If file was uploaded as an attachment, the ID of message that
        attached this file.
    user_id: Optional[:class:`str`]
        If file was uploaded by a user, the ID of user that
        uploaded this file.
    server_id: Optional[:class:`str`]
        If file was uploaded inside or by a server, the ID of server that
        uploaded this file.
    object_id: Optional[:class:`str`]
        The ID of object relevant to this file.
    """

    if TYPE_CHECKING:
        id: str
        tag: str
        filename: str
        content_type: str
        size: int
        type: FileTypeRaw
        deleted: bool
        reported: bool
        message_id: Optional[str]
        user_id: Optional[str]
        server_id: Optional[str]
        object_id: Optional[str]

    __slots__ = (
        "_state",
        "id",
        "tag",
        "filename",
        "content_type",
        "size",
        "deleted",
        "reported",
        "message_id",
        "user_id",
        "server_id",
        "object_id",
    )

    def __init__(self, data: FileData, state: State) -> None:
        self._state = state
        self._update_from_data(data)

    def _update_from_data(self, data: FileData):
        self.id = data["_id"]
        self.tag = data["tag"]
        self.filename = data["filename"]
        self.content_type = data["content_type"]
        self.size = data["size"]
        self.deleted = handle_optional_field(data, "deleted", False, None)
        self.reported = handle_optional_field(data, "reported", False, None)
        self.message_id = data.get("message_id")
        self.user_id = data.get("user_id")
        self.server_id = data.get("server_id")
        self.object_id = data.get("object_id")

        self._unroll_metadata(data)

    def _unroll_metadata(self, data: FileData):
        metadata = data["metadata"]
        self.type = metadata["type"]

    def is_attachment(self) -> bool:
        """Indicates whether this file is uploaded as a message attachment.

        Parameters
        ----------
        :class:`bool`
        """
        return self.message_id is not None
