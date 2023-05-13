# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

from typing import Any, Callable, Dict, Generic, TypeVar, TypedDict
import inspect

DataT = TypeVar("DataT", bound=TypedDict)
Handler = Callable[[Any, Any], Any]

def handle_update(field: str) -> Callable[[Handler], Handler]:
    def __wrap(func: Handler) -> Handler:
        func.__update_handler_field__ = field  # type: ignore
        return func

    return __wrap


class UpdateHandler(Generic[DataT]):
    __update_handlers__: Dict[str, Handler]

    def __init_subclass__(cls) -> None:
        cls.__update_handlers__ = handlers = {}

        for _, member in inspect.getmembers(cls):
            try:
                field = member.__update_handler_field__
            except AttributeError:
                continue
            else:
                handlers[field] = member

    def update(self, data: DataT) -> None:
        handlers = self.__update_handlers__

        for field, value in data.items():
            try:
                handler = handlers[field]
            except KeyError:
                pass
            else:
                handler(self, value)
