import re

_CERVIX_PREFIX = "阴道镜所见(宫颈)"
_VAGINA_PREFIX = "阴道镜所见(阴道)"


def parse_stain_text(text: str) -> dict[str, str]:
    cleaned = _strip_control_chars(text)
    out = {"cervix_findings": "", "vagina_findings": ""}

    for line in cleaned.splitlines():
        line = line.strip()
        if not line:
            continue

        cervix_match = re.match(rf"^{re.escape(_CERVIX_PREFIX)}\s*[:：]\s*(.*)$", line)
        if cervix_match:
            out["cervix_findings"] = cervix_match.group(1).strip()
            continue

        vagina_match = re.match(rf"^{re.escape(_VAGINA_PREFIX)}\s*[:：]\s*(.*)$", line)
        if vagina_match:
            out["vagina_findings"] = vagina_match.group(1).strip()

    return out


def _strip_control_chars(text: str) -> str:
    return "".join(ch for ch in text if ch == "\n" or ch == "\t" or ord(ch) >= 32 and ord(ch) != 127)
