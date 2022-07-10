# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from luster.state import State


class StateAware:
    _state: State

    @property
    def state(self) -> State:
        return self._state


class StateManagementMixin:
    _state: Optional[State]

    @property
    def state(self) -> Optional[State]:
        return self._state

    def set_state(self, state: State) -> None:
        self._state = state

    def remove_state(self) -> Optional[State]:
        state = self._state
        self._state = None
        return state
