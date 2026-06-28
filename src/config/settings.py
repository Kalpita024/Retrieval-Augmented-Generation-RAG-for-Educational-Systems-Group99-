"""Centralized configuration for ingestion and text splitting.

Place configuration constants here so they can be adjusted for
different deployment environments (development, staging, production).

Values can be overridden with environment variables to allow runtime
configuration without editing source files.
"""
from __future__ import annotations

import os
from typing import Final

# Default chunk size for RecursiveCharacterTextSplitter. This is the
# target maximum number of characters per chunk (approximate).
CHUNK_SIZE: Final[int] = int(os.getenv("CHUNK_SIZE", "1000"))

# Number of characters that consecutive chunks will overlap by. Overlap
# helps preserve context at chunk boundaries for retrieval tasks.
CHUNK_OVERLAP: Final[int] = int(os.getenv("CHUNK_OVERLAP", "200"))

__all__ = ["CHUNK_SIZE", "CHUNK_OVERLAP"]
