#!/usr/bin/env python3

import sys
import os
import subprocess
from datetime import datetime

'''
1. Open your crontab file:
crontab -e

2. Add the following line to run the script every 5 minutes:
*/5 * * * * /usr/bin/python3 /path/to/commit_daily.py /path/to/repo >> /path/to/commit_daily.log 2>&1
'''

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    return output.decode('utf-8').strip(), error.decode('utf-8').strip()

def check_and_commit(repo_path):
    repo_name = os.path.basename(repo_path)
    os.chdir(repo_path)

    # Skip if there are no changes
    status_output, _ = run_command("git status --porcelain")
    if not status_output:
        return

    # Skip if we committed today already
    today = datetime.now().strftime("%Y-%m-%d")
    last_commit_date, _ = run_command("git log -1 --format=%cd --date=short")
    if last_commit_date == today:
        return

    commit_message = f"Auto-commit: {today}"
    _, error = run_command(f"git add . && git commit -m '{commit_message}'")

    print(f"Attempting to commit changes in '{repo_name}' on '{today}'")
    if error:
        print(f"Error during commit: {error}")
    else:
        print(f"Changes committed with message: {commit_message}")
    print("")

def main():
    if len(sys.argv) != 2:
        raise ValueError("Usage: python commit_daily.py <repo_path>")
    
    repo_path = sys.argv[1]
    check_and_commit(repo_path)


if __name__ == "__main__":
    main()