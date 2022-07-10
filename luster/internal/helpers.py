# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

from typing import Any, Union, TYPE_CHECKING

import io

if TYPE_CHECKING:
    from luster.http import HTTPHandler
    from luster.types.enums import FileTag


class _Missing:
    def __bool__(self) -> bool:
        return False

    def __repr__(self) -> str:
        return "..."

MISSING: Any = _Missing()


def handle_optional_field(data: Any, key: str, default: Any = None, fallback: Any = MISSING) -> Any:
    try:
        ret = data[key]
    except KeyError:
        return default
    else:
        if ret == fallback:
            return default
        return ret


def inner_upsert(data: Any, key: str, inner_key: str, value: Any) -> None:
    try:
        dct = data[key]
    except KeyError:
        data[key] = dct = {}

    dct[inner_key] = value


def upsert_remove_value(data: Any, value: Any, *, key: str = "remove"):
    try:
        fields = data[key]
    except KeyError:
        data[key] = fields = []

    fields.append(value)  # type: ignore

async def get_attachment_id(http: HTTPHandler, target: Union[str, io.BufferedReader], tag: FileTag) -> str:
    if isinstance(target, str):
        # Already target ID
        return target

    data = await http.upload_file(target, tag)
    return data["id"]  # type: ignore

