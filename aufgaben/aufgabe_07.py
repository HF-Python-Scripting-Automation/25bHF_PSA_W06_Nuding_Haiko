# Path: aufgaben/aufgabe_07.py
import re
import sys
import argparse
import paramiko
from utils.logger_config import get_aufgabe_07_logger


def main(args: argparse.Namespace) -> int:
    """
    Connects to server-3, reads vsftpd.log directly from the
    Metasploitable container, and extracts source IPs.
    """
    logger = get_aufgabe_07_logger()

    # Infrastructure Details
    host: str = "192.168.110.12"
    user: str = "vmadmin"
    password: str = "sml1234"

    # Task Essence and Regex Patterns
    task_essence: str = "Identification of FTP access IPs via Log-Injection (Container-Internal)"
    # vsftpd often logs CONNECT, USER, or PASS attempts
    regex_ftp_keywords: str = r".*(CONNECT|vsftpd|USER|PASS).*"
    # Standard IPv4 pattern
    regex_ip: str = r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"

    logger.debug(f"Task Essence: {task_essence}")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        logger.info(f"Connecting to {host}...")
        client.connect(hostname=host, username=user, password=password, timeout=10)

        # Step 1: Locate Container Name
        find_cmd = "sudo docker ps --format '{{.Names}}' --filter 'ancestor=tleemcjr/metasploitable2'"
        stdin, stdout, stderr = client.exec_command(f'echo "{password}" | sudo -S {find_cmd}')
        container_name = stdout.read().decode('utf-8').strip()

        if not container_name:
            logger.warning("Metasploitable container not found. Using fallback name...")
            container_name = "infra_metasploitable_1"

        # Step 2: Retrieve Logs - Direct Internal Access
        # We must reach inside the container because FTP logs don't go to stdout
        logger.info(f"Extracting /var/log/vsftpd.log from container '{container_name}'...")
        log_cmd = f"sudo docker exec {container_name} cat /var/log/vsftpd.log"

        stdin, stdout, stderr = client.exec_command(f'echo "{password}" | sudo -S {log_cmd}')

        # Read the stream
        full_logs = stdout.read().decode('utf-8')

        # Step 3: Analysis and IP Extraction
        unique_ips = set()
        lines = full_logs.splitlines()

        for line in lines:
            # Check for FTP relevance
            if re.search(regex_ftp_keywords, line, re.IGNORECASE):
                # Extract IP
                ip_match = re.search(regex_ip, line)
                if ip_match:
                    ip = ip_match.group(1)
                    # Ignore internal loopback if present
                    if ip != "127.0.0.1":
                        unique_ips.add(ip)

        # Step 4: Output results
        if unique_ips:
            logger.info(f"Success! Found {len(unique_ips)} IPs with FTP interaction:")
            for ip in sorted(unique_ips):
                logger.info(f"[FTP-SOURCE]: {ip}")
        else:
            logger.info("No FTP-related IP addresses found in /var/log/vsftpd.log.")
            logger.info("Note: Ensure you have attempted an FTP connection from Kali first.")

        return 0

    except Exception as e:
        logger.error(f"Error during container analysis: {e}")
        return 1
    finally:
        client.close()
        logger.debug("SSH connection closed.")


def cli() -> int:
    parser = argparse.ArgumentParser(description="FTP Log Analysis (Metasploitable Internal).")
    args = parser.parse_args()
    return main(args)


if __name__ == "__main__":
    sys.exit(cli())