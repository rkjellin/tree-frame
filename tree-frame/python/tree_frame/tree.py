from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from tree_frame.engine.base import BaseEngine
from tree_frame.engine.pyengine import PyEngine
from tree_frame.util import assert_never


@dataclass
class TreeFrame:
    engine: BaseEngine

    @staticmethod
    def from_records(
        records: list[dict], childprop: str, engine: Literal["py"]
    ) -> TreeFrame:
        if engine == "py":
            engine_impl = PyEngine.from_records(records, childprop)
        else:
            assert_never(engine)
        return TreeFrame(engine=engine_impl)
