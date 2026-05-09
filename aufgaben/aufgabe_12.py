# Path: aufgaben/aufgabe_12.py
import re
import sys
import argparse
import paramiko
from utils.logger_config import get_aufgabe_12_logger


def main(args: argparse.Namespace) -> int:
    """
    Connects to all three servers and extracts the system load average using 'uptime'.
    """
    logger = get_aufgabe_12_logger()

    # List of target IPs as requested in the worksheet
    server_ips = ["192.168.110.10", "192.168.110.11", "192.168.110.12"]
    user: str = "vmadmin"
    password: str = "sml1234"

    task_essence = "Cross-server Uptime and Load Average Audit"

    # Regex to find the load averages (e.g., 0.05, 0.12, 0.09)
    # This looks for numbers with dots as decimal separators
    regex_load = r"(\d+\.\d+)"

    logger.debug(f"Task Essence: {task_essence}")

    for host in server_ips:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            logger.info(f"Connecting to {host}...")
            client.connect(hostname=host, username=user, password=password, timeout=10)

            # Step 1: Execute uptime
            stdin, stdout, stderr = client.exec_command("uptime")
            output = stdout.read().decode('utf-8').strip()

            # Step 2: Extract load averages using Regex
            # We expect exactly 3 values at the end of the uptime output
            loads = re.findall(regex_load, output)

            if len(loads) >= 3:
                # Take the last 3 matches (1, 5, and 15 min load)
                l1, l5, l15 = loads[-3:]
                logger.info(f"[LOAD-REPORT] Host: {host} | Load: {l1}, {l5}, {l15}")
            else:
                logger.warning(f"Could not parse load averages for {host}. Raw output: {output}")

        except Exception as e:
            logger.error(f"Failed to connect to {host}: {e}")
        finally:
            client.close()
            logger.debug(f"Connection to {host} closed.")

    return 0


def cli() -> int:
    parser = argparse.ArgumentParser(description="Cross-server load average check.")
    args = parser.parse_args()
    return main(args)


if __name__ == "__main__":
    sys.exit(cli())