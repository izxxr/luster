# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

from typing import Any


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
