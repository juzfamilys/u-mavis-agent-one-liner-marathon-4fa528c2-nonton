#!/usr/bin/env python3
"""One-Liner Marathon entry.

Writes exactly one original, funny one-liner about running a marathon
to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output), with no trailing
newline. Pure Python standard library only.

The line is validated before writing, then the file is read back and
the exact bytes on disk are re-validated.
"""

import os

LINE = (
    "I signed up for a marathon so I could finally finish something, "
    "but halfway through I realized the finish line was just another "
    "starting line with better snacks."
)


def validate_line(line: str) -> None:
    """Check every rule the competition requires.

    Runs before the write and again on the exact bytes read back from
    disk, so a bad line can never reach entry.txt.
    """
    assert isinstance(line, str) and line, "line must be a non-empty string"
    assert len(line) >= 20, "line must be at least 20 characters"
    assert "\n" not in line and "\r" not in line, "line must be a single line"
    assert "\t" not in line, "no tabs allowed"
    assert all(32 <= ord(ch) < 127 for ch in line), \
        "line must be printable ASCII only (no control characters)"
    assert line == line.strip(), "no leading or trailing whitespace"
    assert "  " not in line, "no double spaces"
    assert len(line) <= 200, "line must be at most 200 characters"
    assert line.endswith("."), "line must end with a period"


def main() -> None:
    validate_line(LINE)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")

    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)

    # Read back and re-validate the exact bytes on disk.
    with open(out_path, "rb") as f:
        raw = f.read()
    assert raw == LINE.encode("utf-8"), "bytes on disk differ from the line"
    assert not raw.endswith(b"\n"), "no trailing newline allowed"
    validate_line(raw.decode("utf-8"))

    print(f"Wrote {len(raw)} bytes to {out_path}")


if __name__ == "__main__":
    main()
