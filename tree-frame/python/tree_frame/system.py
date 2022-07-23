from dataclasses import dataclass, field

import polars as pl

from tree_frame.axis import Axis, resolve_tree_axis
from tree_frame.column import Column


@dataclass
class AxisSystem:
    axes: list[Axis] = field(default_factory=list)

    def add_tree_axis(
        self,
        node_id_column: str | Column,
        parent_node_id_column: str | Column,
        df: pl.DataFrame,
    ) -> None:
        tree_axis = resolve_tree_axis(
            node_id_column=Column(node_id_column),
            parent_node_id_column=Column(parent_node_id_column),
            df=df,
        )
        self.axes.append(tree_axis)
