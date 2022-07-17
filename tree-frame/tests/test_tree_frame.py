from tree_frame.engine.axis import HierarchicalAxisDefinition, make_axes
from tree_frame.tree import TreeFrame


def test_from_records() -> None:
    x = TreeFrame.from_records(
        [{"x": 5, "y": 4, "children": [{"x": 3, "y": 6}]}],
        axes=make_axes(hierarchy1="children"),
        engine="py",
    )


def test_label_axis() -> None:
    x = TreeFrame.from_records(
        [
            {"x": "a", "y": 4, "children": [{"x": "a", "y": 6}]},
            {"x": "b", "y": 9},
        ],
        axes=make_axes(hierarchy1="children", axis2="x"),
        engine="py",
    )
