import paramiko

# 1. Instanziierung
client = paramiko.SSHClient()

# 2. Policy für unbekannte Keys (wichtig für die Laborumgebung)
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# 3. Verbindungsaufbau
client.connect(
    hostname="192.168.110.10",
    username="vmadmin",
    password="sml1234"
)

# 4. Befehl ausführen
stdin, stdout, stderr = client.exec_command("uname -a")

# 5. Output auslesen und schliessen
print(stdout.read().decode())
client.close()