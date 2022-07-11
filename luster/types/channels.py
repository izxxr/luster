# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

from typing import List, TypedDict

__all__ = (
    "Category",
)


class Category(TypedDict):
    """Represents a category for other channels."""

    id: str
    """The ID of this category."""

    title: str
    """The title of this category."""

    channels: List[str]
    """The list of IDs for channels that are in this category."""
