# Path: aufgabe_01.py
import re
import sys
import argparse
from utils.logger_config import get_aufgabe_01_logger


def main(args: argparse.Namespace) -> int:
    """
    Performs local log analysis on OpenSSH_2k.log to find successful logins.
    """
    logger = get_aufgabe_01_logger()
    logfile = "OpenSSH_2k.log"

    logger.info(f"Starting analysis of {logfile} on Kali Linux client")

    try:
        # Resource Safety: Using context manager with explicit encoding
        with open(logfile, "r", encoding="utf-8") as file:
            for line in file:
                # Check for successful login keyword
                if "Accepted password" in line:
                    clean_line: str = line.strip()
                    logger.info(f"Found match: {clean_line}")

                    # Regex extraction for username and IP address
                    match = re.search(r"Accepted password for (\w+) from ([\d.]+)", clean_line)

                    if match:
                        user: str = match.group(1)
                        ip: str = match.group(2)
                        logger.info(f"Successful login: User {user} from IP {ip}")

        return 0

    except FileNotFoundError:
        logger.error(f"Log file '{logfile}' not found in current directory")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error during log analysis: {e}")
        return 1


def cli() -> int:
    """
    CLI wrapper for argument parsing and execution flow.
    """
    parser = argparse.ArgumentParser(description="Local log analysis for successful SSH logins.")
    args = parser.parse_args()
    return main(args)


if __name__ == "__main__":
    # Execution Flow: Exit via sys.exit using CLI wrapper return code
    sys.exit(cli())