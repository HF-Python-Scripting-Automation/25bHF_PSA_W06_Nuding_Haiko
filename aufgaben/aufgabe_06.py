# Path: aufgaben/aufgabe_06.py
import re
import sys
import argparse
import paramiko
from utils.logger_config import get_aufgabe_06_logger


def main(args: argparse.Namespace) -> int:
    """
    Identifies the webserver technology (Apache/Nginx) and version
    of the DVWA Docker container on server-3.
    """
    logger = get_aufgabe_06_logger()

    host: str = "192.168.110.12"
    user: str = "vmadmin"
    password: str = "sml1234"

    # Task essence and Regex
    task_essence: str = "Identify webserver and version in DVWA Docker logs"
    # Pattern to find 'Apache/x.x.x' or 'nginx/x.x.x'
    regex_webserver: str = r"(Apache|nginx)\/([\d\.]+)"

    logger.debug(f"Task Essence: {task_essence}")
    logger.debug(f"Applied Regex: {regex_webserver}")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        logger.info(f"Connecting to {host}...")
        client.connect(hostname=host, username=user, password=password, timeout=10)

        # Step 1: Find container name for DVWA
        # We search for the container that uses the dvwa image
        logger.info("Locating DVWA container...")
        cmd_find: str = "sudo docker ps --format '{{.Names}}' --filter 'ancestor=vulnerables/web-dvwa'"
        stdin, stdout, stderr = client.exec_command(f'echo "{password}" | sudo -S {cmd_find}')
        container_name: str = stdout.read().decode('utf-8').strip()

        if not container_name:
            # Fallback: if filter fails, try to find by name directly
            container_name = "dvwa"
            logger.debug(f"Container filter empty, using fallback name: {container_name}")

        # Step 2: Fetch Docker logs
        logger.info(f"Fetching logs for container: {container_name}")
        cmd_logs: str = f"sudo docker logs {container_name}"
        # Note: Docker logs often go to stderr, but paramiko handles this via the streams
        stdin, stdout, stderr = client.exec_command(f'echo "{password}" | sudo -S {cmd_logs}')

        # We combine stdout and stderr because Docker logs can be tricky
        logs: str = stdout.read().decode('utf-8') + stderr.read().decode('utf-8')

        # Step 3: Analyze logs with Regex
        match = re.search(regex_webserver, logs, re.IGNORECASE)

        if match:
            server_name: str = match.group(1)
            version: str = match.group(2)
            logger.info(f"Technology Identified: {server_name}")
            logger.info(f"Version Identified: {version}")
            logger.info(f"Result: The application uses {server_name} version {version}")
        else:
            logger.warning("Webserver information not found in the first few log lines.")

        return 0

    except Exception as e:
        logger.error(f"Failed to identify technology on {host}: {e}")
        return 1
    finally:
        client.close()
        logger.debug("SSH session closed.")


def cli() -> int:
    parser = argparse.ArgumentParser(description="Identify DVWA webserver technology on server-3.")
    args = parser.parse_args()
    return main(args)


if __name__ == "__main__":
    sys.exit(cli())