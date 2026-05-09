# Path: aufgaben/aufgabe_08.py
import re
import sys
import argparse
import paramiko
from utils.logger_config import get_aufgabe_08_logger


def main(args: argparse.Namespace) -> int:
    """
    Analyzes Mosquitto MQTT broker logs on server-3 to verify the listening port.
    """
    logger = get_aufgabe_08_logger()
    # Infrastructure Details
    host: str = "192.168.110.12"
    user: str = "vmadmin"
    password: str = "sml1234"

    # Task Essence and Regex
    task_essence: str = "Verify MQTT Broker port via Docker logs"
    # This pattern looks for "listening on port" or "socket on port" followed by digits
    regex_port: str = r"(?:listening on port|socket on port)\s+(\d+)"

    logger.debug(f"Task Essence: {task_essence}")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        logger.info(f"Connecting to {host}...")
        client.connect(hostname=host, username=user, password=password, timeout=10)

        # Step 1: Identify the Mosquitto container name
        # We filter by the image name 'eclipse-mosquitto'
        find_cmd = "sudo docker ps --format '{{.Names}}' --filter 'ancestor=eclipse-mosquitto'"
        stdin, stdout, stderr = client.exec_command(f'echo "{password}" | sudo -S {find_cmd}')
        container_name = stdout.read().decode('utf-8').strip()

        if not container_name:
            logger.warning("Mosquitto container not found. Using fallback name...")
            container_name = "infra_mosquitto_1"

        # Step 2: Fetch Docker logs
        logger.info(f"Fetching logs for container: {container_name}")
        log_cmd = f"sudo docker logs {container_name}"
        stdin, stdout, stderr = client.exec_command(f'echo "{password}" | sudo -S {log_cmd}')

        # Mosquitto often writes startup info to stderr, so we combine both streams
        full_output = stdout.read().decode('utf-8') + stderr.read().decode('utf-8')

        # Step 3: Extract and verify the port
        # We search for the first occurrence of the port in the logs
        match = re.search(regex_port, full_output)

        if match:
            extracted_port = match.group(1)
            port_int = int(extracted_port)
            standard_port = 1883

            # Final output in a clean sentence as requested
            if port_int == standard_port:
                logger.info(f"Result: The MQTT broker is correctly listening on the standard port {port_int}.")
            else:
                logger.warning(
                    f"Result: The MQTT broker is listening on port {port_int}, which deviates from the standard port 1883!")
        else:
            logger.info("Could not find any port assignment messages in the logs.")

        return 0

    except Exception as e:
        logger.error(f"Failed to analyze MQTT logs on {host}: {e}")
        return 1
    finally:
        client.close()
        logger.debug("SSH connection closed.")


def cli() -> int:
    parser = argparse.ArgumentParser(description="Analyze MQTT broker port on server-3.")
    args = parser.parse_args()
    return main(args)


if __name__ == "__main__":
    sys.exit(cli())