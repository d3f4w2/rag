from rag.ingest.txt_parser import parse_stain_text


def test_parse_stain_text_extracts_two_fields():
    text = (
        "阴道镜所见(宫颈):\x7fA\n"
        "阴道镜所见(阴道):\x7fB\n"
    )
    out = parse_stain_text(text)
    assert out["cervix_findings"] == "A"
    assert out["vagina_findings"] == "B"
