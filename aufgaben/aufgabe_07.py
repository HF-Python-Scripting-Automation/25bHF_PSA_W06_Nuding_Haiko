# Path: aufgaben/aufgabe_07.py
import re
import sys
import os
import argparse
import paramiko
from utils.logger_config import get_aufgabe_07_logger

# Sicherstellen, dass das Projekt-Root im Pfad ist für 'utils'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    logger = get_aufgabe_07_logger()
except ModuleNotFoundError:
    print("Critical: utils.logger_config nicht gefunden. Run from project root.")
    sys.exit(1)


def main(args: argparse.Namespace) -> int:
    """
    Verbindet sich mit server-3, liest die vsftpd.log direkt aus dem
    Metasploitable-Container und extrahiert die Quell-IPs.
    """
    # Infrastruktur-Details
    host: str = "192.168.110.12"
    user: str = "vmadmin"
    password: str = "sml1234"

    # Task Essence und Regex-Muster
    task_essence: str = "Identifikation von FTP-Zugriffs-IPs via Log-Injection (Container-Intern)"
    # vsftpd loggt oft CONNECT oder LOGIN Versuche
    regex_ftp_keywords: str = r".*(CONNECT|vsftpd|USER|PASS).*"
    # Muster für IPv4 Adressen
    regex_ip: str = r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"

    logger.debug(f"Task Essence: {task_essence}")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        logger.info(f"Verbinde zu {host}...")
        client.connect(hostname=host, username=user, password=password, timeout=10)

        # Schritt 1: Container-Namen finden
        find_cmd = "sudo docker ps --format '{{.Names}}' --filter 'ancestor=tleemcjr/metasploitable2'"
        stdin, stdout, stderr = client.exec_command(f'echo "{password}" | sudo -S {find_cmd}')
        container_name = stdout.read().decode('utf-8').strip()

        if not container_name:
            logger.warning("Metasploitable Container nicht gefunden. Nutze Fallback...")
            container_name = "infra_metasploitable_1"

        # Schritt 2: Logs abrufen - DER FIX:
        # Wir müssen in den Container hineingreifen, da die FTP-Logs nicht an stdout gehen
        logger.info(f"Extrahiere /var/log/vsftpd.log aus Container '{container_name}'...")
        log_cmd = f"sudo docker exec {container_name} cat /var/log/vsftpd.log"

        stdin, stdout, stderr = client.exec_command(f'echo "{password}" | sudo -S {log_cmd}')

        # Den Stream auslesen
        full_logs = stdout.read().decode('utf-8')

        # Schritt 3: Analyse und IP-Extraktion
        unique_ips = set()
        lines = full_logs.splitlines()

        for line in lines:
            # Wir prüfen auf FTP-Relevanz
            if re.search(regex_ftp_keywords, line, re.IGNORECASE):
                # IP extrahieren
                ip_match = re.search(regex_ip, line)
                if ip_match:
                    ip = ip_match.group(1)
                    # Wir ignorieren die lokale Loopback-IP des Containers falls vorhanden
                    if ip != "127.0.0.1":
                        unique_ips.add(ip)

        # Schritt 4: Ausgabe
        if unique_ips:
            logger.info(f"Erfolg! Gefundene IPs mit FTP-Interaktion ({len(unique_ips)}):")
            for ip in sorted(unique_ips):
                logger.info(f"[FTP-SOURCE]: {ip}")
        else:
            logger.info("Keine FTP-bezogenen IP-Adressen in /var/log/vsftpd.log gefunden.")
            logger.info("Hinweis: Stelle sicher, dass du zuvor einen FTP-Connect von Kali aus gemacht hast.")

        return 0

    except Exception as e:
        logger.error(f"Fehler bei der Container-Analyse: {e}")
        return 1
    finally:
        client.close()
        logger.debug("SSH Verbindung geschlossen.")


def cli() -> int:
    parser = argparse.ArgumentParser(description="FTP Log Analyse (Metasploitable Intern).")
    args = parser.parse_args()
    return main(args)


if __name__ == "__main__":
    sys.exit(cli())