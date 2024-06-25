from __future__ import annotations

from typing import NamedTuple

__version__ = "1.1.0"


class VersionNo(NamedTuple):
    major: int
    minor: int
    patch: int

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, VersionNo):
            return False
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

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, VersionNo)
            and self.major == other.major
            and self.minor == other.minor
            and self.patch == other.patch
        )

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    @staticmethod
    def process_version(version: str) -> VersionNo:
        major, minor, patch = version.split(".")
        return VersionNo(int(major), int(minor), int(patch))
