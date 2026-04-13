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

    def list_files(self, directory: Path, limit: int = 20) -> list[Path]:
        if not directory.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")

        if not directory.is_dir():
            raise NotADirectoryError(f"Expected a directory but got a file: {directory}")

        files = [path for path in directory.rglob("*") if path.is_file()]
        files.sort()
        return files[:limit]

    def read_directory_summary(self, directory: Path, limit: int = 20) -> str:
        files = self.list_files(directory, limit=limit)
        if not files:
            return "Directory summary: no files found."

        lines = [f"Directory summary for: {directory}"]
        for path in files:
            relative_path = path.relative_to(directory)
            lines.append(f"- {relative_path}")

        if len(files) == limit:
            lines.append(f"- ... truncated to first {limit} files")

        return "\n".join(lines)
