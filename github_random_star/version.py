from __future__ import annotations

from typing import NamedTuple

__version__ = "0.1.1"


class VersionNo(NamedTuple):
    major: int
    minor: int
    patch: int

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    def __gt__(self, other: VersionNo) -> bool:
        if self == other:
            return False
        if self.major > other.major:
            return True
        if self.major >= other.major and self.minor > other.minor:
            return True
        if (
            self.major >= other.major
            and self.minor >= other.minor
            and self.patch > other.patch
        ):
            return True
        return False

    def __eq__(self, other: VersionNo) -> bool:
        return (
            self.major == other.major
            and self.minor == other.minor
            and self.patch == other.patch
        )

    def __ne__(self, other: VersionNo) -> bool:
        return not self.__eq__(other)


def process_version(version: str) -> VersionNo:
    major, minor, patch = version.split(".")
    return VersionNo(int(major), int(minor), int(patch))
