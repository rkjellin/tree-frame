from __future__ import annotations

import abc


class BaseEngine(abc.ABC):
    @abc.abstractmethod
    def clone(self) -> BaseEngine:
        ...
