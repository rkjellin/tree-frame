from __future__ import annotations

from dataclasses import dataclass
from typing import NewType, Union

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


def _parse_records(records: list[dict], childprop: str) -> TreeFrame:
    flat_recs = []
    for record in records:
        frec = record.copy()
        if childprop in frec:
            del frec[childprop]
        flat_recs.append(frec)
    df = pd.DataFrame.from_records(flat_recs)


@dataclass
class TreeFrame:
    axes: list[Axis]
    storage: pd.DataFrame

    @staticmethod
    def from_records(records: list[dict], childprop: str) -> TreeFrame:
        return _parse_records(records, childprop)
