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

Alle Aufgaben befinden sich im Verzeichnis aufgaben/. 
Um sicherzustellen, dass die Imports (insbesondere das utils-Paket für das Logging) korrekt funktionieren, 
sollten die Skripte aus dem Wurzelverzeichnis des Projekts gestartet werden:

# Beispiel für Aufgabe 9 (Juice Shop Analyse)
python3 aufgaben/aufgabe_09.py

# Beispiel für Aufgabe 14 (Docker Port Mapper)
python3 aufgaben/aufgabe_14.py

### Highlights der Implementierung:
- Zentrales Logging: Jedes Skript nutzt einen dedizierten Logger, der sowohl in die Konsole als auch in eine entsprechende Datei im Ordner logs/ schreibt.
- Regex-Präzision: In Aufgabe 14 wurden gezielt Capture Groups eingesetzt, um externe und interne Ports voneinander zu trennen.
- Fehlerbehandlung: Alle SSH-Verbindungen sind mit try/except/finally Blöcken abgesichert, um eine saubere Trennung der Sessions zu gewährleisten.

## Abgabedetails
Name: Haiko Nuding
Kurs: 25bHF_PSA
Datum: 09.05.2026
