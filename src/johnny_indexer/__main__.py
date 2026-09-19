import argparse
import logging
import os
import sys

from johnny_indexer import log, schedule
from johnny_indexer.create_jdex import create_jdex
from johnny_indexer.file import File
from johnny_indexer.fix_indexes import fix_indexes

logger = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="johnny-indexer",
        description="Index notes using the Johnny Decimal system.",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    fix_parser = commands.add_parser("fix", help="Fix the indexes of your notes")
    fix_parser.add_argument("notes_path")

    jdex_parser = commands.add_parser(
        "jdex", help="Generate JDex files without fixing indexes"
    )
    jdex_parser.add_argument("notes_path")

    schedule.add_arguments(
        commands.add_parser("schedule", help="Schedule recurring index fixes")
    )

    args = parser.parse_args()
    if args.command in ("fix", "jdex"):
        args.notes_path = os.path.abspath(args.notes_path)
        log.setup_logging(args.notes_path)
    else:
        log.setup_logging(None)  # Schedule commands only print, so have no log file

    try:
        if args.command == "fix":
            fix_indexes(args.notes_path)
        elif args.command == "jdex":
            create_jdex(File.from_abs_path(args.notes_path, -1))
        else:
            schedule.run(args)
    except Exception:
        logger.exception("Run failed")
        sys.exit(1)

    if log.warning_count() > 0:
        sys.exit(log.EXIT_WARNINGS)


if __name__ == "__main__":
    main()
