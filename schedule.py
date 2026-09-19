import argparse
import os
import platform
import re
import shlex
import shutil
import subprocess
import sys
import time

"""
schedule.py

Sets up recurring runs of fix_indexes.py so users never edit a crontab by hand.
Cron is used under the hood because it works on both macOS and Linux.

Each scheduled notes directory gets one crontab line, tagged with a marker comment so
this script only ever touches its own entries.

Install tests the setup end to end through cron itself: a temporary crontab entry runs
quick checks and then the indexer, starting within the next minute. Running the test from the terminal
would miss cron-only problems, like missing Full Disk Access on macOS or git credentials.

Usage:
    python schedule.py install <notes_path> [--hours 24] [--skip-test]
    python schedule.py status
    python schedule.py uninstall <notes_path>
"""

_MARKER = "# johnny-indexer:"
_VALID_HOURS = (1, 2, 3, 4, 6, 8, 12, 24)
_ANCHOR_HOUR = 12
_TEST_MARKER = "# johnny-indexer-test:"
_REPO_PATH = os.path.dirname(os.path.abspath(__file__))
_TEST_RESULT_PATH = os.path.join(_REPO_PATH, "logs", "schedule_test_result.txt")
_TEST_LOG_PATH = os.path.join(_REPO_PATH, "logs", "schedule_test.log")
_TEST_LOCK_PATH = os.path.join(_REPO_PATH, "logs", "schedule_test.lock")
_TEST_START_TIMEOUT_SECONDS = 120
_PUSH_TIMEOUT_SECONDS = 60
_TEST_TIMEOUT_SECONDS = 300
_TEST_STARTED = "Test run started."


def _hours_to_cron(hours: int) -> str:
    """
    Converts an interval in hours to a cron schedule that always includes noon, when
    most machines are awake (cron skips runs during sleep).
    Eg: 6 hours -> runs at 00:00, 06:00, 12:00 and 18:00.
    """
    if hours not in _VALID_HOURS:
        raise ValueError(
            f"--hours must be one of {', '.join(str(h) for h in _VALID_HOURS)}."
        )
    run_hours = range(_ANCHOR_HOUR % hours, 24, hours)
    hour_field = "*" if hours == 1 else ",".join(str(h) for h in run_hours)
    return f"0 {hour_field} * * *"


def _cron_to_hours(line: str) -> int:
    """Reverses _hours_to_cron using the hour field of a crontab line."""
    hour_field = line.split()[1]
    return 1 if hour_field == "*" else 24 // len(hour_field.split(","))


def _read_crontab() -> list[str]:
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    if result.returncode != 0:  # No crontab exists yet
        return []
    return result.stdout.splitlines()


def _write_crontab(lines: list[str]) -> None:
    content = "\n".join(lines) + "\n" if lines else ""
    subprocess.run(["crontab", "-"], input=content, text=True, check=True)


def _without_entry(lines: list[str], marker: str) -> list[str]:
    return [line for line in lines if not line.endswith(marker)]


def _command(script_args: list[str], log_path: str) -> str:
    """Builds a shell command that runs a script in this repo with the current Python."""
    return " ".join(
        [
            "cd",
            shlex.quote(_REPO_PATH),
            "&&",
            shlex.quote(sys.executable),
            *(shlex.quote(arg) for arg in script_args),
            ">>",
            shlex.quote(log_path),
            "2>&1",
        ]
    )


def _log_path(notes_path: str) -> str:
    log_name = re.sub(r"[^A-Za-z0-9_.-]", "_", os.path.basename(notes_path))
    return f"logs/fix_indexes_{log_name}.log"


def _build_line(notes_path: str, hours: int) -> str:
    command = _command(["fix_indexes.py", notes_path], _log_path(notes_path))
    return f"{_hours_to_cron(hours)} {command} {_MARKER} {notes_path}"


