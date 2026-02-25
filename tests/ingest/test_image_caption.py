from rag.ingest.image_caption import make_caption, stage_from_filename


def test_stage_mapping():
    assert stage_from_filename("1.jpg") == "baseline"
    assert stage_from_filename("3.jpg") == "post_acetic"
    assert stage_from_filename("5.jpg") == "post_iodine"


def test_make_caption_contains_stage():
    caption = make_caption("3.jpg", "HSIL", "Case A")
    assert "post_acetic" in caption
