# PSA Modul - Woche 6: Log-Analyse und SSH-Automatisierung

Dieses Projekt enthält die Lösungen für das Arbeitsblatt der Woche 6 im Modul PSA. 
Es automatisiert die Verbindung zu verschiedenen Servern, extrahiert Logdaten und analysiert diese mittels Regular Expressions (Regex).

## Projektstruktur

```text
  .
  ├── aufgaben/           # Alle Skripte (01-14)
  ├── logs/               # Log-Files pro Aufgabe
  ├── outputs/            # Ergebnisse (z.B. blacklist_ips.txt)
  ├── utils/              # Logger-Konfiguration
  ├── requirements.txt    # Abhängigkeiten
  └── OpenSSH_2k.log      # Lokales Log-File
```

## Voraussetzungen

Die Skripte wurden in einer Python 3.13 Virtual Environment (.venv) entwickelt. 
Die einzige externe Abhängigkeit ist paramiko.

Installation der Abhängigkeiten:
pip install -r requirements.txt

## Ausführung der Aufgaben

Da das Projekt eine modulare Struktur nutzt (z. B. für das `utils`-Paket), müssen die Skripte zwingend als **Python-Module** aus dem Wurzelverzeichnis gestartet werden. Dies stellt sicher, dass alle internen Abhängigkeiten korrekt aufgelöst werden.

### Ausführungsoptionen:

1. **Komfort-Option:** Im Ordner `.run/` befinden sich vorbereitete IDE-Konfigurationen, die die Skripte automatisch als Module im richtigen Kontext starten.
   
2. **Manuelle Option (Terminal):** Verwende den Flag `-m` und den Modulpfad (mit Punkten statt Slashes), während du dich im Hauptverzeichnis befindest:
   
   ```bash
   # Beispiel für Aufgabe 09
   python3 -m aufgaben.aufgabe_09

   # Beispiel für Aufgabe 14
   python3 -m aufgaben.aufgabe_14

### Highlights der Implementierung:
- Zentrales Logging: Jedes Skript nutzt einen dedizierten Logger, der sowohl in die Konsole als auch in eine entsprechende Datei im Ordner logs/ schreibt.
- Regex-Präzision: In Aufgabe 14 wurden gezielt Capture Groups eingesetzt, um externe und interne Ports voneinander zu trennen.
- Fehlerbehandlung: Alle SSH-Verbindungen sind mit try/except/finally Blöcken abgesichert, um eine saubere Trennung der Sessions zu gewährleisten.

## Abgabedetails
Name: Haiko Nuding
Kurs: 25bHF_PSA
Datum: 09.05.2026