def _build_test_line(notes_path: str) -> str:
    """
    A crontab line that runs the setup check every minute. Only the first run does the
    check (see test()), and install removes the line once it starts. Running every
    minute, rather than once, covers cron missing a minute while it starts up, which
    macOS does when the crontab was empty.
    """
    command = _command(
        ["schedule.py", "test", notes_path, _TEST_RESULT_PATH], _TEST_LOG_PATH
    )
    return f"* * * * * {command} {_TEST_MARKER} {notes_path}"


def test(notes_path: str, result_path: str) -> None:
    """
    Runs from cron during install. Checks what a scheduled run needs, then runs the
    indexer, and writes the outcome to result_path: "ok", or the reason it failed.
    """
    try:
        os.close(os.open(_TEST_LOCK_PATH, os.O_CREAT | os.O_EXCL))
    except FileExistsError:
        return  # A run from an earlier minute already started the test

    print(_TEST_STARTED, flush=True)
    try:
        _check_setup(notes_path)
        _run_indexer(notes_path)
        result = "ok"
    except Exception as e:
        result = str(e)
    with open(result_path, "w", encoding="utf-8") as f:
        f.write(result)


def _check_setup(notes_path: str) -> None:
    try:
        os.listdir(notes_path)
    except PermissionError as e:
        if platform.system() == "Darwin":
            raise PermissionError(
                "cron can't read your notes. Give `/usr/sbin/cron` Full Disk Access "
                "in System Settings > Privacy & Security, then re-run install."
            ) from e
        raise

    from utils.config import ConfigHelper as ch  # Checks dependencies load under cron

    if ch.load_from_config("auto_push") is True:
        result = subprocess.run(
            ["git", "-C", notes_path, "push", "--dry-run", "--quiet"],
            capture_output=True,
            text=True,
            timeout=_PUSH_TIMEOUT_SECONDS,
            env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"auto_push is on, but git can't push from cron: {result.stderr.strip()}"
            )


def _run_indexer(notes_path: str) -> None:
    """Runs the indexer like a scheduled run would, failing on errors or warnings."""
    result = subprocess.run(
        [sys.executable, "fix_indexes.py", notes_path],
        cwd=_REPO_PATH,
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
    )
    output = (result.stdout + result.stderr).strip()
    with open(
        os.path.join(_REPO_PATH, _log_path(notes_path)), "a", encoding="utf-8"
    ) as f:
        f.write(output + "\n")

    warnings = [line for line in output.splitlines() if line.startswith("⚠️")]
    if result.returncode != 0:
        raise RuntimeError(f"The indexer failed:\n{output}")
    if warnings:
        raise RuntimeError("The indexer ran with warnings:\n" + "\n".join(warnings))


def _test_through_cron(notes_path: str) -> str:
    """
    Adds a temporary crontab entry that runs the setup check, waits for its result and
    removes the entry. Returns "ok" or the reason it failed.
    """
    for path in (_TEST_RESULT_PATH, _TEST_LOG_PATH, _TEST_LOCK_PATH):
        if os.path.exists(path):
            os.remove(path)

    test_marker = f"{_TEST_MARKER} {notes_path}"
    lines = _without_entry(_read_crontab(), test_marker)
    _write_crontab([*lines, _build_test_line(notes_path)])
    print(
        "Testing the setup through cron. This runs the indexer once and can take a "
        "few minutes..."
    )

    try:
        if not _wait_for(_TEST_LOCK_PATH, _TEST_START_TIMEOUT_SECONDS):
            return (
                "The test run through cron never started. Check that cron is running"
                + (
                    " and has Full Disk Access (System Settings > Privacy & Security)."
                    if platform.system() == "Darwin"
                    else "."
                )
            )
        _write_crontab(_without_entry(_read_crontab(), test_marker))

        if not _wait_for(_TEST_RESULT_PATH, _TEST_TIMEOUT_SECONDS):
            return _test_failure_output() or (
                f"The test run through cron didn't finish within "
                f"{_TEST_TIMEOUT_SECONDS // 60} minutes."
            )
        with open(_TEST_RESULT_PATH, encoding="utf-8") as f:
            return f.read().strip()
    finally:
        _write_crontab(_without_entry(_read_crontab(), test_marker))
        for path in (_TEST_LOCK_PATH, _TEST_RESULT_PATH):
            if os.path.exists(path):
                os.remove(path)


