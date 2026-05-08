# Path: aufgaben/aufgabe_02.py
import re
import sys
import os
import argparse
from typing import Set
from utils.logger_config import get_aufgabe_02_logger


def main(args: argparse.Namespace) -> int:
    """
    Identifies failed login attempts and exports unique attacker IPs to a blacklist file.
    """
    logger = get_aufgabe_02_logger()

    # Path management relative to script location
    base_dir: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    logfile: str = os.path.join(base_dir, "OpenSSH_2k.log")
    output_dir: str = os.path.join(base_dir, "outputs")
    output_file: str = os.path.join(output_dir, "blacklist_ips.txt")

    # Task essence and regex definition for observability
    task_essence: str = "Extract unique attacker IPs from failed logins and export to blacklist"
    # Standard IPv4 Regex as defined in the worksheet
    regex_ip: str = r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"

    logger.debug(f"Task Essence: {task_essence}")
    logger.debug(f"Applied Regex Pattern: {regex_ip}")

    # Set for automatic duplicate removal (Efficiency requirement)
    attacker_ips: Set[str] = set()

    try:
        # Step 1: Parse log for failed password attempts
        logger.info(f"Scanning {logfile} for failed login attempts")

        with open(logfile, "r", encoding="utf-8") as file:
            for line in file:
                if "Failed password" in line:
                    match = re.search(regex_ip, line)
                    if match:
                        attacker_ips.add(match.group(1))

        logger.info(f"Identified {len(attacker_ips)} unique malicious IP addresses")

        # Step 2: Idempotent directory creation for outputs
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            logger.debug(f"Created directory: {output_dir}")

        # Step 3: Export collected IPs to the blacklist file
        with open(output_file, "w", encoding="utf-8") as out:
            # Sort IPs for better readability in the output file
            for ip in sorted(attacker_ips):
                out.write(f"{ip}\n")

        logger.info(f"Blacklist successfully exported to {output_file}")
        return 0

    except FileNotFoundError:
        logger.error(f"Required log file not found: {logfile}")
        return 1
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return 1


def cli() -> int:
    """
    CLI wrapper for argument parsing and execution flow.
    """
    parser = argparse.ArgumentParser(description="Extract unique attacker IPs for blacklisting.")
    args = parser.parse_args()
    return main(args)


if __name__ == "__main__":
    sys.exit(cli())