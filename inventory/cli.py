"""Command-line interface for offline inventory allocation."""

import json
import sys

from . import allocate


def main():
    try:
        document = json.load(sys.stdin)
        if not isinstance(document, dict) or set(document) != {"stock", "requests"}:
            raise ValueError("input must contain exactly stock and requests")
        result = allocate(document["stock"], document["requests"])
    except (ValueError, TypeError, json.JSONDecodeError) as error:
        print(f"invalid input: {error}", file=sys.stderr)
        return 2

    json.dump(result, sys.stdout, separators=(",", ":"))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
