from __future__ import annotations

from pathlib import Path


class FileTool:
    """Bounded file access tool used by the orchestrator."""

    def read_text(self, path: Path) -> str:
        if not path.exists():
            raise FileNotFoundError(f"Target file not found: {path}")

        if path.is_dir():
            raise IsADirectoryError(f"Expected a file but got a directory: {path}")

        return path.read_text(encoding="utf-8")

    def write_text(self, path: Path, content: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
