from __future__ import annotations

import argparse
from pathlib import Path

from dev_agent_cli.models import CommandName, CommandRequest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dev-agent",
        description="A lightweight developer agent CLI.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("explain", "fix", "gen-api"):
        subparser = subparsers.add_parser(command, help=f"Run the {command} command.")
        subparser.add_argument("target", type=Path, help="Target file path.")
        subparser.add_argument("--goal", type=str, help="Optional task goal.")
        subparser.add_argument("--output", type=Path, help="Optional output file path.")
        subparser.add_argument(
            "--trace",
            action="store_true",
            help="Show orchestrator trace after execution.",
        )

    return parser


def parse_request(argv: list[str] | None = None) -> CommandRequest:
    parser = build_parser()
    args = parser.parse_args(argv)

    return CommandRequest(
        command=args.command,  # type: ignore[arg-type]
        target_path=args.target,
        goal=args.goal,
        output_path=args.output,
        trace=args.trace,
    )
