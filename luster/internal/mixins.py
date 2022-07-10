# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from luster.state import State


class StateAware:
    _state: State

    @property
    def state(self) -> State:
        return self._state
