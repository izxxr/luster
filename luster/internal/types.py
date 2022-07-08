# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

from typing import Any, Protocol


class SupportsAsyncInit(Protocol):
    async def _async_init(self) -> Any:
        ...


class SupportsAsyncSetup(SupportsAsyncInit, Protocol):
    async def _cleanup(self) -> Any:
        ...
