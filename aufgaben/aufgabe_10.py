# Path: aufgaben/aufgabe_10.py
import re
import sys
import argparse
import paramiko
from utils.logger_config import get_aufgabe_10_logger


def main(args: argparse.Namespace) -> int:
    """
    Monitors disk usage on server-2 and warns if any partition exceeds 80%.
    """
    logger = get_aufgabe_10_logger()

    # Infrastructure Details
    host: str = "192.168.110.11"
    user: str = "vmadmin"
    password: str = "sml1234"

    # Task Essence and Regex
    task_essence = "Monitor disk space usage and alert on high occupancy"
    # Tip from worksheet: "Muster sucht nach einer oder mehreren Ziffern direkt gefolgt von einem Prozentzeichen"
    regex_usage = r"(\d+)%"

    logger.debug(f"Task Essence: {task_essence}")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        logger.info(f"Connecting to {host} to check disk usage...")
        client.connect(hostname=host, username=user, password=password, timeout=10)

        # Step 1: Execute disk free command
        stdin, stdout, stderr = client.exec_command("df -h")
        output = stdout.read().decode('utf-8')

        # Step 2: Extract all percentage values
        # re.findall returns only the captured group (the digits)
        usage_values = re.findall(regex_usage, output)

        # Step 3: Logic - Convert string to integer and compare
        threshold = 80
        alert_triggered = False

        for value_str in usage_values:
            # Convert to integer as requested: "Wandle die gefundenen Werte in echte Python Integer um"
            usage_int = int(value_str)

            if usage_int > threshold:
                logger.warning(f"ALERT: High disk usage detected! Partition at {usage_int}% (Threshold: {threshold}%)")
                alert_triggered = True
            else:
                logger.debug(f"Partition check: {usage_int}% is within safe limits.")

        if not alert_triggered:
            logger.info(f"Disk check completed. All partitions on {host} are below {threshold}%.")

        return 0

    except Exception as e:
        logger.error(f"Failed to monitor disk space on {host}: {e}")
        return 1
    finally:
        client.close()
        logger.debug("SSH connection closed.")


def cli() -> int:
    parser = argparse.ArgumentParser(description="Monitor disk usage on server-2.")
    args = parser.parse_args()
    return main(args)


if __name__ == "__main__":
    sys.exit(cli())