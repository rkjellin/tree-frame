import polars as pl
from tree_frame.system import AxisSystem


def test_add_tree_axis() -> None:
    df = pl.DataFrame(
        {
            "nid": [1, 2, 3, 4, 5, 6],
            "pnid": [None, 1, 1, None, 4, 5],
            "x": ["a", "b", "c", "d", "e", "f"],
        }
    )
    system = AxisSystem()
    system.add_tree_axis(node_id_column="nid", parent_node_id_column="pnid", df=df)
