from tree_frame.tree import TreeFrame


def test_from_records() -> None:
    x = TreeFrame.from_records(
        [{"x": 5, "y": 4, "children": [{"x": 3, "y": 6}]}], "children", engine="py"
    )
    print(x)
