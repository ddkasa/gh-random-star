from __future__ import annotations

from dataclasses import dataclass, field

__version__ = "1.2.0"


@dataclass(frozen=True)
class Version:
    major: int = field()
    minor: int = field()
    patch: int = field()

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Version):
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
            isinstance(other, Version)
            and self.major == other.major
            and self.minor == other.minor
            and self.patch == other.patch
        )

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    @classmethod
    def process_version(cls, version: str) -> Version:
        major, minor, patch = version.split(".")
        return Version(int(major), int(minor), int(patch))
