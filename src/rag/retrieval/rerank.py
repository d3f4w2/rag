from __future__ import annotations


def rerank_cases(
    field_hits: list[dict[str, float]],
    text_hits: list[dict[str, float]],
    image_hits: list[dict[str, float]],
) -> list[dict[str, float | str]]:
    by_channel = {
        "field": _best_scores(field_hits),
        "text": _best_scores(text_hits),
        "image": _best_scores(image_hits),
    }
    case_ids = set(by_channel["field"]) | set(by_channel["text"]) | set(by_channel["image"])

    merged: list[dict[str, float | str]] = []
    for case_id in case_ids:
        field_score = by_channel["field"].get(case_id, 0.0)
        text_score = by_channel["text"].get(case_id, 0.0)
        image_score = by_channel["image"].get(case_id, 0.0)
        score = 0.45 * field_score + 0.40 * text_score + 0.15 * image_score
        merged.append(
            {
                "case_id": case_id,
                "score": score,
                "field_score": field_score,
                "text_score": text_score,
                "image_score": image_score,
            }
        )

    merged.sort(key=lambda row: (-float(row["score"]), str(row["case_id"])))
    return merged


def _best_scores(hits: list[dict[str, float]]) -> dict[str, float]:
    by_case: dict[str, float] = {}
    for hit in hits:
        case_id = str(hit["case_id"])
        score = float(hit["score"])
        by_case[case_id] = max(score, by_case.get(case_id, 0.0))
    return by_case
