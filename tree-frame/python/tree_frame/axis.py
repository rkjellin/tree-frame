from collections import defaultdict
from dataclasses import dataclass
from typing import DefaultDict, NewType

import polars as pl
from tree_frame.column import Column

NodeId = NewType("NodeId", str)
ParentNodeId = NewType("ParentNodeId", NodeId)


@dataclass
class TreeAxis:
    node_id_column: Column
    parent_node_id_column: Column
    roots: list[NodeId]
    uplinks: dict[NodeId, ParentNodeId]
    downlinks: dict[ParentNodeId, list[NodeId]]


def resolve_tree_axis(
    node_id_column: Column, parent_node_id_column: Column, df: pl.DataFrame
) -> TreeAxis:
    roots: list[NodeId] = []
    uplinks: dict[NodeId, ParentNodeId] = {}
    downlinks: DefaultDict[ParentNodeId, list[NodeId]] = defaultdict(list)
    cols = df.select([pl.col(node_id_column), pl.col(parent_node_id_column)])
    for nid, pnid in cols.rows():
        if pnid is None:
            roots.append(nid)
        else:
            uplinks[nid] = pnid
            downlinks[pnid].append(nid)
    return TreeAxis(
        node_id_column=node_id_column,
        parent_node_id_column=parent_node_id_column,
        roots=roots,
        uplinks=uplinks,
        downlinks=downlinks,
    )


Axis = TreeAxis
