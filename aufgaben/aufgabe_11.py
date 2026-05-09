# Path: aufgaben/aufgabe_11.py
import re
import sys
import argparse
import paramiko
from utils.logger_config import get_aufgabe_11_logger


def main(args: argparse.Namespace) -> int:
    """
    Identifies users on server-1 who have /bin/bash as their default shell
    by auditing the /etc/passwd file.
    """
    logger = get_aufgabe_11_logger()

    # Infrastructure Details
    host: str = "192.168.110.10"
    user: str = "vmadmin"
    password: str = "sml1234"

    # Task Essence
    task_essence = "Audit /etc/passwd for interactive users with /bin/bash shell"

    # Regex Explanation:
    # ^([^:]+)   -> Group 1: Matches the username (everything at the start until the first colon)
    # :.*:       -> Matches the middle part (UID, GID, GECOS, Home dir)
    # /bin/bash$ -> Ensures the line ends exactly with /bin/bash
    regex_bash_users = r"^([^:]+):.*:/bin/bash$"

    logger.debug(f"Task Essence: {task_essence}")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        logger.info(f"Connecting to {host} for user account audit...")
        client.connect(hostname=host, username=user, password=password, timeout=10)

        # Step 1: Read the /etc/passwd file
        logger.info("Reading /etc/passwd content...")
        stdin, stdout, stderr = client.exec_command("cat /etc/passwd")
        content = stdout.read().decode('utf-8')

        # Step 2: Use Regex to find matching lines
        # re.MULTILINE is necessary for ^ and $ to match per line in the file string
        interactive_users = re.findall(regex_bash_users, content, re.MULTILINE)

        # Step 3: Output the results
        if interactive_users:
            logger.info(f"Audit Complete: Found {len(interactive_users)} interactive user(s).")
            # Sort the list for a cleaner output
            for user_name in sorted(interactive_users):
                logger.info(f"[USER-FOUND]: {user_name}")
        else:
            logger.warning("No users with /bin/bash shell found in /etc/passwd.")

        return 0

    except Exception as e:
        logger.error(f"Failed to audit users on {host}: {e}")
        return 1
    finally:
        client.close()
        logger.debug("SSH connection closed.")


def cli() -> int:
    parser = argparse.ArgumentParser(description="Identify users with /bin/bash on server-1.")
    args = parser.parse_args()
    return main(args)


if __name__ == "__main__":
    sys.exit(cli())