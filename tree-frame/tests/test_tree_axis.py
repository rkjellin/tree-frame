import polars as pl
from tree_frame.axis import resolve_tree_axis
from tree_frame.column import Column


def test_resolve_tree_axis() -> None:
    df = pl.DataFrame(
        {
            "nid": [1, 2, 3, 4, 5, 6],
            "pnid": [None, 1, 1, None, 4, 5],
            "x": ["a", "b", "c", "d", "e", "f"],
        }
    )
    tree_axis = resolve_tree_axis(
        node_id_column=Column("nid"), parent_node_id_column=Column("pnid"), df=df
    )
