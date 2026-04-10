# EasyBash

![Python](https://img.shields.io/badge/python-3.8+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## Repo Description
### What it is

EasyBash is a Python-based CLI tool that simplifies Bash workflows by introducing higher-level commands for file and directory operations.

### Key Highlights

1. Simplifies repetitive terminal commands
2. Adds batch processing for files and directories
3. Works across Linux, macOS, Windows, and Termux
4. Lightweight and built using only Python standard libraries

---

## Purpose
### What it is for
EasyBash is designed to improve terminal productivity by reducing repetitive navigation and command execution patterns in Bash environments.

---

## Installation
### git clone
```bash
git clone https://github.com/sonych995-byte/EasyBash.git
chmod +x easybash
```

#### Run Directly
```bash
python easybash.py
```

### Load File (Manual Setup)
If running from another location:
```bash
python /path/to/easybash.py
```

---

## Global Access Setup (All Platforms)
### Linux / macOS
```bash
chmod +x easybash
sudo mv easybash /usr/local/bin/
```

### Windows
1. Create easybash.bat
```bash
@echo off
python C:\path\to\easybash.py %*
```
2. Add the folder to PATH environment variables

### termux
```bash
chmod +x easybash
mv easybash $PREFIX/bin/
```

## Commands Overview

### for
#### Description
Run a command on a single file across multiple directories.
#### syntax
```bash
for <filename> in <path1>|<path2> <command>
```
#### Usage
```bash
for test.txt in /tmp|/home "rm"
```

---

### rush
#### Description
Run a command across multiple directories.
#### Syntax
```bash
rush <path1>|<path2> <command>
```
#### Usage
```bash
rush /tmp|/home "ls -la"
```

---

### copy
#### Description
Copy files matching a pattern to multiple destinations.
#### Syntax
```bash
copy <pattern> <dest1>|<dest2>
```
#### Usage
```bash
copy *.log src|backup
```

---

### move
#### Description
Move files matching a pattern to multiple destinations.
#### Syntax
```bash
move <pattern> <dest1>|<dest2>
```
#### Usage
```bash
move *.tmp logs|archive
```

## How EasyBash Works
### Core Principle
EasyBash acts as a command interpreter that:
1. Parses custom commands
2. Converts them into shell operations
3. Executes them using Python subprocess
4. Handles multi-path execution logic
### Core Engine (Conceptual Code)
```python
while True:
    command = input("EasyBash> ")
    parsed = parse_command(command)
    execute(parsed)
```
### Execution Flow
1. Read user input
2. Parse command type
3. Extract paths / files / actions
4. Execute system commands
5. Return output

## version
v2.0.0
