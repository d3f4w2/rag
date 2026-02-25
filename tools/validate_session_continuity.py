from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from rag.governance.continuity_rules import ValidationResult, validate_repository


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate session continuity artifacts.")
    parser.add_argument(
        "--root",
        type=Path,
        default=REPO_ROOT,
        help="Repository root to validate.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as errors.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON payload.",
    )
    return parser


def _render_text(result: ValidationResult, strict: bool) -> str:
    lines: list[str] = []
    lines.append(f"Status: {result.status}")
    lines.append(f"Strict Mode: {'on' if strict else 'off'}")
    lines.append(f"Next Task: {result.next_task_id or 'n/a'}")
    lines.append(f"Next First Command: {result.next_first_command or 'n/a'}")

    if result.violations:
        lines.append("")
        lines.append("Violations:")
        for item in result.violations:
            lines.append(f"- [{item.code}] {item.file}: {item.message}")
            lines.append(f"  Suggestion: {item.suggestion}")

    if result.warnings:
        lines.append("")
        lines.append("Warnings:")
        for item in result.warnings:
            lines.append(f"- [{item.code}] {item.file}: {item.message}")
            lines.append(f"  Suggestion: {item.suggestion}")

    if not result.violations and not result.warnings:
        lines.append("")
        lines.append("Continuity checks passed.")
    return "\n".join(lines)


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()
    result = validate_repository(args.root, strict=args.strict)

    if args.json:
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(_render_text(result, strict=args.strict))

    return 0 if result.status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
