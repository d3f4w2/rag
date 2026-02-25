from rag.index.build_index import rebuild_index
from rag.retrieval.retrieve import retrieve_channels


def test_retrieve_channels_returns_empty_when_no_query_match(tmp_path):
    index_dir = tmp_path / "rag-index"
    rebuild_index("example-data", str(index_dir))

    hits = retrieve_channels(
        question="definitely-not-in-the-documents",
        index_dir=str(index_dir),
        top_k=5,
    )

    assert hits["field_hits"] == []
    assert hits["text_hits"] == []
    assert hits["image_hits"] == []


def test_retrieve_channels_applies_label_filter(tmp_path):
    index_dir = tmp_path / "rag-index"
    rebuild_index("example-data", str(index_dir))

    hits = retrieve_channels(
        question="",
        index_dir=str(index_dir),
        top_k=20,
        label_filter="HSIL",
    )

    assert hits["field_hits"]
    assert hits["text_hits"]
    assert hits["image_hits"]
    assert all(str(hit["case_id"]).startswith("HSIL/") for hit in hits["field_hits"])
    assert all(str(hit["case_id"]).startswith("HSIL/") for hit in hits["text_hits"])
    assert all(str(hit["case_id"]).startswith("HSIL/") for hit in hits["image_hits"])
