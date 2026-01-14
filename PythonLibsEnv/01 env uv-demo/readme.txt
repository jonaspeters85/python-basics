
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



Debuggen in VS Code
===================
Weg 1 (am einfachsten): VS Code nutzt die .venv von uv

Wenn du im Projekt eine .venv hast (typisch bei uv sync), dann:

uv sync (damit .venv existiert)

In VS Code: Command Palette → Python: Select Interpreter

Wähle den Interpreter aus:

macOS/Linux: .venv/bin/python

Windows: .venv\Scripts\python.exe

Dann kannst du ganz normal den Pfeil drücken und VS Code debuggt im richtigen venv.

Optional (empfohlen) in .vscode/settings.json:

{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.terminal.activateEnvironment": true
}




In VS Code öffnest du die Command Palette so:

macOS: ⌘ + ⇧ + P (Command + Shift + P)
(Alternativ: F1)

Windows / Linux: Ctrl + Shift + P
(Alternativ: F1)

Auch über das Menü geht’s:

View → Command Palette…

