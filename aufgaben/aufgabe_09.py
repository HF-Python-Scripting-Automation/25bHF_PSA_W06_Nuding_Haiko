# Path: aufgaben/aufgabe_09.py
import re
import sys
import argparse
import paramiko
from utils.logger_config import get_aufgabe_09_logger


def main(args: argparse.Namespace) -> int:
    """
    Connects to server-3 and counts HTTP 4xx status codes using the worksheet's
    recommended regex pattern and logic.
    """
    logger = get_aufgabe_09_logger()
    # Infrastructure Details
    host: str = "192.168.110.12"
    user: str = "vmadmin"
    password: str = "sml1234"

    # Task Essence
    task_essence = "Count HTTP 4xx client errors in Juice Shop logs"

    # WORKSHEET TIP REGEX:
    # "Erstelle ein Regex Muster, das nach dreistelligen Zahlen sucht,
    # die mit einer 4 beginnen und oft von Anführungszeichen oder Leerzeichen umgeben sind."
    regex_status_code = r"[\" ](4\d{2})[\" ]"

    # ADDITIONAL LOGIC FOR JUICE SHOP:
    # Because the Juice Shop logs 'UnauthorizedError' (which is a 401),
    # we add a second pattern to ensure the script actually finds the errors.
    regex_unauthorized = r"UnauthorizedError"

    logger.debug(f"Task Essence: {task_essence}")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        logger.info(f"Connecting to {host}...")
        client.connect(hostname=host, username=user, password=password, timeout=10)

        # Fetch logs
        container_name = "infra_juice-shop_1"
        logger.info(f"Fetching logs for: {container_name}")
        log_cmd = f"sudo docker logs --tail 200 {container_name}"
        stdin, stdout, stderr = client.exec_command(f'echo "{password}" | sudo -S {log_cmd}')

        # Combine streams
        logs = stdout.read().decode('utf-8') + stderr.read().decode('utf-8')

        # Step 3: Count occurrences using BOTH patterns
        # 1. First, search for the worksheet's required 3-digit number pattern
        standard_matches = re.findall(regex_status_code, logs)

        # 2. Second, search for the app-specific error messages
        app_specific_matches = re.findall(regex_unauthorized, logs)

        # Combine the results for the final count
        total_error_count = len(standard_matches) + len(app_specific_matches)

        # Output the statistics in a clean format
        logger.info(f"Analysis Complete: Found {total_error_count} instances of HTTP 4xx errors.")
        logger.debug(f"Breakdown: {len(standard_matches)} via status code, {len(app_specific_matches)} via error text.")

        return 0

    except Exception as e:
        logger.error(f"Failed to analyze Juice Shop logs: {e}")
        return 1
    finally:
        client.close()
        logger.debug("SSH connection closed.")


def cli() -> int:
    parser = argparse.ArgumentParser(description="Count HTTP 4xx errors in Juice Shop.")
    args = parser.parse_args()
    return main(args)


if __name__ == "__main__":
    sys.exit(cli())