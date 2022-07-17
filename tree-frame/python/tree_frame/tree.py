from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Optional

from tree_frame.column import ColumnName
from tree_frame.engine.axis import AxisDefinition
from tree_frame.engine.base import BaseEngine
from tree_frame.engine.pyengine import PyEngine
from tree_frame.util import assert_never


@dataclass
class TreeFrame:
    engine: BaseEngine

    def with_axis(self, column: ColumnName) -> TreeFrame:
        pass

    @staticmethod
    def from_records(
        records: list[dict],
        axes: Optional[list[AxisDefinition]] = None,
        engine: Literal["py"] = "py",
    ) -> TreeFrame:
        if engine == "py":
            engine_impl = PyEngine.from_records(records, axes or [])
        else:
            assert_never(engine)
        return TreeFrame(engine=engine_impl)
