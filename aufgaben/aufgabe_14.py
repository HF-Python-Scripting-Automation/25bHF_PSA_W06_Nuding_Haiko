# Path: aufgaben/aufgabe_14.py
import re
import sys
import argparse
import paramiko
from utils.logger_config import get_aufgabe_14_logger


def main(args: argparse.Namespace) -> int:
    """
    Parses docker ps output on server-3 to extract and map external to internal
    ports for the Metasploitable container using Regex Capture Groups.
    """
    logger = get_aufgabe_14_logger()

    # Infrastructure Details
    host: str = "192.168.110.12"
    user: str = "vmadmin"
    password: str = "sml1234"

    task_essence = "Docker Port Mapping Audit using Regex Capture Groups"

    # Regex-Erklärung:
    # 0\.0\.0\.0:  -> Sucht den fixen Teil der IP
    # (\d+)        -> Gruppe 1: Findet eine oder mehrere Ziffern (Externer Port)
    # ->           -> Sucht den Pfeil-Trenner
    # (\d+)        -> Gruppe 2: Findet eine oder mehrere Ziffern (Interner Port)
    # /tcp         -> Sucht das Protokoll
    regex_port_map = r"0\.0\.0\.0:(\d+)->(\d+)/tcp"

    logger.debug(f"Task Essence: {task_essence}")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        logger.info(f"Connecting to {host} for Docker port mapping audit...")
        client.connect(hostname=host, username=user, password=password, timeout=10)

        # Schritt 1: Docker PS ausführen
        # Wir brauchen sudo, um auf die Docker-Laufzeit zuzugreifen
        cmd = "sudo docker ps"
        stdin, stdout, stderr = client.exec_command(f'echo "{password}" | sudo -S {cmd}')
        output = stdout.read().decode('utf-8')

        # Schritt 2: finditer verwenden
        # finditer gibt uns Match-Objekte zurück, mit denen wir auf Gruppen zugreifen können
        matches = re.finditer(regex_port_map, output)

        found_mapping = False
        logger.info("Analyse der Metasploitable Port-Zuweisungen:")

        for match in matches:
            # Capture Groups extrahieren
            external_port = match.group(1)  # Die erste Klammer (\d+)
            internal_port = match.group(2)  # Die zweite Klammer (\d+)

            # Ausgabe im geforderten Format
            logger.info(
                f"[PORT-MAP]: Der externe Port {external_port} leitet auf den internen Port {internal_port} weiter.")
            found_mapping = True

        if not found_mapping:
            logger.warning("Keine Port-Mappings im Docker-Output gefunden.")

        return 0

    except Exception as e:
        logger.error(f"Fehler beim Port-Mapping Audit auf {host}: {e}")
        return 1
    finally:
        client.close()
        logger.debug("SSH Verbindung geschlossen.")


def cli() -> int:
    parser = argparse.ArgumentParser(description="Map Docker ports for Metasploitable.")
    args = parser.parse_args()
    return main(args)


if __name__ == "__main__":
    sys.exit(cli())