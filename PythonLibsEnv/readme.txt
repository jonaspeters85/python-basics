
UV install
==========
curl -LsSf https://astral.sh/uv/install.sh | sh
uv --version

Windows:
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
uv --version

oder 
winget install --id=astral-sh.uv -e

Wenn Policy meckert:
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

---
Wenn uv installiert ist, aber nicht gefunden wird

Die uv.exe liegt typischerweise hier:
%USERPROFILE%\.local\bin (also $HOME\.local\bin)

Für die aktuelle Session kannst du testweise:

$env:Path = "$HOME\.local\bin;$env:Path"
uv --version


Wenn das klappt, füge den Pfad dauerhaft zur User-PATH hinzu (PowerShell):

[Environment]::SetEnvironmentVariable("Path", "$HOME\.local\bin;" + [Environment]::GetEnvironmentVariable("Path","User"), "User")
---

Dann neues Terminal öffnen.

===============================================================
1) Projekt anlegen (mit uv)

mkdir uv-demo
cd uv-demo

# Projekt-Grundgerüst erzeugen
uv init

# Python-Version fürs Projekt festlegen (Beispiel: 3.12)
echo "3.12" > .python-version

# Dependency hinzufügen
uv add pydantic

uv lock
uv sync


2) py datei anlegen

3) Ausführen im richtigen environment

uv run python main.py