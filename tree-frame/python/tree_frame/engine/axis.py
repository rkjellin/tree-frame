from dataclasses import dataclass
from typing import Optional, Union

from tree_frame.column import ColumnName


@dataclass
class HierarchicalAxisDefinition:
    childprop: ColumnName


AxisDefinition = Union[HierarchicalAxisDefinition, ColumnName]


def make_axes(
    *,
    axis1: Optional[str] = None,
    axis2: Optional[str] = None,
    axis3: Optional[str] = None,
    axis4: Optional[str] = None,
    hierarchy1: Optional[str] = None,
    hierarchy2: Optional[str] = None,
    hierarchy3: Optional[str] = None,
    hierarchy4: Optional[str] = None,
) -> list[AxisDefinition]:
    res: list[AxisDefinition] = []

    pairs = [
        (axis1, hierarchy1),
        (axis2, hierarchy2),
        (axis3, hierarchy3),
        (axis4, hierarchy4),
    ]
    for i, (axis, hierarchy) in enumerate(pairs):
        nbr = i + 1
        if axis and hierarchy:
            raise ValueError(f"Cannot provide both axis{nbr} and hierarchy{nbr}")
        elif axis and not hierarchy:
            res.append(ColumnName(axis))
        elif hierarchy and not axis:
            res.append(HierarchicalAxisDefinition(childprop=ColumnName(hierarchy)))
        else:
            break
    return res
