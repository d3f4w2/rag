from rag.index.build_index import rebuild_index


def test_rebuild_index_returns_stats(tmp_path):
    stats = rebuild_index("example-data", str(tmp_path / "rag-index"))
    assert stats["cases"] == 4
    assert stats["field_docs"] > 0
    assert stats["text_docs"] > 0
    assert stats["image_docs"] > 0
