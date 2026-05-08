# Path: aufgaben/aufgabe_05.py
import re
import sys
import os
import time
import argparse
import paramiko
from utils.logger_config import get_aufgabe_05_logger

# Robustness: Ensure the project root is in the search path for 'utils'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from utils.logger_config import get_aufgabe_05_logger
except ModuleNotFoundError:
    print("Critical: utils.logger_config not found. Run from project root.")
    sys.exit(1)


def main(args: argparse.Namespace) -> int:
    """
    Connects to server-2, restarts the SSH service using sudo,
    and verifies the success via journalctl logs.
    """
    logger = get_aufgabe_05_logger()

    # Connection details for server-2
    host: str = "192.168.110.11"
    user: str = "vmadmin"
    password: str = "sml1234"

    # Task essence and Regex
    task_essence: str = "Restart remote SSH service and verify via journalctl"
    # This regex looks for the 'Started' message in systemd logs for SSH
    regex_confirm: str = r".*Started (SSH|OpenBSD Secure Shell).*"

    logger.debug(f"Task Essence: {task_essence}")
    logger.debug(f"Applied Regex: {regex_confirm}")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        logger.info(f"Connecting to {host}...")
        client.connect(hostname=host, username=user, password=password, timeout=10)

        # Step 1: Execute Sudo Restart
        # The -S flag tells sudo to read the password from standard input
        restart_cmd: str = f'echo "{password}" | sudo -S systemctl restart ssh'
        logger.info("Sending restart command for SSH service...")
        client.exec_command(restart_cmd)

        # Step 2: Mandatory Wait
        logger.info("Waiting 2 seconds for the service to stabilize...")
        time.sleep(2)

        # Step 3: Read Systemd Journal
        journal_cmd: str = "journalctl -u ssh --no-pager -n 10"
        logger.info(f"Fetching latest logs with: {journal_cmd}")
        stdin, stdout, stderr = client.exec_command(journal_cmd)
        journal_output: str = stdout.read().decode('utf-8')

        # Step 4: Extract confirmation using Regex
        # We split the output into lines and search from bottom to top (newest first)
        lines = journal_output.strip().split('\n')
        confirmation_found = False

        for line in reversed(lines):
            if re.search(regex_confirm, line, re.IGNORECASE):
                logger.info(f"Verification Successful: {line.strip()}")
                confirmation_found = True
                break

        if not confirmation_found:
            logger.warning("Service command sent, but no confirmation found in recent journal logs.")

        return 0

    except Exception as e:
        logger.error(f"Failed to manipulate/monitor service on {host}: {e}")
        return 1
    finally:
        client.close()
        logger.debug(f"SSH connection to {host} closed.")


def cli() -> int:
    """
    CLI wrapper for task 05.
    """
    parser = argparse.ArgumentParser(description="Restart and monitor SSH service on server-2.")
    args = parser.parse_args()
    return main(args)


if __name__ == "__main__":
    sys.exit(cli())