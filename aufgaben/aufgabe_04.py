# Path: aufgaben/aufgabe_04.py
import re
import sys
import argparse
import paramiko
from utils.logger_config import get_aufgabe_04_logger


def main(args: argparse.Namespace) -> int:
    """
    Connects to server-1 and identifies failed SSH login attempts using sudo.
    """
    logger = get_aufgabe_04_logger()

    # Infrastructure details
    host: str = "192.168.110.10"
    user: str = "vmadmin"
    password: str = "sml1234"

    # Use sudo -S to bypass potential permission issues on auth logs
    remote_log: str = "/var/log/auth.log"
    command: str = f"sudo -S cat {remote_log}"

    # Task essence and Regex
    task_essence: str = "Identify failed remote SSH login attempts via sudo"
    regex_pattern: str = r".*Failed password.*"

    logger.debug(f"Task Essence: {task_essence}")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        logger.info(f"Connecting to {host}...")
        client.connect(hostname=host, username=user, password=password, timeout=10)

        # Execution with pseudo-terminal for sudo support
        stdin, stdout, stderr = client.exec_command(command, get_pty=True)

        # Pass sudo password
        stdin.write(password + '\n')
        stdin.flush()

        log_content: str = stdout.read().decode('utf-8')
        matches = re.findall(regex_pattern, log_content)

        if matches:
            logger.info(f"Found {len(matches)} failed attempts on {host}:")
            for entry in matches:
                # Clean logging: ensure we don't log the sudo prompt itself
                if "password for" not in entry or "Failed password" in entry:
                    logger.info(f"[LOG-ENTRY]: {entry.strip()}")
        else:
            logger.info(f"No 'Failed password' entries found in {remote_log}.")
            # The Tip is back!
            logger.info("Tip: Try a failed SSH login from Kali: 'ssh user@192.168.110.10' with wrong PW.")

        return 0

    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        return 1
    finally:
        client.close()
        logger.debug("SSH connection closed.")


def cli() -> int:
    parser = argparse.ArgumentParser(description="Analyze remote logs on server-1.")
    args = parser.parse_args()
    return main(args)


if __name__ == "__main__":
    sys.exit(cli())