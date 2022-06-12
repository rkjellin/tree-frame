from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import NewType, Optional, Union

import pandas as pd

NodeId = NewType("NodeId", str)
ParentNodeId = NewType("ParentNodId", NodeId)


@dataclass
class TreeAxis:
    roots: list[NodeId]
    parent_links: dict[NodeId, ParentNodeId]


@dataclass
class GroupbyAxis:
    groupers: list[str]


Axis = Union[TreeAxis, GroupbyAxis]


def _gen_node_id() -> NodeId:
    return uuid.uuid4().hex


@dataclass
class _TreeBuilder:
    childprop: str
    roots: list[NodeId] = field(default_factory=list)
    parent_links: dict[NodeId, ParentNodeId] = field(default_factory=dict)
    rows: list[dict] = field(default_factory=list)

    def _parse_row(self, record: dict, parent_node_id: Optional[ParentNodeId]):
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
    ):
        for row in records:
            self._parse_row(row, parent_node_id)

    def _build_axis(self) -> TreeAxis:
        return TreeAxis(roots=self.roots, parent_links=self.parent_links)

    def _build_storage(self) -> pd.DataFrame:
        return pd.DataFrame.from_records(self.rows)

    @staticmethod
    def parse_records(records: list[dict], childprop: str) -> TreeFrame:
        builder = _TreeBuilder(childprop=childprop)
        builder._parse_level(records, parent_node_id=None)
        return TreeFrame(axes=[builder._build_axis()], storage=builder._build_storage())


@dataclass
class TreeFrame:
    axes: list[Axis]
    storage: pd.DataFrame

    @staticmethod
    def from_records(records: list[dict], childprop: str) -> TreeFrame:
        return _TreeBuilder.parse_records(records, childprop)
