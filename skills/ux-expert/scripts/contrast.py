"""WCAG 2.2 contrast ratio of two colors (SC 1.4.3, 1.4.6, 1.4.11).

Standard library only.
Usage: python3 scripts/contrast.py <foreground> <background> [--size <css px>] [--bold]
Colors are #rgb or #rrggbb; composite alpha colors over their background first.
Large text is 24 CSS px, or 18.66 CSS px bold; without --size, text is judged as normal text.
"""

import argparse
import json
import re
import sys


def luminance(color: str) -> float:
    hex_part = color.strip().lstrip("#")
    if len(hex_part) == 3:
        hex_part = "".join(c * 2 for c in hex_part)
    if not re.fullmatch(r"[0-9a-fA-F]{6}", hex_part):
        raise ValueError(f'"{color}" is not a #rgb or #rrggbb color; composite alpha colors over their background first')
    channels = [int(hex_part[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    r, g, b = (c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(foreground: str, background: str, size_px: float | None = None, bold: bool = False) -> dict:
    lighter, darker = sorted((luminance(foreground), luminance(background)), reverse=True)
    ratio = round((lighter + 0.05) / (darker + 0.05), 2)
    large = None if size_px is None else size_px >= 24 or (bold and size_px >= 18.66)
    return {
        "ratio": ratio,
        "large_text": large,
        "passes": {"text_aa": ratio >= (3 if large else 4.5), "text_aaa": ratio >= (4.5 if large else 7), "non_text_aa": ratio >= 3},
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="WCAG 2.2 contrast ratio of two colors.")
    parser.add_argument("foreground")
    parser.add_argument("background")
    parser.add_argument("--size", type=float, help="rendered font size in CSS px")
    parser.add_argument("--bold", action="store_true")
    args = parser.parse_args(argv)
    try:
        print(json.dumps(contrast(args.foreground, args.background, args.size, args.bold)))
    except ValueError as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
