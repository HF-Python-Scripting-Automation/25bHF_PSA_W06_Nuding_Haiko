# Path: aufgaben/aufgabe_13.py
import re
import sys
import argparse
import paramiko
from utils.logger_config import get_aufgabe_13_logger


def main(args: argparse.Namespace) -> int:
    """
    Extracts MAC addresses from a server and filters out loopback and broadcast addresses.
    """
    logger = get_aufgabe_13_logger()

    # We choose server-1 for this audit
    host: str = "192.168.110.10"
    user: str = "vmadmin"
    password: str = "sml1234"

    task_essence = "Network Audit: Extracting physical MAC addresses"

    # High-precision MAC Regex: 6 blocks of 2 hex characters [0-9a-fA-F]
    regex_mac = r"([0-9a-fA-F]{2}(?::[0-9a-fA-F]{2}){5})"

    logger.debug(f"Task Essence: {task_essence}")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        logger.info(f"Connecting to {host} for network audit...")
        client.connect(hostname=host, username=user, password=password, timeout=10)

        # Step 1: Execute network command
        stdin, stdout, stderr = client.exec_command("ip link show")
        output = stdout.read().decode('utf-8')

        # Step 2: Find all MAC addresses
        all_macs = re.findall(regex_mac, output)

        # Step 3: Filter loopback/broadcast and display results
        found_real_mac = False
        for mac in all_macs:
            # Check if it's NOT the loopback (00:...) AND NOT the broadcast (ff:...)
            if mac != "00:00:00:00:00:00" and mac.lower() != "ff:ff:ff:ff:ff:ff":
                logger.info(f"[MAC-ADDRESS]: {mac}")
                found_real_mac = True

        if not found_real_mac:
            logger.warning("No physical MAC addresses found (only loopback, broadcast or nothing).")

        return 0

    except Exception as e:
        logger.error(f"Failed to extract MAC addresses from {host}: {e}")
        return 1
    finally:
        client.close()
        logger.debug("SSH connection closed.")


def cli() -> int:
    parser = argparse.ArgumentParser(description="Extract MAC addresses from a server.")
    args = parser.parse_args()
    return main(args)


if __name__ == "__main__":
    sys.exit(cli())