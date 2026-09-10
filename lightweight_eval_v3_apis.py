#!/usr/bin/env python3
"""Compatibility wrapper for legacy v3 API evaluator entrypoint."""

from lightweight_eval import main

if __name__ == "__main__":
    raise SystemExit(main())
