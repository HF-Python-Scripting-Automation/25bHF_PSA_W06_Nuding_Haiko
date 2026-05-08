# Path: aufgaben/log_fetcher.py
import sys
import argparse
import paramiko
from utils.logger_config import get_aufgabe_03_logger


def main(args: argparse.Namespace) -> int:
    """
    Establishes an SSH connection to server-1 and executes uname -a.
    Implements mandatory error handling and resource safety.
    """
    logger = get_aufgabe_03_logger()

    # Infrastructure Context: server-1
    host: str = "192.168.110.10"
    user: str = "vmadmin"
    password: str = "sml1234"
    command: str = "uname -a"

    # Task essence for observability
    task_essence: str = "Verify SSH connectivity to server-1 and fetch system info"
    logger.debug(f"Task Essence: {task_essence}")
    logger.debug(f"Target: {user}@{host} | Remote Command: {command}")

    # Initialization of the SSHClient (Step 1)
    client = paramiko.SSHClient()

    # Policy for unknown host keys (Step 2)
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        logger.info(f"Connecting to {host}...")

        # Connection establishment (Step 3)
        client.connect(hostname=host, username=user, password=password, timeout=10)
        logger.info(f"Successfully connected to {host}")

        # Command execution (Step 4)
        stdin, stdout, stderr = client.exec_command(command)

        # Read and decode remote output (Step 5)
        # Using explicit utf-8 encoding strategy
        remote_response: str = stdout.read().decode('utf-8').strip()

        # Log output with the required mandatory prefix
        logger.info(f"[SERVER-1 OUTPUT]: {remote_response}")

        return 0

    except paramiko.AuthenticationException:
        logger.error(f"Authentication failed for {user} on {host}. Check credentials.")
        return 1
    except paramiko.SSHException as ssh_err:
        logger.error(f"SSH protocol error: {ssh_err}")
        return 1
    except Exception as e:
        logger.error(f"Connectivity check failed: {e}")
        return 1
    finally:
        # Resource Safety (Step 5): Ensure session is always closed
        client.close()
        logger.debug(f"SSH session to {host} closed.")


def cli() -> int:
    """
    CLI wrapper for log_fetcher.py.
    """
    parser = argparse.ArgumentParser(description="SSH Connectivity Check for server-1.")
    args = parser.parse_args()
    return main(args)


if __name__ == "__main__":
    # Execution Flow: Exit via sys.exit using return code from main
    sys.exit(cli())