def _wait_for(path: str, timeout_seconds: int) -> bool:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        if os.path.exists(path):
            return True
        time.sleep(2)
    return False


def _test_failure_output() -> str:
    """Output of a test run that crashed before writing its result, if any."""
    if not os.path.exists(_TEST_LOG_PATH):
        return ""
    with open(_TEST_LOG_PATH, encoding="utf-8") as f:
        output = f.read().replace(_TEST_STARTED, "").strip()
    return f"The test run through cron failed:\n{output}" if output else ""


def install(notes_path: str, hours: int, skip_test: bool) -> None:
    if not os.path.isdir(notes_path):
        sys.exit(f"'{notes_path}' is not a directory.")
    if "%" in notes_path or "%" in _REPO_PATH or "\n" in notes_path:
        sys.exit("Paths containing '%' or newlines can't be scheduled with cron.")

    os.makedirs(os.path.join(_REPO_PATH, "logs"), exist_ok=True)
    marker = f"{_MARKER} {notes_path}"
    line = _build_line(notes_path, hours)
    _write_crontab([*_without_entry(_read_crontab(), marker), line])

    if skip_test:
        print(f"✅ Scheduled every {hours}h: {notes_path}")
        print(
            f"⚠️  Setup not tested. Check {_log_path(notes_path)} after the first run."
        )
        return

    result = _test_through_cron(notes_path)
    if result != "ok":
        _write_crontab(_without_entry(_read_crontab(), marker))
        sys.exit(f"❌ Not scheduled. {result}")

    print(f"✅ Scheduled every {hours}h: {notes_path}")
    print("Test run of the indexer through cron succeeded.")
    print(f"Logs: {os.path.join(_REPO_PATH, 'logs')}")


def status() -> None:
    entries = [line for line in _read_crontab() if _MARKER in line]
    if not entries:
        print("No scheduled runs.")
        return
    for line in entries:
        notes_path = line.split(_MARKER, 1)[1].strip()
        print(f"every {_cron_to_hours(line)}h  {notes_path}")


def uninstall(notes_path: str) -> None:
    lines = _read_crontab()
    remaining = _without_entry(lines, f"{_MARKER} {notes_path}")
    if len(remaining) == len(lines):
        sys.exit(f"No scheduled run found for '{notes_path}'.")
    _write_crontab(remaining)
    print(f"Removed scheduled run: {notes_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Schedule recurring index fixes.")
    commands = parser.add_subparsers(dest="command", required=True)

    install_parser = commands.add_parser("install", help="Schedule recurring runs")
    install_parser.add_argument("notes_path")
    install_parser.add_argument(
        "--hours",
        type=int,
        default=24,
        help=f"Hours between runs, one of {', '.join(str(h) for h in _VALID_HOURS)} (default: 24)",
    )
    install_parser.add_argument(
        "--skip-test",
        action="store_true",
        help="Install without the test run through cron",
    )

    commands.add_parser("status", help="List scheduled runs")

    uninstall_parser = commands.add_parser("uninstall", help="Remove a scheduled run")
    uninstall_parser.add_argument("notes_path")

    # Run by cron during install. Not meant to be called directly.
    test_parser = commands.add_parser("test")
    test_parser.add_argument("notes_path")
    test_parser.add_argument("result_path")

    args = parser.parse_args()
    if args.command == "test":
        test(args.notes_path, args.result_path)
        return
    if shutil.which("crontab") is None:
        sys.exit("`crontab` was not found. Scheduling requires cron.")

    if args.command == "install":
        try:
            install(os.path.abspath(args.notes_path), args.hours, args.skip_test)
        except ValueError as e:
            sys.exit(str(e))
    elif args.command == "status":
        status()
    else:
        uninstall(os.path.abspath(args.notes_path))


if __name__ == "__main__":
    main()
