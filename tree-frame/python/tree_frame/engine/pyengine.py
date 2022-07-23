from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import NewType, Optional, Union

import polars as pl
from tree_frame.column import ColumnName
from tree_frame.engine.axis import AxisDefinition, HierarchicalAxisDefinition
from tree_frame.engine.base import BaseEngine

NodeId = NewType("NodeId", str)
ParentNodeId = NewType("ParentNodeId", NodeId)


@dataclass
class TreeAxis:
    roots: list[NodeId]
    parent_links: dict[NodeId, ParentNodeId]


@dataclass
class LabelAxis:
    label_column: ColumnName
    labels: dict[str, int]


Axis = Union[TreeAxis, LabelAxis]


def _gen_node_id() -> NodeId:
    return NodeId(uuid.uuid4().hex)


def _find_hierarchical_axes(
    axes: list[AxisDefinition],
) -> list[HierarchicalAxisDefinition]:
    return [axis for axis in axes if isinstance(axis, HierarchicalAxisDefinition)]


def _find_label_axes(axes: list[AxisDefinition]) -> list[ColumnName]:
    return [axis for axis in axes if isinstance(axis, ColumnName)]


@dataclass
class _TreeBuilder:
    childprop: str
    label_axes: list[ColumnName]
    roots: list[NodeId] = field(default_factory=list)
    parent_links: dict[NodeId, ParentNodeId] = field(default_factory=dict)
    rows: list[dict] = field(default_factory=list)

    def _parse_row(self, record: dict, parent_node_id: Optional[ParentNodeId]) -> None:
        nid = _gen_node_id()
        if not parent_node_id:
            self.roots.append(nid)
        else:
            self.parent_links[nid] = parent_node_id
        record = record | {"node_id": nid}
        if childrows := record.get(self.childprop):
            del record[self.childprop]
            self._parse_level(childrows, parent_node_id=ParentNodeId(nid))
        self.rows.append(record)

    def _parse_level(
        self,
        records: list[dict],
        parent_node_id: Optional[ParentNodeId],
    ) -> None:
        for row in records:
            self._parse_row(row, parent_node_id)

    def _build_axes(self) -> list[Axis]:
        return [TreeAxis(roots=self.roots, parent_links=self.parent_links)]

    def _build_storage(self) -> pl.DataFrame:
        return pl.from_dicts(self.rows)

    @staticmethod
    def parse_records(
        records: list[dict],
        axes: list[AxisDefinition],
    ) -> PyEngine:
        hierarchical_axes = _find_hierarchical_axes(axes)
        if len(hierarchical_axes) != 1:
            # TODO: handle arbitrary axes
            raise ValueError(f"Currently only one hierarchy is supported")
        childprop = hierarchical_axes[0].childprop
        builder = _TreeBuilder(childprop=childprop, label_axes=_find_label_axes(axes))
        builder._parse_level(records, parent_node_id=None)
        return PyEngine(axes=builder._build_axes(), storage=builder._build_storage())


@dataclass
class PyEngine(BaseEngine):
    axes: list[Axis]
    storage: pl.DataFrame

    def clone(self) -> BaseEngine:
        raise NotImplementedError()

    @staticmethod
    def from_records(
        records: list[dict],
        axes: list[AxisDefinition],
    ) -> PyEngine:
        return _TreeBuilder.parse_records(records, axes)
